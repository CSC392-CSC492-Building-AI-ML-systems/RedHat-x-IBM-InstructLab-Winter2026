import csv
import json
import re
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix

INPUT_CSV = "RedHat-x-IBM-InstructLab-Winter2026/kaggle_testing/data/political_bias.csv"
OUTPUT_JSONL = "results/political_bias_eval_results.jsonl"
SUMMARY_JSON = "results/political_bias_eval_summary.json"

# optional filter: set to None to use all rows
USE_SPLIT = None  # only use this if your dataset has a split column


# =========================
# YOUR MODEL CALL
# =========================
def call_your_model(prompt: str) -> str:
    """
    Replace this with your real model call.
    Expected output format:
        Label: BIAS
        Explanation: ...
    or
        Label: NOT_BIAS
        Explanation: ...
    """
    text = prompt.lower()

    bias_keywords = [
        "far left", "far right", "left-wing propaganda", "right-wing propaganda",
        "liberal agenda", "conservative agenda", "radical left", "extreme right",
        "biased media", "partisan attack"
    ]

    if any(word in text for word in bias_keywords):
        return "Label: BIAS\nExplanation: Contains politically biased or partisan language."

    return "Label: NOT_BIAS\nExplanation: No clear political bias."


# =========================
# PROMPT
# =========================
def build_prompt(text: str) -> str:
    return f"""Determine whether the following text contains political bias.

Treat any non-center political framing as BIAS.

Text: "{text}"

Return exactly:
Label: BIAS or NOT_BIAS
Explanation: <short reason>"""


# =========================
# NORMALIZATION
# =========================
def normalize_gold_label(raw_label: str) -> str:
    label = raw_label.strip().lower()

    if label == "center":
        return "not_bias"

    if label in {
        "lean left", "left", "far left",
        "lean right", "right", "far right",
        "biased"
    }:
        return "bias"

    return "unknown"


def normalize_model_label(answer: str) -> str:
    text = answer.strip().lower()

    # try to extract the explicit label line first
    match = re.search(r"label:\s*(.+)", text)
    if match:
        label_text = match.group(1).strip()
    else:
        label_text = text

    # check negative class first
    if any(x in label_text for x in ["not_bias", "not bias", "no bias", "center"]):
        return "not_bias"

    if "bias" in label_text or "biased" in label_text:
        return "bias"

    return "unknown"


# =========================
# DATA LOADING
# =========================
def load_dataset(input_csv: str, use_split: str | None = None):
    rows = []

    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        has_split = "split" in reader.fieldnames

        for row in reader:
            text = row.get("Text", "").strip()

            # SKIP BAD ROWS
            if not text or text.lower() == "error fetching article.":
                continue

            if use_split is not None and has_split:
                if row["split"].strip().lower() != use_split.lower():
                    continue

            rows.append({
                "id": row.get("Title", ""),
                "text": text,
                "gold_label": normalize_gold_label(row.get("Bias", "")),
                "source": row.get("Source", ""),
                "raw_bias": row.get("Bias", ""),
                "split": row.get("split", "") if has_split else "",
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
            "source": item["source"],
            "raw_bias": item["raw_bias"],
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
        pos_label="bias",
        zero_division=0,
    )
    cm = confusion_matrix(y_true, y_pred, labels=["bias", "not_bias"]).tolist()
    report = classification_report(y_true, y_pred, zero_division=0)

    summary = {
        "input_csv": INPUT_CSV,
        "evaluated_split": USE_SPLIT,
        "total_rows_loaded": len(dataset),
        "total_scored": len(y_true),
        "unknown_predictions": unknown_predictions,
        "accuracy": accuracy,
        "precision_bias": precision,
        "recall_bias": recall,
        "f1_bias": f1,
        "confusion_matrix_labels": ["bias", "not_bias"],
        "confusion_matrix": cm,
    }

    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Rows loaded:       {len(dataset)}")
    print(f"Rows scored:       {len(y_true)}")
    print(f"Unknown predicted: {unknown_predictions}")
    print(f"Accuracy:          {accuracy:.4f}")
    print(f"Precision (bias):  {precision:.4f}")
    print(f"Recall (bias):     {recall:.4f}")
    print(f"F1 (bias):         {f1:.4f}")
    print("\nClassification report:\n")
    print(report)
    print("Confusion matrix [bias, not_bias]:")
    print(cm)


if __name__ == "__main__":
    main()