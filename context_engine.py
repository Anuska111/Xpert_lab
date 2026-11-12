
import os
import json
import re
from collections import defaultdict

try:
    from llm import chat as llm_chat
except ImportError:
    llm_chat = None


# --------------------------------------------------
# 1. Check whether LLM credentials are available
# --------------------------------------------------

def is_llm_available():
    return (
        llm_chat is not None
        and bool(os.getenv("LLM_BASE_URL"))
        and bool(os.getenv("LLM_API_KEY"))
        and bool(os.getenv("LLM_MODEL"))
    )


# --------------------------------------------------
# 2. Group messages by chat
# --------------------------------------------------

def group_messages(messages):
    grouped = defaultdict(list)

    for msg in messages:
        grouped[msg.get("chat_id")].append(msg)

    for chat_id in grouped:
        grouped[chat_id].sort(
            key=lambda x: x.get("ts", 0)
        )

    return grouped


# --------------------------------------------------
# 3. Prepare chat data for the LLM
# --------------------------------------------------

def prepare_chat(chat, messages):
    prepared_messages = []

    for msg in messages:
        if msg.get("kind") != "text":
            continue

        body = str(msg.get("body", "")).strip()

        if not body:
            continue

        prepared_messages.append({
            "id": msg.get("id"),
            "sender_id": msg.get("sender_id"),
            "sender_name": msg.get("sender_name"),
            "text": body[:1500]
        })

    return {
        "chat_id": chat.get("chat_id"),
        "chat_name": chat.get("name"),
        "is_group": chat.get("is_group", False),
        "participants": chat.get("participants", []),
        "messages": prepared_messages
    }


# --------------------------------------------------
# 4. Extract JSON from LLM response
# --------------------------------------------------

def parse_json_response(response):
    if isinstance(response, dict):
        return response

    response = str(response).strip()

    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response
    )

    response = re.sub(
        r"\s*```$",
        "",
        response
    )

    return json.loads(response)


# --------------------------------------------------
# 5. Validate extracted open loops
# --------------------------------------------------

def validate_loops(data, valid_message_ids, valid_chat_ids, valid_people):
    valid_types = {
        "commitment",
        "followup",
        "deadline",
        "question"
    }

    valid_statuses = {
        "open",
        "done",
        "dropped"
    }

    valid_actions = {
        "assist",
        "remind",
        "leave"
    }

    result = []

    loops = data.get("open_loops", [])

    if not isinstance(loops, list):
        return result

    for loop in loops:

        if not isinstance(loop, dict):
            continue

        source_msg = loop.get("source_msg")
        chat_id = loop.get("chat_id")
        owner = loop.get("owner")

        if source_msg not in valid_message_ids:
            continue

        if chat_id not in valid_chat_ids:
            continue

        if owner not in valid_people:
            continue

        if loop.get("type") not in valid_types:
            continue

        if loop.get("status") not in valid_statuses:
            continue

        title = str(loop.get("title", "")).strip()

        if not title:
            continue

        clean_loop = {
            "title": title[:250],
            "type": loop["type"],
            "owner": owner,
            "chat_id": chat_id,
            "source_msg": source_msg,
            "status": loop["status"],
            "due": loop.get("due"),
            "closed_by": loop.get("closed_by")
        }

        help_data = loop.get("help")

        if loop["status"] == "open":
            if isinstance(help_data, dict):
                action = help_data.get("action")

                if action not in valid_actions:
                    action = "leave"

                clean_loop["help"] = {
                    "action": action,
                    "next_step": help_data.get("next_step"),
                    "needs_yes": help_data.get("needs_yes"),
                    "remind_at": help_data.get("remind_at"),
                    "reason": help_data.get("reason")
                }
            else:
                clean_loop["help"] = {
                    "action": "leave",
                    "reason": "No clear next action identified."
                }

        result.append(clean_loop)

    return result


# --------------------------------------------------
# 6. LLM prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are an expert personal-context analyst.

You analyse WhatsApp conversations to identify genuine
real-world tasks, commitments, follow-ups and open loops.

Important rules:

1. Read the complete conversation context.
2. Do not treat every question or message as a task.
3. Combine related messages into one meaningful task.
4. Identify implied responsibilities where context supports them.
5. Detect whether a task was completed later.
6. Ignore greetings, casual conversations, emotional statements
   and ordinary information sharing unless a real action is needed.
7. Do not invent people, dates, tasks or message IDs.
8. Use only message IDs and chat IDs provided in the input.
9. Owner must be ME or a participant ID.
10. Distinguish open, done and dropped tasks.
11. Return only valid JSON.

Output format:

{
  "open_loops": [
    {
      "title": "Short meaningful task",
      "type": "followup",
      "owner": "ME",
      "chat_id": "C01",
      "source_msg": "M00001",
      "status": "open",
      "due": null,
      "closed_by": null,
      "help": {
        "action": "assist",
        "next_step": "Specific next action",
        "needs_yes": false,
        "remind_at": null,
        "reason": "Why this needs attention"
      }
    }
  ]
}

Allowed types:
commitment, followup, deadline, question

Allowed statuses:
open, done, dropped

Allowed help actions:
assist, remind, leave

For completed or dropped tasks, help must be null.
"""


# --------------------------------------------------
# 7. Process one batch of conversations
# --------------------------------------------------

def analyse_batch(batch):

    prompt = (
        "Analyse these WhatsApp conversations.\n"
        "Identify only genuine actionable tasks.\n\n"
        + json.dumps(batch, ensure_ascii=False)
    )

    response = llm_chat(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=3500,
        timeout=120
    )

    return parse_json_response(response)


# --------------------------------------------------
# 8. Main extraction function
# --------------------------------------------------

def extract_context_loops(messages, chats):

    if not is_llm_available():
        print("LLM unavailable. Context extraction skipped.")
        return []

    grouped = group_messages(messages)

    chat_lookup = {
        chat.get("chat_id"): chat
        for chat in chats
    }

    valid_message_ids = {
        msg.get("id")
        for msg in messages
        if msg.get("id")
    }

    valid_chat_ids = set(chat_lookup.keys())

    valid_people = {"ME"}

    for chat in chats:
        valid_people.update(
            chat.get("participants", [])
        )

    # Prepare individual conversations
    conversations = []

    for chat_id, chat_messages in grouped.items():

        chat = chat_lookup.get(chat_id)

        if not chat:
            continue

        prepared = prepare_chat(chat, chat_messages)

        if prepared["messages"]:
            conversations.append(prepared)

    # Batch conversations by approximate character budget
    batches = []
    current_batch = []
    current_size = 0

    for conversation in conversations:

        size = len(json.dumps(conversation, ensure_ascii=False))

        if current_batch and current_size + size > 18000:
            batches.append(current_batch)
            current_batch = []
            current_size = 0

        current_batch.append(conversation)
        current_size += size

    if current_batch:
        batches.append(current_batch)

    all_loops = []

    print("LLM batches:", len(batches))

    for index, batch in enumerate(batches, start=1):

        try:
            print(f"Processing batch {index}/{len(batches)}")

            response_data = analyse_batch(batch)

            batch_chat_ids = {
                item["chat_id"]
                for item in batch
            }

            batch_message_ids = {
                msg["id"]
                for item in batch
                for msg in item["messages"]
            }

            valid_batch_people = {"ME"}

            for item in batch:
                valid_batch_people.update(
                    item["participants"]
                )

            loops = validate_loops(
                response_data,
                batch_message_ids,
                batch_chat_ids,
                valid_batch_people
            )

            all_loops.extend(loops)

        except Exception as error:
            print(
                f"Batch {index} failed:",
                str(error)
            )

    # Remove exact duplicates
    unique = {}

    for loop in all_loops:
        key = (
            loop["chat_id"],
            loop["source_msg"],
            loop["title"].lower()
        )

        unique[key] = loop

    return list(unique.values())
# --------------------------------------------------
# 9. Goal extraction prompt
# --------------------------------------------------

GOAL_SYSTEM_PROMPT = """
You are an expert personal-context analyst.

Your task is to identify genuine goals of ME (Arjun) from
WhatsApp conversations.

A goal is a meaningful longer-term intention, desired outcome,
habit, milestone or experience.

IMPORTANT RULES:

1. Identify goals belonging to ME, not goals of other people.
2. Use the full conversation context to understand each message.
3. A goal is NOT the same as a one-time task, request, purchase,
   meeting, reminder or follow-up.
4. Do not treat casual words like want, learn, build, hope or plan
   as goals without meaningful supporting context.
5. Prefer explicit goals and repeated, clearly supported intentions.
6. Combine repeated references to the same goal into one goal.
7. Do not invent goals, evidence, deadlines or personal details.
8. Every goal must have at least one supporting message ID.
9. Evidence must contain only message IDs supplied in the input.
10. Return at most 10 strong goals. It is better to return fewer
    genuine goals than many weak guesses.
11. Return only valid JSON.

Allowed areas:
self, spouse, kids, parents, work, friends, experiences,
finances, health, home

Allowed types:
habit, milestone, experience

Allowed horizons:
3mo, 1yr, 3yr, 5yr

Output format:

{
  "goals": [
    {
      "title": "Build an AI product for consumer brands",
      "area": "work",
      "type": "milestone",
      "horizon": "1yr",
      "evidence": ["M00001", "M00002"]
    }
  ]
}

Horizon guidance:
- Use 3mo only when a short-term horizon is clearly supported.
- Use 1yr for a goal with a medium-term or unspecified horizon.
- Use 3yr or 5yr only when the conversation supports that timeframe.
- Never invent a deadline just to fill the field.
"""


# --------------------------------------------------
# 10. Validate extracted goals
# --------------------------------------------------

def validate_goals(data, valid_message_ids, me_message_ids):

    valid_areas = {
        "self", "spouse", "kids", "parents", "work",
        "friends", "experiences", "finances", "health", "home"
    }

    valid_types = {
        "habit", "milestone", "experience"
    }

    valid_horizons = {
        "3mo", "1yr", "3yr", "5yr"
    }

    result = []

    goals = data.get("goals", [])

    if not isinstance(goals, list):
        return result

    for goal in goals:

        if not isinstance(goal, dict):
            continue

        title = str(goal.get("title", "")).strip()
        area = goal.get("area")
        goal_type = goal.get("type")
        horizon = goal.get("horizon")

        if not title:
            continue

        if area not in valid_areas:
            continue

        if goal_type not in valid_types:
            continue

        if horizon not in valid_horizons:
            continue

        evidence = goal.get("evidence", [])

        if not isinstance(evidence, list):
            continue

        # Keep only real message IDs.
        evidence = list(dict.fromkeys(
            msg_id for msg_id in evidence
            if msg_id in valid_message_ids
        ))

        # At least one evidence message must be written by ME.
        if not evidence or not any(
            msg_id in me_message_ids for msg_id in evidence
        ):
            continue

        result.append({
            "title": title[:200],
            "area": area,
            "type": goal_type,
            "horizon": horizon,
            "evidence": evidence
        })

    return result


# --------------------------------------------------
# 11. Analyse one batch for goals
# --------------------------------------------------

def analyse_goals_batch(batch):

    prompt = (
        "Identify genuine longer-term goals belonging to ME "
        "from these WhatsApp conversations.\n"
        "Do not confuse ordinary tasks with goals.\n\n"
        + json.dumps(batch, ensure_ascii=False)
    )

    response = llm_chat(
        messages=[
            {
                "role": "system",
                "content": GOAL_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=2500,
        timeout=120
    )

    return parse_json_response(response)


# --------------------------------------------------
# 12. Main goal extraction function
# --------------------------------------------------

def extract_context_goals(messages, chats):

    if not is_llm_available():
        print("LLM unavailable. Goal extraction skipped.")
        return []

    grouped = group_messages(messages)

    chat_lookup = {
        chat.get("chat_id"): chat
        for chat in chats
    }

    valid_message_ids = {
        msg.get("id")
        for msg in messages
        if msg.get("id")
    }

    me_message_ids = {
        msg.get("id")
        for msg in messages
        if msg.get("sender_id") == "ME"
        and msg.get("id")
    }

    conversations = []

    for chat_id, chat_messages in grouped.items():

        chat = chat_lookup.get(chat_id)

        if not chat:
            continue

        prepared = prepare_chat(chat, chat_messages)

        if prepared["messages"]:
            conversations.append(prepared)

    # Keep batches within an approximate character budget.
    batches = []
    current_batch = []
    current_size = 0

    for conversation in conversations:

        size = len(json.dumps(conversation, ensure_ascii=False))

        if current_batch and current_size + size > 18000:
            batches.append(current_batch)
            current_batch = []
            current_size = 0

        current_batch.append(conversation)
        current_size += size

    if current_batch:
        batches.append(current_batch)

    all_goals = []

    print("Goal extraction batches:", len(batches))

    for index, batch in enumerate(batches, start=1):

        try:
            print(
                f"Analysing goals batch {index}/{len(batches)}"
            )

            response_data = analyse_goals_batch(batch)

            batch_message_ids = {
                msg["id"]
                for item in batch
                for msg in item["messages"]
            }

            batch_me_ids = {
                msg["id"]
                for item in batch
                for msg in item["messages"]
                if msg["sender_id"] == "ME"
            }

            goals = validate_goals(
                response_data,
                batch_message_ids,
                batch_me_ids
            )

            all_goals.extend(goals)

        except Exception as error:
            print(
                f"Goal batch {index} failed:",
                str(error)
            )

    # Merge repeated goals across different conversations.
    unique_goals = {}

    for goal in all_goals:

        normalized_title = re.sub(
            r"[^a-z0-9 ]",
            "",
            goal["title"].lower()
        )

        normalized_title = " ".join(
            normalized_title.split()
        )

        key = (
            goal["area"],
            normalized_title
        )

        if key not in unique_goals:
            unique_goals[key] = goal

        else:
            existing = unique_goals[key]

            existing["evidence"] = list(dict.fromkeys(
                existing["evidence"] + goal["evidence"]
            ))

    return list(unique_goals.values())[:10]
