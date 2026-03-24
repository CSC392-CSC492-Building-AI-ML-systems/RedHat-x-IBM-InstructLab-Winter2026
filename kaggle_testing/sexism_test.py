import csv
import json
import re
from pathlib import Path
from openai import OpenAI
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix

model_client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy-key-not-needed")

INPUT_CSV = "RedHat-x-IBM-InstructLab-Winter2026/kaggle_testing/data/sexism.csv"
OUTPUT_JSONL = "results/sexism_eval_results.jsonl"
SUMMARY_JSON = "results/sexism_eval_summary.json"

# optional filter: set to None to use all rows
USE_SPLIT = None  # e.g. "train", "dev", "test", or None


# =========================
# YOUR MODEL CALL
# =========================
def call_your_model(prompt: str) -> str:
    response = model_client.chat.completions.create(
        model="ggml-model-f16.gguf",
        messages=[
            {"role": "system", "content": "You are a bias detection assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# =========================
# PROMPT
# =========================
def build_prompt(text: str) -> str:
    return f"""Determine whether the following text contains sexism.

Text: "{text}"

Return exactly:
Label: SEXISM or NOT_SEXISM
Explanation: <short reason>"""


# =========================
# NORMALIZATION
# =========================
def normalize_gold_label(raw_label: str) -> str:
    label = raw_label.strip().lower()

    if label == "sexist":
        return "sexist"
    if label == "not sexist":
        return "not_sexist"

    return "unknown"


def normalize_model_label(answer: str) -> str:
    text = answer.strip().lower()

    # try to extract the explicit label line first
    match = re.search(r"label:\s*(.+)", text)
    if match:
        label_text = match.group(1).strip()
    else:
        label_text = text

    # check negative class first so "not sexism" doesn't get caught by "sexism"
    if any(x in label_text for x in ["not_sexism", "not sexism", "non-sexist", "non sexist", "not sexist"]):
        return "not_sexist"

    if any(x in label_text for x in ["sexism", "sexist"]):
        return "sexist"

    return "unknown"


# =========================
# DATA LOADING
# =========================
def load_dataset(input_csv: str, use_split: str | None = None):
    rows = []

    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if use_split is not None and row["split"].strip().lower() != use_split.lower():
                continue

            rows.append({
                "id": row["rewire_id"],
                "text": row["text"],
                "gold_label": normalize_gold_label(row["label_sexist"]),
                "label_category": row["label_category"],
                "label_vector": row["label_vector"],
                "split": row["split"],
            })

    return rows


# =========================
# MAIN EVAL
# =========================
def main():
    dataset = load_dataset(INPUT_CSV, USE_SPLIT)

    Path("results").mkdir(exist_ok=True)

    y_true = []
    y_pred = []
    unknown_predictions = 0
    output_rows = []

    for item in dataset:
        prompt = build_prompt(item["text"])
        model_answer = call_your_model(prompt)
        pred_label = normalize_model_label(model_answer)

        if pred_label == "unknown":
            unknown_predictions += 1

        record = {
            "id": item["id"],
            "text": item["text"],
            "gold_label": item["gold_label"],
            "pred_label": pred_label,
            "correct": pred_label == item["gold_label"],
            "label_category": item["label_category"],
            "label_vector": item["label_vector"],
            "split": item["split"],
            "model_answer": model_answer,
        }
        output_rows.append(record)

        if item["gold_label"] != "unknown" and pred_label != "unknown":
            y_true.append(item["gold_label"])
            y_pred.append(pred_label)

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for row in output_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    if not y_true:
        print("No valid predictions to score.")
        return

    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="binary",
        pos_label="sexist",
        zero_division=0,
    )
    cm = confusion_matrix(y_true, y_pred, labels=["sexist", "not_sexist"]).tolist()
    report = classification_report(y_true, y_pred, zero_division=0)

    summary = {
        "input_csv": INPUT_CSV,
        "evaluated_split": USE_SPLIT,
        "total_rows_loaded": len(dataset),
        "total_scored": len(y_true),
        "unknown_predictions": unknown_predictions,
        "accuracy": accuracy,
        "precision_sexist": precision,
        "recall_sexist": recall,
        "f1_sexist": f1,
        "confusion_matrix_labels": ["sexist", "not_sexist"],
        "confusion_matrix": cm,
    }

    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Rows loaded:        {len(dataset)}")
    print(f"Rows scored:        {len(y_true)}")
    print(f"Unknown predicted:  {unknown_predictions}")
    print(f"Accuracy:           {accuracy:.4f}")
    print(f"Precision (sexist): {precision:.4f}")
    print(f"Recall (sexist):    {recall:.4f}")
    print(f"F1 (sexist):        {f1:.4f}")
    print("\nClassification report:\n")
    print(report)
    print("Confusion matrix [sexist, not_sexist]:")
    print(cm)


if __name__ == "__main__":
    main()