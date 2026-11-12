# Xpert Project – AI Development Log

**Date:** 12 November 2026  
**AI Tool:** ChatGPT  
**Project:** Xpert WhatsApp Personal Context Analysis

## 1. Project Understanding

**Prompt / Discussion:**  
I discussed the Xpert internship challenge and asked how to build a system that understands WhatsApp conversations, identifies people and organisations, extracts goals and open tasks, and determines where an assistant can help.

**Outcome:**  
We broke the challenge into smaller components: people and circles, organisations, chats, goals, open loops, and assistance opportunities.

## 2. Development Approach

**Prompt / Discussion:**  
I asked for an alternative to using Google Colab and wanted to implement the complete solution directly in PyCharm.

**Outcome:**  
We chose a modular Python implementation with separate files for NLP processing, ML logic, task extraction, context analysis, and the main solution pipeline.

## 3. Debugging and Evaluation

**Prompt / Discussion:**  
I discussed Python environment setup, project paths, running the solution, and interpreting checker results.

**Outcome:**  
We resolved setup and Git issues and evaluated the generated output using the provided checker.

## 4. Evaluation and Improvements

**Latest local evaluation:** 19.1 / 56

The evaluation showed that chat extraction was comparatively stronger, while people, organisations, and open-loop extraction needed improvement.

**Next improvements:**  
- Improve person and relationship identification.
- Improve goal and open-task extraction.
- Reduce incorrect task detections.
- Improve where-to-help recommendations.

## 5. AI Usage

ChatGPT was used for understanding requirements, planning the architecture, Python debugging, interpreting evaluation results, and documenting development decisions.

The implementation and final evaluation were performed in the local PyCharm project.