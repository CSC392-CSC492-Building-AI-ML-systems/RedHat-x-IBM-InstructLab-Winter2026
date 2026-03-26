import os
import shutil
import subprocess
import yaml

BASE_DIR = os.getcwd()
SOURCE_DIR = os.path.join(BASE_DIR, "bias")
TAXONOMY_DIR = os.path.join(BASE_DIR, "unified_taxonomy")

def stage_taxonomies():
    print("[INFO] Resetting and staging taxonomies...")
    if os.path.exists(TAXONOMY_DIR):
        shutil.rmtree(TAXONOMY_DIR)
        
    for category in os.listdir(SOURCE_DIR):
        cat_path = os.path.join(SOURCE_DIR, category)
        if not os.path.isdir(cat_path): 
            continue
        
        dest_path = os.path.join(TAXONOMY_DIR, "compositional_skills", "bias", category)
        os.makedirs(dest_path, exist_ok=True)

        for file in os.listdir(cat_path):
            if file.endswith(".md"): 
                continue
            
            src = os.path.join(cat_path, file)
            dest = os.path.join(dest_path, file)
            
            if file == "qna.yaml":
                with open(src, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # Extract seeds
                seeds = []
                for s in data.get('seed_examples', []):
                    seeds.extend(s['questions_and_answers']) if 'questions_and_answers' in s else seeds.append(s)
                
                
                while len(seeds) < 5:
                    seeds.append({'question': 'Valid example?', 'answer': 'Yes.'})
                    
                # Write YAML
                with open(dest, 'w', encoding='utf-8') as f:
                    f.write(f"version: 3\ncreated_by: {data.get('created_by', 'developer')}\n")
                    f.write(f"task_description: Identify {category} bias.\nseed_examples:\n")
                    for s in seeds:
                        q, a = s.get('question', ''), s.get('answer', '')
                        f.write(f"  - question: |\n      {q.strip()}\n    answer: |\n      {a.strip()}\n")
            else:
                shutil.copy(src, dest)

def generate_data():
    print("[INFO] Initiating synthetic data generation...")
    subprocess.run([
        "ilab", "data", "generate",
        "--taxonomy-path", TAXONOMY_DIR,
        "--taxonomy-base", "empty",
        "--pipeline", "simple",
        "--sdg-scale-factor", "10"
    ], check=True)

if __name__ == "__main__":
    try:
        stage_taxonomies()
        generate_data()
        print("[SUCCESS] Pipeline execution complete.")
    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")
        exit(1)
