# RedHat x IBM InstructLab Bias Detection Model

This project fine-tunes [RedHat x IBM InstructLab](http://instructlab.ai/) to create a Bias Detection Model. Using taxonomies across multiple bias categories, the model identifies bias in text, highlights the relevant content, and explains why it is biased — helping users understand what to avoid.

## Overview

InstructLab's model-agnostic technology allows new skills to be composed into an open source model without retraining from scratch. We use this framework to generate synthetic training data and fine-tune a Granite-7B base model for bias detection across 6 categories.

## Small Example

<img width="1241" height="745" alt="image" src="https://github.com/user-attachments/assets/bb29a09d-c53d-43c0-8b0f-36f52e2b8536" />

---

## Bias Categories

| Category | Description |
|---|---|
| **Political** | Flag any poltical favoritism, negative comments, and sterotyping baased of poltical views |
| **Gender** | Flag any gender stereotyping or discrimination that can affect external decision (ex. professional development) |
| **Ageism** | Flag any stereotyping or discrimination based on age |
| **Ethical** | Flag racial, cultural, religious, language/dialect, and socioeconomic biases |
| **Marketing** | Flag any text that seems to contain fabricated claims in promotional content |
| **Research** | Flag any confirmation bias, selective reporting, opinionized views, and overconfident conclusions |

---

## Results

| Metric | Original Model | Our Bias Detection Model |
|---|---|---|
| Political Bias Accuracy | ---% | **100%** |
| Political Bias F1 | --- | **1.00** |
| Sexism Accuracy | ---% | see `kaggle_testing/results/` |

---

## Pipeline Overview

```
bias/*/qna.yaml
       │
       ▼
auto_generate.py          ← stages taxonomies + runs ilab data generate
       │
       ▼
datasets/                 ← synthetic JSONL training data (SDG output)
       │
       ▼
ilab model train          ← fine-tunes Granite-7B on generated data
       │
       ▼
training_results/         ← checkpoints + final merged model
       │
       ▼
kaggle_testing/           ← evaluates on real-world bias datasets
response_testing/         ← evaluates free-form answers via GPT-4o-mini judge
```

---

## Project Structure

```
.
├── auto_generate.py              # Taxonomy staging + ilab SDG launcher
├── bias/                         # Seed taxonomies (qna.yaml per category)
│   ├── ageism/
│   ├── ethical bias/
│   ├── gender bias/
│   ├── marketing/
│   ├── political/
│   └── reasearch/
├── datasets/                     # Generated training/test data (JSONL)
│   └── SDG_Output/               # ilab recipe files
├── kaggle_testing/               # Evaluation against Kaggle datasets
│   ├── data/
│   │   ├── political_bias.csv
│   │   └── sexism.csv
│   ├── results/                  # Evaluation output (JSONL + JSON summary)
│   ├── political_test.py
│   └── sexism_test.py
├── response_testing/             # Free-form response quality evaluation
│   ├── test.py                   # GPT-4o-mini judge
│   └── custom_questions.jsonl    # Evaluation prompts
├── training_results/             # Model checkpoints + final merged model
│   ├── checkpoint-*/
│   ├── final/
│   └── merged_model/
└── unified_taxonomy/             # Staged taxonomy for ilab (auto-generated)
```

---

## Installation / How to Run

1. Clone this repository
2. [Install InstructLab for your system](https://docs.instructlab.ai/getting-started/mac_metal/)
3. Install Python dependencies:

```bash
pip install python-dotenv openai scikit-learn pyyaml transformers
```

### Generate synthetic training data

```bash
python auto_generate.py
```

### Train the model

```bash
ilab model train --data-path datasets/ --output-dir training_results/
```

### Serve the model

```bash
ilab model serve --model-path training_results/ggml-model-q8_0.gguf
```

### Run Kaggle evaluations

```bash
python kaggle_testing/political_test.py
python kaggle_testing/sexism_test.py
```

Results are written to `kaggle_testing/results/` as a JSONL file (per-row predictions) and a JSON summary (accuracy, precision, recall, F1).

### Run free-form response evaluation

Requires an OpenAI API key in a `.env` file:

```
OPENAI_API_KEY=sk-...
```

```bash
python response_testing/test.py
```

---

## Technologies Used

**IBM InstructLab** — instruction-based model refinement and synthetic dataset generation

**Granite-7B** — base LLM fine-tuned for bias detection

**MT-Bench** — evaluating model performance

**Git** — version control and project management

**Google Cloud Platform** — training and scalable compute

---

## Ethical Considerations

- The model addresses sensitive social concepts such as bias, discrimination, and stereotypes.
- There is a risk of false positives, where neutral or contextual language may be incorrectly flagged as biased.
- Over-reliance on the model may lead users to treat outputs as authoritative judgments rather than advisory feedback, which is not the intended use of this model.
- The model is designed to provide neutral explanations as much as possible to ensure outputs are not accusatory or moralizing.
- Bias detection outputs are intended to support reflection and revision, not punishment or exclusion.

---

## License

This project is licensed under the MIT License.

---

## Team

**CSC398 Group 1** — University of Toronto

- Shaarif Ali Syed
- Asser Ismail
- Remy Zazo
- Zelimir Stajic
- Belal Shrief

**Special Thanks**

Special thanks to our industry mentors Carol Chen and Wesley Chun, and to RedHat x IBM InstructLab for the model, guidance, and reference material that made this work possible.
