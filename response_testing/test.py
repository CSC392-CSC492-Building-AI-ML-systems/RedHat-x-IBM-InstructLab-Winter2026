import json
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from .env
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "custom_questions.jsonl"
OUTPUT_DIR = BASE_DIR / "model_answers"
ANSWER_FILE = OUTPUT_DIR / "my-model.jsonl"
JUDGMENT_FILE = OUTPUT_DIR / "my-model_judged.jsonl"
SUMMARY_FILE = OUTPUT_DIR / "my-model_summary.json"

MODEL_ID = "my-model"
JUDGE_MODEL = "gpt-5.4-mini"

# Create OpenAI client
client = OpenAI()


# =========================
# OUR MODEL CALL
# =========================
def call_your_model(prompt: str) -> str:
    """
    Replace this with your actual model call.
    Right now this is a placeholder.
    """
    return (
        "Label: AGEISM\n"
        "Explanation: This statement stereotypes people based on age."
    )


# =========================
# JUDGE PROMPT
# =========================
def build_judge_prompt(input_text: str, model_response: str) -> str:
    return f"""
You are evaluating a bias detection model.

Input:
"{input_text}"

Model response:
"{model_response}"

Score from 1 to 5 on:
- label_correctness
- reasoning_quality
- evidence_grounding
- clarity

Guidelines:
- label_correctness: Is the predicted label appropriate for the text?
- reasoning_quality: Is the explanation logically sound?
- evidence_grounding: Does the explanation point to the text itself?
- clarity: Is the response clear and easy to understand?

Be strict and consistent. Do not reward explanations that sound fluent but are not supported by the text.
"""


# =========================
# JUDGE MODEL
# =========================
def call_judge(prompt: str) -> dict:
    response = client.responses.create(
        model=JUDGE_MODEL,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "bias_eval_judgment",
                "schema": {
                    "type": "object",
                    "properties": {
                        "scores": {
                            "type": "object",
                            "properties": {
                                "label_correctness": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 5
                                },
                                "reasoning_quality": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 5
                                },
                                "evidence_grounding": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 5
                                },
                                "clarity": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 5
                                }
                            },
                            "required": [
                                "label_correctness",
                                "reasoning_quality",
                                "evidence_grounding",
                                "clarity"
                            ],
                            "additionalProperties": False
                        },
                        "overall_score": {
                            "type": "number"
                        },
                        "verdict": {
                            "type": "string",
                            "enum": ["weak", "fair", "strong"]
                        },
                        "justification": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "scores",
                        "overall_score",
                        "verdict",
                        "justification"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.output_text)


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

            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {line_number}: {e}") from e

            question_id = item.get("question_id")
            turns = item.get("turns")

            if question_id is None:
                raise ValueError(f"Missing question_id on line {line_number}")

            if not isinstance(turns, list) or len(turns) != 1:
                raise ValueError(f"Question {question_id} must contain exactly one turn.")

            prompt = turns[0]
            model_response = call_your_model(prompt)

            record = {
                "question_id": question_id,
                "answer_id": str(uuid.uuid4()),
                "model_id": MODEL_ID,
                "choices": [
                    {
                        "index": 0,
                        "turns": [model_response]
                    }
                ],
                "tstamp": time.time()
            }

            fout.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Answers saved to {ANSWER_FILE}")


# =========================
# RUN JUDGE
# =========================
def run_judge():
    with open(INPUT_FILE, "r", encoding="utf-8") as qf, \
         open(ANSWER_FILE, "r", encoding="utf-8") as af, \
         open(JUDGMENT_FILE, "w", encoding="utf-8") as out:

        questions = [json.loads(line) for line in qf if line.strip()]
        answers = [json.loads(line) for line in af if line.strip()]

        if len(questions) != len(answers):
            raise ValueError("Number of questions and answers does not match.")

        for q, a in zip(questions, answers):
            input_text = q["turns"][0]
            model_response = a["choices"][0]["turns"][0]

            judge_prompt = build_judge_prompt(input_text, model_response)
            judgment = call_judge(judge_prompt)

            result = {
                "question_id": q["question_id"],
                "model_id": MODEL_ID,
                "judgment": judgment
            }

            out.write(json.dumps(result, ensure_ascii=False) + "\n")

    print(f"Judgments saved to {JUDGMENT_FILE}")


# =========================
# SUMMARIZE JUDGMENTS
# =========================
def summarize_judgments():
    totals = {
        "label_correctness": 0.0,
        "reasoning_quality": 0.0,
        "evidence_grounding": 0.0,
        "clarity": 0.0,
        "overall_score": 0.0
    }
    count = 0

    with open(JUDGMENT_FILE, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue

            item = json.loads(line)
            judgment = item["judgment"]
            scores = judgment["scores"]

            totals["label_correctness"] += scores.get("label_correctness", 0)
            totals["reasoning_quality"] += scores.get("reasoning_quality", 0)
            totals["evidence_grounding"] += scores.get("evidence_grounding", 0)
            totals["clarity"] += scores.get("clarity", 0)
            totals["overall_score"] += judgment.get("overall_score", 0)

            count += 1

    if count == 0:
        raise ValueError("No judgments found to summarize.")

    averages = {key: value / count for key, value in totals.items()}

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