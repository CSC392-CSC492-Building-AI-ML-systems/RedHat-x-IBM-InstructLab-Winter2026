import os
import shutil
import subprocess
import glob

# --- Configuration ---
BASE_DIR = os.getcwd()
SOURCE_BIAS_DIR = os.path.join(BASE_DIR, "bias")
TAXONOMY_DIR = os.path.join(BASE_DIR, "unified_taxonomy")
SDG_OUTPUT_DIR = os.path.join(BASE_DIR, "datasets", "SDG_Output")
ILAB_DATASETS_DIR = os.path.expanduser("~/.local/share/instructlab/datasets")

def clean_old_output():
    print("\n" + "="*50)
    print("🧹 STEP 1: Cleaning Old SDG_Output")
    print("="*50)
    if os.path.exists(SDG_OUTPUT_DIR):
        shutil.rmtree(SDG_OUTPUT_DIR)
        print("   -> Removed old datasets/SDG_Output folder.")
    else:
        print("   -> No old datasets/SDG_Output folder found to remove.")

def fix_and_stage_taxonomies():
    print("\n" + "="*50)
    print("🛠️ STEP 2: Smart-Parsing YAML and Building Taxonomy Tree")
    print("="*50)
    
    if not os.path.exists(SOURCE_BIAS_DIR):
        print(f"❌ Could not find the source folder: {SOURCE_BIAS_DIR}")
        return False

    if os.path.exists(TAXONOMY_DIR):
        print("   -> 🧹 Wiping old unified_taxonomy staging folder...")
        shutil.rmtree(TAXONOMY_DIR)

    for category in os.listdir(SOURCE_BIAS_DIR):
        category_path = os.path.join(SOURCE_BIAS_DIR, category)
        if not os.path.isdir(category_path):
            continue
        
        qna_path = os.path.join(category_path, "qna.yaml")
        is_knowledge = False
        
        # 1. Read the file to determine if it is Knowledge or a Skill
        if os.path.exists(qna_path):
            with open(qna_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Knowledge files contain document references
                if "document_outline" in content or "document:" in content:
                    is_knowledge = True
                    
        # 2. Route to the correct InstructLab directory
        if is_knowledge:
            dest_category_path = os.path.join(TAXONOMY_DIR, "knowledge", "bias", category)
        else:
            dest_category_path = os.path.join(TAXONOMY_DIR, "compositional_skills", "bias", category)
            
        os.makedirs(dest_category_path, exist_ok=True)

        # 3. Process and fix the files
        for filename in os.listdir(category_path):
            src_file = os.path.join(category_path, filename)
            dest_file = os.path.join(dest_category_path, filename)

            if filename == "qna.yaml":
                with open(src_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    if not is_knowledge and line.strip().startswith("domain:"):
                        # Skills need task_description instead of domain
                        new_lines.append(f"task_description: Teach the model to identify and categorize {category} bias in text.")
                    else:
                        # Remove trailing spaces from each individual line
                        new_lines.append(line.rstrip())
                
                # Join the document back together
                clean_content = "\n".join(new_lines)
                
                # Strip all excess newlines at the end, then add exactly ONE back
                clean_content = clean_content.rstrip() + "\n"
                
                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(clean_content)
            
            elif os.path.isfile(src_file):
                shutil.copy(src_file, dest_file)
                
        type_str = "Knowledge" if is_knowledge else "Skill  "
        print(f"✅ Staged {type_str} taxonomy: {category}")
        
    return True

def generate_synthetic_data():
    print("\n" + "="*50)
    print("🚀 STEP 3: Generating Unified Synthetic Data")
    print("="*50)
    
    command = [
        "ilab", "data", "generate",
        "--taxonomy-path", TAXONOMY_DIR,
        "--taxonomy-base", "empty", 
        "--pipeline", "simple",
        "--sdg-scale-factor", "10"
    ]
    
    try:
        subprocess.run(command, check=True)
        print("\n🎉 Generation complete!")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Data generation failed. Please check the logs above.")
        return False

def harvest_and_organize_output():
    print("\n" + "="*50)
    print("📦 STEP 4: Harvesting Output into datasets/SDG_Output")
    print("="*50)
    
    if not os.path.exists(ILAB_DATASETS_DIR):
        print(f"❌ InstructLab datasets directory not found: {ILAB_DATASETS_DIR}")
        return

    # Find all generated directories (excluding checkpoints or loose files)
    all_items = glob.glob(os.path.join(ILAB_DATASETS_DIR, "*"))
    dirs_only = [d for d in all_items if os.path.isdir(d) and "checkpoints" not in os.path.basename(d)]
    
    if not dirs_only:
        print("❌ Could not find any newly generated dataset folders.")
        return
        
    # Sort by modification time to grab the absolute newest run
    latest_dir = max(dirs_only, key=os.path.getmtime)
    print(f"   -> Found newest generation output at: {latest_dir}")
    
    # Copy the entire directory structure into the repo
    os.makedirs(os.path.dirname(SDG_OUTPUT_DIR), exist_ok=True)
    shutil.copytree(latest_dir, SDG_OUTPUT_DIR)
    
    print(f"✅ Success! All new files have been cleanly organized into: {SDG_OUTPUT_DIR}")

if __name__ == "__main__":
    clean_old_output()
    if fix_and_stage_taxonomies():
        if generate_synthetic_data():
            harvest_and_organize_output()
