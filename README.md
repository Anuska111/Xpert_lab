# XPERT | WhatsApp Personal Context Intelligence

<p align="center">
  <strong>Turning everyday conversations into meaningful personal context.</strong>
  <br/>
  An AI-assisted personal context extraction system built for the Xpert Winter Internship Challenge 2026.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Environment-Google%20Colab%20%7C%20PyCharm-orange" />
  <img src="https://img.shields.io/badge/Output-Structured%20JSON-blue" />
  <img src="https://img.shields.io/badge/Challenge-Xpert%202026-purple" />
</p>

---

## 01. Project Overview

Xpert is designed to understand the context hidden inside everyday WhatsApp conversations.

Important information is often scattered across multiple conversations — people, relationships, organisations, personal goals, commitments, and unfinished tasks.

The objective of this project is to transform unstructured chat data into structured information that can help a personal assistant understand a user's life and identify situations where assistance may be useful.

Rather than treating conversations as isolated messages, the system aims to extract meaningful context from them.

## 02. What Does the System Extract?

| Component | Description |
|---|---|
| **People & Circles** | Identifies people and their relationships |
| **Organisations** | Extracts companies, institutions, and groups |
| **Chats** | Processes and organises conversation information |
| **Goals** | Identifies goals and intentions |
| **Open Loops** | Detects pending tasks, promises, and commitments |
| **Where to Help** | Identifies potential opportunities for assistant intervention |

## 03. Development Workflow

The project development involved two environments: Google Colab for initial exploration and experimentation, and PyCharm for the main implementation and local execution.

### Google Colab — Data Exploration & Experimentation

Initial experimentation focused on understanding the conversation dataset and exploring possible processing approaches.

- Dataset exploration and inspection.
- Understanding WhatsApp conversation structures.
- Initial data analysis and experimentation.
- Reviewing extracted information and intermediate results.
- Exploring approaches for personal context extraction.

### PyCharm — Implementation & Execution

The main solution was organised and implemented as a modular Python project.

- Developing individual Python modules.
- Integrating text and context processing.
- Implementing task and open-loop extraction.
- Generating structured JSON output.
- Running local evaluations using the provided checker.

### End-to-End Workflow

```text
       WhatsApp Conversations
                 |
                 v
       Google Colab
    Data Exploration & Analysis
                 |
                 v
             PyCharm
       Modular Python Development
                 |
                 v
       Text & Context Processing
                 |
                 v
       Entity and Task Extraction
                 |
                 v
       Structured JSON Output
                 |
                 v
       Official Xpert Checker
                 |
                 v
       Evaluation & Improvements
```

## 04. Technical Architecture

The implementation follows a modular approach, separating different responsibilities into individual Python files.

| Module | Responsibility |
|---|---|
| `solution.py` | Main execution pipeline |
| `nlp_engine.py` | Text and language processing |
| `ml_engine.py` | ML-related processing |
| `context_engine.py` | Personal context analysis |
| `task_engine.py` | Task and open-loop extraction |
| `llm.py` | LLM-related functionality |
| `schema.json` | Output structure definition |
| `check.py` | Provided evaluation checker |

## 05. Technology Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Colab-F9AB00?logo=googlecolab&logoColor=black" />
  <img src="https://img.shields.io/badge/PyCharm-000000?logo=pycharm&logoColor=white" />
  <img src="https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white" />
</p>

- **Programming:** Python 3.11
- **Exploration:** Google Colab
- **Development:** PyCharm
- **Version Control:** Git & GitHub
- **Output:** Structured JSON
- **Evaluation:** Xpert-provided checker
- **Processing:** Rule-based extraction and modular text-processing logic

## 06. Project Structure

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
├── WRITEUP.md
├── README.md
└── .gitignore
```

*Local datasets, credentials, and generated output files are intentionally excluded from version control.*

## 07. Installation & Execution

### Prerequisites

- Python 3.11
- Git
- Xpert challenge starter kit
- Locally available challenge dataset

### Step 1 — Clone Repository

```bash
git clone https://github.com/Anuska111/Xpert_lab.git
cd Xpert_lab
```

### Step 2 — Create Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

### Step 3 — Install Dependencies

Install the dependencies required by the implementation in the Python environment.

### Step 4 — Add Dataset

Place the permitted local challenge dataset inside the expected `data/` directory.

The dataset is intentionally not included in this public repository.

### Step 5 — Execute Solution

```bash
python solution.py data/dev final_output.json
```

### Step 6 — Evaluate Output

```bash
python check.py data/dev final_output.json
```

## 08. Latest Evaluation Results

The solution was tested locally using the evaluation checker supplied with the Xpert challenge.

<p align="center">
  <strong>LOCAL DATA EVALUATION</strong>
  <br/>
  <img src="https://img.shields.io/badge/Score-19.1%20%2F%2056-2563EB?style=for-the-badge" />
</p>

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

### Latest Extraction Summary

| Extracted Information | Count |
|---|---:|
| People | 286 |
| Organisations | 5 |
| Chats | 138 |
| Goals | 0 |
| Open loops | 246 |
| Completed loops | 51 |
| Pending loops | 195 |

**Evaluation note:** Extraction counts are not equivalent to correct predictions. The checker evaluates the quality of the extracted information separately.

The organisers separately assess cost, write-up quality, and one-command execution. The data score above is not the final overall challenge score.

## 09. Current Limitations

The latest local run showed that the solution still has areas requiring improvement:

- Person and relationship identification need better accuracy.
- Organisation extraction requires stronger contextual understanding.
- Goal extraction did not produce results in the latest run.
- Open-loop extraction needs improved precision.
- LLM functionality was unavailable during the latest run, so the existing rule-based extraction was retained.

## 10. Future Improvements

- Improve entity recognition and relationship mapping.
- Develop stronger context-aware goal extraction.
- Distinguish completed commitments from pending tasks.
- Reduce false-positive open-loop detection.
- Improve contextual recommendations for where an assistant can help.
- Continue evaluation and refinement using the supplied checker.

## 11. AI-Assisted Development

AI tools were used as development assistants throughout the project for:

- Understanding challenge requirements.
- Exploring possible implementation approaches.
- Learning relevant NLP and context-processing concepts.
- Debugging Python and Git issues.
- Interpreting evaluation results.
- Improving project documentation.

Development records are maintained in the `ai-logs/` directory.

## 12. Data Privacy

- Challenge conversation data remains on the local machine.
- Dataset files are excluded from Git commits.
- Generated local outputs are excluded.
- API keys and environment secrets are not included in the repository.

## 13. Author

**Anuska Biswas**

GitHub: [@Anuska111](https://github.com/Anuska111) 

email:anuska.biswas.mec24@itbhu.ac.in

3rd Year

IIT(BHU)Varanasi

Project Repository: [Xpert_lab](https://github.com/Anuska111/Xpert_lab)

---

<p align="center">
  <strong>Built for the Xpert Winter Internship Challenge · 2026</strong>
  <br/>
  <sub>Learning • Experimenting • Building • Improving</sub>
</p>
