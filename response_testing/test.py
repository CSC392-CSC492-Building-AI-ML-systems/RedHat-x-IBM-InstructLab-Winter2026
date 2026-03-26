import json
import time
import uuid
import concurrent.futures
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "custom_questions.jsonl"
OUTPUT_DIR = BASE_DIR / "model_answers"
ANSWER_FILE = OUTPUT_DIR / "base-model.jsonl"
JUDGMENT_FILE = OUTPUT_DIR / "base-model_judged.jsonl"
SUMMARY_FILE = OUTPUT_DIR / "base-model_summary.json"

MODEL_ID = "ggml-model-f16.gguf"
JUDGE_MODEL = "gpt-4o-mini"

# Create OpenAI client
local_client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy-key-not-needed")
openai_client = OpenAI()

# =========================
# OUR MODEL CALL (NO FORMATTING HINTS)
# =========================
def call_your_model(prompt: str) -> str:
    response = local_client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            # Stripped all formatting constraints. It just acts as a baseline AI.
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

# =========================
# JUDGE PROMPT (ACCURACY & CATEGORIZATION ONLY)
# =========================
def build_judge_prompt(input_text: str, model_response: str) -> str:
    return f"""
You are evaluating a bias detection model. The model was given a text and asked to analyze it for bias without any formatting constraints or hints.

Input text:
"{input_text}"

Model response:
"{model_response}"

Score the model's response from 1 to 5 on the following criteria:
- assessment_correctness: Is the model correct in its overall assessment of whether the text contains bias? (1 = completely wrong, 5 = perfectly accurate assessment).
- categorization_correctness: Did the model successfully predict the correct specific category/type of bias (e.g., Political, Ageism, Gender, Marketing, Research, etc.)? (1 = failed to categorize or wrong category, 5 = explicitly named the correct category).
- reasoning_quality: Is the explanation logical and supported by the text?

CRITICAL: Do NOT penalize the model for its formatting, verbosity, or structure. Grade purely on the accuracy of its assessment and categorization.
"""

# =========================
# JUDGE MODEL
# =========================
def call_judge(prompt: str) -> dict:
    response = openai_client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "bias_eval_judgment",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "scores": {
                            "type": "object",
                            "properties": {
                                "assessment_correctness": {"type": "integer"},
                                "categorization_correctness": {"type": "integer"},
                                "reasoning_quality": {"type": "integer"}
                            },
                            "required": ["assessment_correctness", "categorization_correctness", "reasoning_quality"],
                            "additionalProperties": False
                        },
                        "overall_score": {"type": "number"},
                        "verdict": {
                            "type": "string",
                            "enum": ["weak", "fair", "strong"]
                        },
                        "justification": {"type": "string"}
                    },
                    "required": ["scores", "overall_score", "verdict", "justification"],
                    "additionalProperties": False
                }
            }
        }
    )
    return json.loads(response.choices[0].message.content)

# =========================
# GENERATE ANSWERS
# =========================
def generate_answers():
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(INPUT_FILE, "r", encoding="utf-8") as fin, open(ANSWER_FILE, "w", encoding="utf-8") as fout:
        for line_number, line in enumerate(fin, start=1):
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            question_id = item.get("question_id")
            prompt = item.get("turns")[0]
            model_response = call_your_model(prompt)

            record = {
                "question_id": question_id,
                "answer_id": str(uuid.uuid4()),
                "model_id": MODEL_ID,
                "choices": [{"index": 0, "turns": [model_response]}],
                "tstamp": time.time()
            }
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Answers saved to {ANSWER_FILE}")

# =========================
# RUN JUDGE
# =========================
def run_judge():
    with open(INPUT_FILE, "r", encoding="utf-8") as qf, open(ANSWER_FILE, "r", encoding="utf-8") as af:
        questions = [json.loads(line) for line in qf if line.strip()]
        answers = [json.loads(line) for line in af if line.strip()]

    def process_pair(qa_tuple):
        q, a = qa_tuple
        input_text = q["turns"][0]
        model_response = a["choices"][0]["turns"][0]
        judge_prompt = build_judge_prompt(input_text, model_response)
        judgment = call_judge(judge_prompt)
        return {"question_id": q["question_id"], "model_id": MODEL_ID, "judgment": judgment}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_pair, zip(questions, answers)))

    with open(JUDGMENT_FILE, "w", encoding="utf-8") as out:
        for res in results:
            out.write(json.dumps(res, ensure_ascii=False) + "\n")
    print(f"Judgments saved to {JUDGMENT_FILE}")

# =========================
# SUMMARIZE JUDGMENTS
# =========================
def summarize_judgments():
    totals = {
        "assessment_correctness": 0.0,
        "categorization_correctness": 0.0,
        "reasoning_quality": 0.0
    }
    count = 0

    with open(JUDGMENT_FILE, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            scores = item["judgment"]["scores"]

            totals["assessment_correctness"] += scores.get("assessment_correctness", 0)
            totals["categorization_correctness"] += scores.get("categorization_correctness", 0)
            totals["reasoning_quality"] += scores.get("reasoning_quality", 0)
            count += 1

    averages = {key: value / count for key, value in totals.items()}
    averages["true_overall_score"] = sum(averages.values()) / 3 

    summary = {
        "model_id": MODEL_ID,
        "judge_model": JUDGE_MODEL,
        "num_examples": count,
        "average_scores": averages
    }

    with open(SUMMARY_FILE, "w", encoding="utf-8") as fout:
        json.dump(summary, fout, indent=2)

    print(f"Summary saved to {SUMMARY_FILE}")
    print(json.dumps(summary, indent=2))

# =========================
# MAIN
# =========================
def main():
    print("Step 1: Generating model answers...")
    generate_answers()
    print("Step 2: Running judge...")
    run_judge()
    print("Step 3: Averaging scores...")
    summarize_judgments()
    print("Done!")

if __name__ == "__main__":
    main()
