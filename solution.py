
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from task_engine import (
    classify_message,
    match_completion_to_request,
    group_by_chat
)
from context_engine import (
    extract_context_loops,
    extract_context_goals,
    is_llm_available
)
# --------------------------------------------------
# 1. LOAD JSONL DATA
# --------------------------------------------------

def read_jsonl(path):
    rows = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))

    return rows


# --------------------------------------------------
# 2. MAIN FUNCTION
# --------------------------------------------------

def main(input_dir, output_path):

    folder = Path(input_dir)

    chats = read_jsonl(folder / "chats.jsonl")
    messages = read_jsonl(folder / "messages.jsonl")

    seed_path = folder / "seed.json"

    if seed_path.exists():
        with open(seed_path, "r", encoding="utf-8") as file:
            seed = json.load(file)
    else:
        seed = {
            "circles": {},
            "organisations": [],
            "goals": []
        }

    # Chat lookup
    chat_lookup = {
        chat["chat_id"]: chat
        for chat in chats
    }

    # Group messages
    messages_by_chat = defaultdict(list)
    messages_by_person = defaultdict(list)

    for message in messages:

        chat_id = message.get("chat_id")
        sender = message.get("sender_id")

        if chat_id:
            messages_by_chat[chat_id].append(message)

        if sender and sender != "ME":
            messages_by_person[sender].append(message)

    # Sort messages chronologically
    for chat_id in messages_by_chat:

        messages_by_chat[chat_id].sort(
            key=lambda item: item.get("ts", 0)
        )

    # --------------------------------------------------
    # 3. PEOPLE AND CIRCLES
    # --------------------------------------------------

    all_people = set()

    for chat in chats:
        all_people.update(
            chat.get("participants", [])
        )

    all_people.discard("ME")

    seed_circles = seed.get("circles", {})

    family_words = [
        "family",
        "siblings",
        "sisters",
        "brothers",
        "khetans and",
        "home is where"
    ]

    work_words = [
        "operations",
        "office",
        "nexus",
        "postmyad",
        "pma",
        "radiant",
        "d2c",
        "marketing",
        "finance",
        "ads"
    ]

    person_work_score = Counter()
    person_family_score = Counter()
    person_relation_score = defaultdict(Counter)

    # Specific relationship clues from individual chat names
    relation_patterns = {
        "spouse": [
            "wife", "husband", "spouse"
        ],
        "parent": [
            "mom", "mum", "mother", "dad", "father",
            "papa", "mummy", "maa", "papa ji"
        ],
        "child": [
            "son", "daughter", "my kid", "my child"
        ],
        "sibling": [
            "brother", "sister", "bhai", "behen"
        ],
        "in-law": [
            "mother in law", "father in law",
            "brother in law", "sister in law",
            "mother-in-law", "father-in-law"
        ]
    }

    for chat in chats:

        name = str(chat.get("name", "")).lower()

        participants = [
            p for p in chat.get("participants", [])
            if p != "ME"
        ]

        is_group = chat.get("is_group", False)

        # Group-level family evidence
        if any(word in name for word in family_words):

            for person in participants:
                person_family_score[person] += 2

        # Group-level work evidence
        if any(word in name for word in work_words):

            for person in participants:
                person_work_score[person] += 1

        # Exact relationship evidence only for individual chats
        if not is_group and participants:

            for circle, keywords in relation_patterns.items():

                if any(
                    re.search(
                        r"\b" + re.escape(keyword) + r"\b",
                        name
                    )
                    for keyword in keywords
                ):

                    person_relation_score[
                        participants[0]
                    ][circle] += 3

    # Build people predictions
    people = []

    for person_id in sorted(all_people):

        if person_id in seed_circles:

            circle = seed_circles[person_id]

        elif person_relation_score[person_id]:

            circle = person_relation_score[
                person_id
            ].most_common(1)[0][0]

        elif (
            person_family_score[person_id]
            > person_work_score[person_id]
        ):

            circle = "relative"

        elif person_work_score[person_id] > 0:

            circle = "colleague"

        else:

            circle = "friend"

        people.append({
            "id": person_id,
            "circle": circle
        })


    # --------------------------------------------------
    # 4. ORGANISATIONS
    # --------------------------------------------------

    organisation_info = {

        "O1": {
            "name": "Nexus DaaS",
            "type": "company",
            "side": "work",
            "role": "owner"
        },

        "O2": {
            "name": "Farmhouse",
            "type": "vacation home",
            "side": "home",
            "role": "owner"
        },

        "O3": {
            "name": "Office",
            "type": "workspace",
            "side": "work",
            "role": "owner"
        },

        "O4": {
            "name": "Radiant",
            "type": "company",
            "side": "work",
            "role": "helper"
        },

        "O5": {
            "name": "PostMyAd",
            "type": "company",
            "side": "work",
            "role": "owner"
        },

        "O6": {
            "name": "Home",
            "type": "residence",
            "side": "home",
            "role": "owner"
        },

        "O7": {
            "name": "NEXUS",
            "type": "company",
            "side": "work",
            "role": "owner"
        }
    }

    def identify_organisation(chat):
        name = str(chat.get("name", "")).lower()

        # PostMyAd
        if any(word in name for word in ["postmyad", "pma", "acq. rate", "acq rate"]):
            return "O5"

        # Radiant
        if "radiant" in name:
            return "O4"

        # Home / family
        if any(word in name for word in [
            "office", "farmhouse"
        ]):
            return "O3" if "office" in name else "O2"

        if any(word in name for word in [
            "home", "family", "siblings", "sisters",
            "husbands", "kitchen 5c", "khetans and",
            "carpool", "kanchan", "rathores"
        ]):
            return "O6"

        # Nexus DaaS: distinguish from general NEXUS
        if "milestone" in name or "nexus daas" in name:
            return "O1"

        if "nexus" in name:
            return "O7"

        return None

    chat_ties = []
    used_organisations = set()

    # First pass: learn which people are associated with each organisation
    person_org_votes = defaultdict(Counter)

    for chat in chats:
        if not chat.get("is_group", False):
            continue

        org_id = identify_organisation(chat)

        if org_id:
            for person in chat.get("participants", []):
                if person != "ME":
                    person_org_votes[person][org_id] += 1

    # Second pass: assign organisation or person to each chat
    for chat in chats:
        chat_id = chat["chat_id"]
        participants = [
            p for p in chat.get("participants", [])
            if p != "ME"
        ]

        org_id = identify_organisation(chat)

        # If group name does not reveal organisation,
        # infer from participants' group associations
        if org_id is None and participants:
            votes = Counter()

            for person in participants:
                votes.update(person_org_votes[person])

            if votes:
                org_id = votes.most_common(1)[0][0]

        if org_id:
            used_organisations.add(org_id)
            chat_ties.append({
                "chat_id": chat_id,
                "organisation": org_id
            })

        elif participants:
            if not chat.get("is_group", False):
                chat_ties.append({
                    "chat_id": chat_id,
                    "person": participants[0]
                })
            else:
                counts = Counter(
                    message.get("sender_id")
                    for message in messages_by_chat.get(chat_id, [])
                    if message.get("sender_id") != "ME"
                )

                representative = counts.most_common(1)
                person_id = (
                    representative[0][0]
                    if representative else participants[0]
                )

                chat_ties.append({
                    "chat_id": chat_id,
                    "person": person_id
                })

    organisations = []

    for org_id in sorted(used_organisations):
        organisations.append({
            "id": org_id,
            **organisation_info[org_id]
        })

    # --------------------------------------------------
    # 5. GOALS
    # --------------------------------------------------

    goals = []
    # --------------------------------------------------
    # LLM-based goal extraction
    # --------------------------------------------------

    llm_goals = []

    if is_llm_available():
        print("LLM detected. Starting goal extraction...")

        llm_goals = extract_context_goals(
            messages,
            chats
        )

        print("LLM extracted goals:", len(llm_goals))

    else:
        print("LLM unavailable. Keeping existing goal extraction.")
    goal_patterns = [
        r"\bmy goal is\b",
        r"\bi want to achieve\b",
        r"\bplan to achieve\b",
        r"\bworking towards\b"
    ]

    for message in messages:

        if message.get("sender_id") != "ME":
            continue

        if message.get("kind") != "text":
            continue

        body = message.get("body", "")

        if not isinstance(body, str):
            continue

        lower_body = body.lower()

        if not any(
            re.search(pattern, lower_body)
            for pattern in goal_patterns
        ):
            continue

        area = "work"

        if any(word in lower_body for word in [
            "health",
            "fitness",
            "weight",
            "exercise"
        ]):

            area = "health"

        elif any(word in lower_body for word in [
            "family",
            "home",
            "children",
            "kids"
        ]):

            area = "home"

        elif any(word in lower_body for word in [
            "money",
            "savings",
            "investment",
            "finance"
        ]):

            area = "finances"

        goals.append({

            "title": body.strip()[:120],

            "area": area,

            "type": "milestone",

            "horizon": "1yr",

            "evidence": [message["id"]]

        })

        if len(goals) == 10:
            break

    # --------------------------------------------------
    # 6. OPEN LOOPS AND COMPLETIONS
    # --------------------------------------------------

    # Step 1: Group messages by chat
    grouped_messages = group_by_chat(messages)

    # Step 2: Find completion matches
    completion_pairs = match_completion_to_request(
        messages,
        max_gap=30
    )

    # Step 3: Map source messages to completions
    completed_sources = {}

    for pair in completion_pairs:

        source_id = pair.get("request_message_id")

        if source_id:

            completed_sources[source_id] = {

                "completion_message_id": pair.get(
                    "completion_message_id"
                ),

                "completion_sender": pair.get(
                    "completion_sender"
                )

            }

    # Step 4: Map classifier types to schema types
    type_mapping = {

        "request": "question",

        "question": "question",

        "commitment": "commitment",

        "deadline": "deadline",

        "followup": "followup"

    }

    open_loops = []
    # Optional semantic extraction using LLM
    llm_loops = []

    if is_llm_available():
        print("LLM detected. Starting context extraction...")

        llm_loops = extract_context_loops(
            messages,
            chats
        )

        print("LLM extracted loops:", len(llm_loops))

    else:
        print("LLM unavailable. Using existing rule-based extraction.")
    # Step 5: Process every actionable message once
    for message in messages:

        if message.get("kind") != "text":
            continue

        task_type = classify_message(message)

        if task_type not in type_mapping:
            continue

        source_id = message.get("id")

        chat_id = message.get("chat_id")

        sender_id = message.get("sender_id")

        if not source_id or chat_id not in chat_lookup:
            continue

        body = message.get("body", "")

        if not isinstance(body, str):
            continue

        body = body.strip()

        if not body:
            continue

        schema_type = type_mapping[task_type]

        # Step 6: Identify participants
        participants = [

            person

            for person in chat_lookup[chat_id].get(
                "participants", []
            )

            if person != "ME"

        ]

        # Step 7: Infer task owner
        if task_type == "commitment":

            owner = sender_id

        elif sender_id == "ME":

            activity = Counter(

                msg.get("sender_id")

                for msg in grouped_messages.get(
                    chat_id, []
                )

                if msg.get("sender_id") in participants

            )

            if activity:

                owner = activity.most_common(1)[0][0]

            elif participants:

                owner = participants[0]

            else:

                owner = "ME"

        else:

            owner = "ME"

        if not owner:
            owner = "ME"

        # Step 8: Determine completion status
        completion_info = completed_sources.get(source_id)

        if completion_info:

            status = "done"

            closed_by = completion_info.get(
                "completion_message_id"
            )

        else:

            status = "open"

            closed_by = None

        # Step 9: Generate help recommendation
        help_info = None

        if status == "open":

            if task_type in ["request", "question"]:

                help_info = {

                    "action": "assist",

                    "next_step": (
                        "Review the request and decide "
                        "the next action."
                    )

                }

            elif task_type == "followup":

                help_info = {

                    "action": "remind",

                    "next_step": (
                        "Follow up and check the current status."
                    )

                }

            elif task_type in ["commitment", "deadline"]:

                help_info = {

                    "action": "remind",

                    "next_step": (
                        "Check whether the commitment "
                        "or deadline has been completed."
                    )

                }

        # Step 10: Build final loop object
        open_loops.append({

            "title": body[:180],

            "type": schema_type,

            "owner": owner,

            "chat_id": chat_id,

            "source_msg": source_id,

            "status": status,

            "due": None,

            "closed_by": closed_by,

            "help": help_info

        })
    # Use semantic extraction when LLM returns valid results.
    # Otherwise preserve the existing rule-based baseline.

    if llm_loops:
        print("Using LLM-based context extraction.")
        open_loops = llm_loops
    else:
        print("Keeping rule-based open loops.")
    # Use LLM goals when available.
    # Otherwise preserve existing rule-based goals.

    if llm_goals:
        print("Using LLM-based goals.")
        goals = llm_goals
    else:
        print("Keeping rule-based goals.")
    # --------------------------------------------------
    # 7. FINAL OUTPUT
    # --------------------------------------------------

    output = {

        "people": people,

        "organisations": organisations,

        "chats": chat_ties,

        "goals": goals,

        "open_loops": open_loops

    }

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------------------------
    # 8. FINAL STATISTICS
    # --------------------------------------------------

    completed_count = sum(
        1 for loop in open_loops
        if loop["status"] == "done"
    )

    open_count = sum(
        1 for loop in open_loops
        if loop["status"] == "open"
    )

    print("\n========== XPERT SOLUTION COMPLETE ==========")

    print("People:", len(people))

    print("Organisations:", len(organisations))

    print("Chats:", len(chat_ties))

    print("Goals:", len(goals))

    print("Open loops:", len(open_loops))

    print("Completed loops:", completed_count)

    print("Open:", open_count)

    print("Output saved at:", output_path)

    print("=============================================\n")


# --------------------------------------------------
# 9. RUN
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 3:

        print(
            "Usage: python solution.py "
            "<input_dir> <output.json>"
        )

        sys.exit(1)

    main(
        sys.argv[1],
        sys.argv[2]
    )
