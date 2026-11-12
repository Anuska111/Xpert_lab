# Xpert — WhatsApp Personal Context Analysis

<p align="center">
  **From everyday conversations to structured personal context.**
</p>

<p align="center">
  ![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
  ![Status](https://img.shields.io/badge/Status-Submitted%20for%20Evaluation-orange)
  ![Challenge](https://img.shields.io/badge/Xpert-Winter%20Internship-purple)
</p>

---

## Overview

**Xpert** is a WhatsApp personal context analysis project developed as part of the Xpert Winter Internship Challenge 2026.

People share important information through everyday conversations: plans, commitments, relationships, goals, and pending tasks. However, this information is often scattered across multiple chats.

This project aims to transform unstructured WhatsApp conversation data into structured personal context that can help a personal assistant understand:

- Who the important people are.
- Which organisations appear in conversations.
- What different chats are about.
- Which goals and intentions are expressed.
- What tasks and commitments are still pending.
- Where an assistant could potentially provide useful help.

## Key Objectives

| Component | Objective |
|---|---|
| Circles | Identify people and their connections |
| Organisations | Extract organisations mentioned in conversations |
| Chats | Understand and organise conversations |
| Goals | Identify personal goals and intentions |
| Open Loops | Detect pending tasks and commitments |
| Where to Help | Identify opportunities for useful assistance |

## Technical Approach

The project uses a modular Python-based architecture to process conversation data and generate structured output.

The implementation includes text processing, rule-based extraction, context analysis, task detection, and optional LLM-related functionality.

### Project Modules

| File | Purpose |
|---|---|
| `solution.py` | Main solution and execution pipeline |
| `nlp_engine.py` | NLP-related text processing |
| `ml_engine.py` | ML-related processing |
| `context_engine.py` | Context analysis |
| `task_engine.py` | Task and open-loop processing |
| `llm.py` | LLM-related functionality |
| `schema.json` | Structured output schema |
| `check.py` | Evaluation using the provided checker |

## Project Structure

```text
Xpert_lab/
│
├── ai-logs/
│   ├── README.md
│   ├── project-development.md
│   ├── debugging.md
│   └── evaluation-and-improvements.md
│
├── solution.py
├── nlp_engine.py
├── ml_engine.py
├── context_engine.py
├── task_engine.py
├── llm.py
├── check.py
├── schema.json
├── run.sh
├── README.md
├── WRITEUP.md
└── .gitignore
```

*Local challenge datasets and generated output files are intentionally excluded from version control.*

## Getting Started

### Requirements

- Python 3.11
- Git
- Xpert challenge starter kit and locally available challenge dataset

### 1. Clone the repository

```bash
git clone https://github.com/Anuska111/Xpert_lab.git
cd Xpert_lab
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install project dependencies

Install the dependencies required by the project in your Python environment.

### 4. Add the challenge dataset

Place the permitted challenge dataset in the expected local `data/` directory.

**Note:** The challenge dataset is not included in this repository.

## Run the Solution

Generate structured output:

```bash
python solution.py data/dev final_output.json
```

Evaluate the generated output:

```bash
python check.py data/dev final_output.json
```

The checker reports the output validity and evaluation performance across the labelled components.

## Latest Evaluation Results

<details>
<summary><strong>Local Checker Results — 19.1 / 56</strong></summary>

The latest local evaluation was performed using the provided Xpert checker.

| Evaluation Component | Score | Points |
|---|---:|---:|
| Circles | 0.24 | 2.9 / 12 |
| Organisations | 0.26 | 2.1 / 8 |
| Chats | 0.77 | 6.1 / 8 |
| Goals | Not labelled | — |
| Open loops found | 0.28 | 3.9 / 14 |
| Open loops closed right | 0.28 | 4.0 / 14 |
| Where to help | Not labelled | — |
| **Total data score** | | **19.1 / 56** |

</details>

### Extraction Summary

Latest local execution produced:

| Extracted Information | Count |
|---|---:|
| People | 286 |
| Organisations | 5 |
| Chats | 138 |
| Goals | 0 |
| Open loops | 246 |
| Completed loops | 51 |
| Pending loops | 195 |

**Important:** Extraction counts represent detected records, not necessarily correctly identified records. Accuracy is evaluated separately by the checker.

The challenge organisers separately assess cost, write-up quality, and one-command execution. Therefore, 19.1/56 is the local data score, not the final overall challenge score.

## Current Limitations

- Person and relationship identification need improvement.
- Organisation extraction needs better contextual understanding.
- Goal extraction is not yet producing results in the latest local run.
- Open-loop detection requires improved precision.
- LLM functionality was unavailable during the latest run, so the existing rule-based extraction was retained.

## Future Improvements

- Improve entity and relationship extraction.
- Introduce stronger contextual goal detection.
- Distinguish pending commitments from completed tasks more accurately.
- Reduce false-positive task detection.
- Improve recommendations for where an assistant can help.
- Evaluate improvements against the provided checker.

## AI-Assisted Development

AI tools were used as development assistants for:

- Understanding the challenge requirements.
- Planning the project structure.
- Learning relevant concepts.
- Debugging Python and Git issues.
- Interpreting checker results.
- Documenting development decisions.

Relevant AI development records are maintained in the `ai-logs/` directory.

## Data Privacy

- Challenge conversation data is kept locally.
- Dataset files are excluded from Git commits.
- Generated local outputs are excluded.
- API keys and environment secrets are not included in the repository.

## Author

**Anuska Biswas**

GitHub: [Anuska111](https://github.com/Anuska111)

Repository: [Xpert_lab](https://github.com/Anuska111/Xpert_lab)

---

<p align="center">
  **Xpert Winter Internship Challenge · 2026**
</p>
