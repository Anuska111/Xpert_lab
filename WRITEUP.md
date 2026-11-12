# Xpert Cold Start — Technical Write-up

## 1. What I Focused On, and Why

My objective was to build a working pipeline that converts WhatsApp conversations into structured personal context.

I focused on three major areas:

- **People, organisations and chats:** Identifying relationships and connecting conversations to the appropriate people or organisations.
- **Open loops:** Detecting requests, commitments, follow-ups and deadlines, and tracking whether they were completed.
- **Goals:** Identifying longer-term intentions rather than treating every short-term task as a goal.

I prioritised building a complete, schema-valid pipeline first. Chat association and task extraction were particularly important because they provide the foundation for understanding who is involved and what still needs attention.

I also aimed to keep the solution modular so that individual components could be improved independently.

## 2. My Approach

The implementation uses Python with a modular architecture.

**Data processing:** The pipeline loads `chats.jsonl`, `messages.jsonl` and `seed.json`. Messages are grouped by chat and processed chronologically.

**People and circles:** Relationship and activity signals are derived using keyword patterns, chat names, participant information and message activity.

**Organisations and chats:** The implementation uses organisation-name matching and participant associations to connect chats to organisations or individual people.

**Goals:** The current implementation uses explicit goal-related expressions as a rule-based fallback. An optional LLM-based extraction path is also present, with validation of evidence message IDs.

**Open loops:** Rule-based patterns classify messages as requests, commitments, questions, deadlines or follow-ups. Completion phrases are matched against earlier requests to infer task status.

**Where to help:** The current rule-based implementation assigns assistance or reminder suggestions based on task type. Context-sensitive decisions about when to leave a conversation alone remain an area for improvement.

The project was initially explored using Google Colab and then organised into a modular local implementation in PyCharm.

The final output is generated as structured JSON and evaluated using the checker supplied with the challenge.

## 3. What It Costs

The latest local evaluation used the rule-based fallback because the required LLM environment variables were unavailable.

Therefore:

- Model used in the latest local run: None.
- LLM API calls in that run: None.
- Model API cost for that local run: $0 per 1,000 messages.
- Optional LLM client: `llm.py`, which supports an OpenAI-compatible API through environment variables.

The repository contains an optional LLM-based extraction path, but I have not completed a model-backed run or measured its token usage. Consequently, I cannot claim a measured cost for that path or provide a verified model-specific price.

## 4. Where It Is Wrong

The latest development-set evaluation scored **19.1 / 56**.

The results indicate the following weaknesses:

- **Circles (2.9 / 12):** Keyword-based relationship inference can confuse colleagues, friends, relatives and staff, especially when the relationship is only implied by conversation context.
- **Organisations (2.1 / 8):** Some organisation associations rely on specific names and chat-name patterns. This is fragile when names change or a group has an ambiguous title.
- **Chats (6.1 / 8):** Chat association is the strongest component, but participant-frequency assumptions can still assign group conversations incorrectly.
- **Open loops found (3.9 / 14):** Broad request and commitment patterns can detect ordinary messages as tasks, while indirect commitments and contextual follow-ups may be missed.
- **Open loops closed correctly (4.0 / 14):** Completion matching based on phrases and message proximity can incorrectly mark a task as completed or leave a completed task open.
- **Goals:** The latest local run produced zero goals. The fallback recognises only a small set of explicit expressions, so goals expressed indirectly are likely to be missed.
- **Where to help:** The current rules do not sufficiently distinguish between situations requiring assistance, a reminder, or no intervention. In particular, the `leave` decision needs stronger contextual reasoning.

Goals and Where-to-help were not labelled in the local development evaluation, so their accuracy cannot be measured from this score.

These results are from the development set and should not be treated as a prediction of hidden-set performance.

## Conclusion

This project gave me practical experience in processing conversational data, designing modular extraction pipelines, validating structured outputs and analysing evaluation results.

The current implementation establishes a working baseline, while the evaluation highlights where stronger contextual reasoning, better generalisation and more conservative assistance decisions are needed.
