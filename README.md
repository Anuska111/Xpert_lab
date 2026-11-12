# XPERT | WhatsApp Personal Context Intelligence

### Understanding People, Organisations, Goals and Open Tasks from WhatsApp Conversations

## Overview

Xpert is a WhatsApp-based personal assistant. Before helping a user, it needs to understand their personal context: the people they interact with, their circles, associated organisations, goals, pending tasks and situations where assistance may be useful.

This project builds a personal context intelligence pipeline using two weeks of WhatsApp conversation data.

The system processes chat and message data and generates structured JSON output following the challenge schema.

## Problem Statement

The objective is to transform unstructured WhatsApp conversations into structured personal context:

- Identify people and their relationships.
- Infer relevant social circles.
- Identify organisations and associate chats with them.
- Extract personal goals from conversations.
- Detect open tasks, questions and commitments.
- Identify completed and pending tasks.
- Decide whether an assistant should assist, remind or leave the conversation alone.

## Project Architecture

The project is organised into modular Python components.

| File | Responsibility |
|---|---|
| `solution.py` | Main execution pipeline and output generation |
| `nlp_engine.py` | Text processing and language-based extraction |
| `ml_engine.py` | Machine-learning-related processing |
| `context_engine.py` | Personal context, people and organisation analysis |
| `task_engine.py` | Open-loop detection and task status analysis |
| `llm.py` | Optional OpenAI-compatible LLM integration |
| `schema.json` | Required output structure |
| `check.py` | Challenge output validation and evaluation |
| `run.sh` | One-command execution entry point |

## Technology Stack

- Python 3.11
- Pandas and NumPy
- NLP and rule-based text processing
- Machine Learning
- JSON and JSONL
- Optional OpenAI-compatible LLM integration
- Google Colab
- PyCharm
- Git and GitHub

## Project Workflow

1. Load WhatsApp chat and message data.
2. Process messages and extract useful conversational information.
3. Analyse people, circles and organisations.
4. Detect goals and open loops.
5. Identify task completion and pending actions.
6. Generate structured JSON output.
7. Validate the output using the provided challenge checker.

## Repository Structure

```text
Xpert_lab/
│
├── solution.py
├── nlp_engine.py
├── ml_engine.py
├── context_engine.py
├── task_engine.py
├── llm.py
├── schema.json
├── check.py
├── run.sh
├── Xpert_lab.ipynb
├── README.md
├── WRITEUP.md
│
└── ai-logs/
    ├── README.md
    ├── project-development.md
    ├── debugging.md
    └── evaluation-and-improvements.md
```

## Execution

Run the solution using:

```bash
./run.sh data/dev output.json
```

Validate the generated output:

```bash
python3 check.py data/dev output.json
```

The solution follows the supplied challenge schema and generates structured JSON.

## Development Evaluation

The solution was tested against the provided development dataset using the official checker.

**Latest recorded development score: 19.1 / 56 data points.**

| Evaluation Component | Score |
|---|---:|
| Circles | 2.9 / 12 |
| Organisations | 2.1 / 8 |
| Chats | 6.1 / 8 |
| Open loops found | 3.9 / 14 |
| Open loops closed right | 4.0 / 14 |
| Goals | Not labelled in this set |
| Where to help | Not labelled in this set |

The generated output passed the checker's structural validation.

These are development-set results, not the final hidden-test score.

## Limitations and Future Improvements

- Improve people-circle classification using stronger conversational context.
- Improve organisation identification and chat association.
- Extract implicit goals using contextual NLP.
- Reduce false positives in open-loop detection.
- Improve task completion matching and status classification.
- Improve assistant intervention decisions, particularly when it should stay out.
- Evaluate optional LLM-based extraction for better contextual understanding and cost efficiency.

## AI-Assisted Development

AI tools were used during development for understanding requirements, architecture planning, debugging, implementation guidance and evaluation analysis.

Development notes and AI usage summaries are available in the `ai-logs/` directory.

## Data Privacy

Original WhatsApp conversation data and private challenge datasets are not intended to be included in the public repository.

## Author

**Anuska Biswas**  
IIT (BHU), Varanasi  
Mechanical Engineering
anuska.biswas.mec24@itbhu.ac.in

---

*Built as part of the Xpert Winter Internship Build Challenge — November 2026.*
