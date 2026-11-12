# Xpert Personal Context Engine — Write-up

## 1. What I Focused On and Why

My goal was to build a system that can analyse WhatsApp conversations and extract useful personal context.

The system focuses on identifying people, circles, organisations, conversations, goals and open tasks. The main idea is to help an assistant understand what is happening in a person's life before deciding where it can provide useful support.

I prioritised extracting structured information from unstructured chat messages while keeping the output compatible with the provided schema.

## 2. My Approach

I implemented the solution in Python using a modular architecture.

- **solution.py:** Main entry point that processes the input directory and generates the final JSON output.
- **task_engine.py:** Uses message patterns, keywords and contextual rules to identify requests, commitments, follow-ups and completion messages.
- **context_engine.py:** Handles context extraction, including goals and open-loop information, with optional LLM support.
- **nlp_engine.py:** Supports text preprocessing and language-related processing.
- **ml_engine.py:** Contains the machine-learning-related processing components.
- **llm.py:** Handles the LLM integration.
- **check.py:** Validates and evaluates the generated output.

The pipeline reads the chat data, processes messages, groups information by conversation and extracts structured entities and tasks. It then generates a JSON output following the expected schema.

I used a combination of rule-based extraction, contextual matching and optional LLM-based processing.

## 3. Evaluation and Results

I evaluated my implementation using the provided development dataset and checker.

My latest local evaluation score was:

**19.1 / 56**

The system successfully processes 138 chats and identifies people, organisations, open tasks and completion candidates.

The evaluation also helped identify areas that need improvement, particularly circle classification, organisation extraction and open-task detection.

## 4. What It Costs

The local rule-based processing does not require an external API.

The LLM integration is optional and uses environment variables for configuration:

- LLM_BASE_URL
- LLM_API_KEY
- LLM_MODEL

When an LLM is configured, API usage and cost depend on the selected model and the number of tokens processed. I have not claimed a fixed API cost because it depends on the evaluation environment.

## 5. Where It Is Wrong and What I Would Improve

The current implementation has several limitations:

- Rule-based patterns can miss indirect requests and implied commitments.
- Short messages may be difficult to interpret without sufficient conversation history.
- People and organisation classification can produce incorrect predictions.
- Completion messages may not always match the correct earlier request.
- Goal extraction needs stronger contextual reasoning.
- Deciding when an assistant should intervene and when it should stay out requires more nuanced context.

With more development time, I would improve entity resolution, contextual task matching, goal extraction and intervention decisions. I would also evaluate the system on more diverse conversations and reduce false positives.

## 6. Final Note

This project was developed as a modular personal-context extraction pipeline. My focus was on building a working system, evaluating it with the supplied checker and identifying the limitations through experimentation.

The current score reflects the development-stage implementation, and there is significant scope for further improvement.