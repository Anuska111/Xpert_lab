

import re
from collections import Counter, defaultdict

from nlp_engine import (
    clean_text,
    tokenize,
    get_message_text,
    is_text_message
)


# -----------------------------------
# 1. RELATIONSHIP KEYWORDS
# -----------------------------------

RELATIONSHIP_KEYWORDS = {
    "spouse": [
        "wife", "husband", "spouse"
    ],

    "child": [
        "son", "daughter", "my child", "my kid"
    ],

    "parent": [
        "mom", "mother", "dad", "father",
        "parents", "mummy", "papa"
    ],

    "in-law": [
        "mother in law", "father in law",
        "brother in law", "sister in law",
        "in laws"
    ],

    "sibling": [
        "brother", "sister", "siblings"
    ],

    "relative": [
        "uncle", "aunt", "cousin",
        "nephew", "niece", "relative"
    ],

    "friend": [
        "friend", "buddy", "bro", "mate",
        "party", "hangout", "birthday",
        "movie", "dinner", "trip"
    ],

    "colleague": [
        "colleague", "coworker", "manager",
        "office", "meeting", "team"
    ],

    "client": [
        "client", "customer"
    ],

    "vendor": [
        "vendor", "supplier", "invoice",
        "payment", "delivery", "quotation"
    ],

    "partner": [
        "business partner", "project partner"
    ],

    "staff": [
        "employee", "staff", "helper",
        "driver", "assistant"
    ]
}


# -----------------------------------
# 2. TASK KEYWORDS
# -----------------------------------

TASK_KEYWORDS = {
    "commitment": [
        "i will", "i'll", "i can do",
        "i will send", "i'll send",
        "will share", "i will share",
        "i will check", "i'll check",
        "let me check", "i will arrange",
        "i'll arrange", "i will update"
    ],

    "followup": [
        "follow up", "update me",
        "get back", "check with",
        "remind me", "let me know",
        "any update", "get back to me"
    ],

    "deadline": [
        "deadline", "due date",
        "by tomorrow", "by monday",
        "before friday", "urgent",
        "by today", "by evening",
        "by next week"
    ],

    "question": [
        "can you", "could you",
        "please confirm", "what happened",
        "any update", "when will",
        "have you", "did you"
    ]
}


# -----------------------------------
# 3. HELPER: COUNT PHRASES
# -----------------------------------

def count_phrase(text, phrase):

    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return len(re.findall(pattern, text))


# -----------------------------------
# 4. GROUP MESSAGES BY PERSON
# -----------------------------------

def group_by_person(messages):

    grouped = defaultdict(list)

    for message in messages:

        sender = message.get("sender_id")

        if sender and sender != "ME":
            grouped[sender].append(message)

    return dict(grouped)


# -----------------------------------
# 5. EXTRACT PERSON FEATURES
# -----------------------------------

def extract_person_features(messages):

    grouped = group_by_person(messages)

    results = {}

    for person_id, person_messages in grouped.items():

        text_messages = [
            m for m in person_messages
            if is_text_message(m)
        ]

        all_text = " ".join(
            get_message_text(m)
            for m in text_messages
        )

        tokens = tokenize(all_text)

        relationship_signals = {}

        for category, keywords in RELATIONSHIP_KEYWORDS.items():

            score = 0

            for keyword in keywords:
                score += count_phrase(all_text, keyword)

            relationship_signals[category] = score

        results[person_id] = {

            "message_count": len(person_messages),

            "text_message_count": len(text_messages),

            "word_count": len(tokens),

            "unique_words": len(set(tokens)),

            "relationship_signals": relationship_signals
        }

    return results


# -----------------------------------
# 6. EXTRACT TASK CANDIDATES
# -----------------------------------

def extract_task_candidates(messages):

    candidates = []

    for message in messages:

        if not is_text_message(message):
            continue

        body = get_message_text(message)

        matched_types = []

        for task_type, keywords in TASK_KEYWORDS.items():

            for keyword in keywords:

                if count_phrase(body, keyword) > 0:

                    matched_types.append(task_type)
                    break

        # Question mark alone is not sufficient.
        question_words = [
            "who", "what", "when", "where",
            "why", "how", "which"
        ]

        if (
            "?" in body
            and "question" not in matched_types
            and any(
                re.search(
                    r"(?<!\w)" + word + r"(?!\w)",
                    body
                )
                for word in question_words
            )
        ):
            matched_types.append("question")

        if matched_types:

            candidates.append({

                "message_id": message.get("id"),

                "chat_id": message.get("chat_id"),

                "sender_id": message.get("sender_id"),

                "text": message.get("body", ""),

                "candidate_types": matched_types
            })

    return candidates


# -----------------------------------
# 7. EXTRACT CHAT FEATURES
# -----------------------------------

def extract_chat_features(messages):

    grouped = defaultdict(list)

    for message in messages:

        chat_id = message.get("chat_id")

        if chat_id:
            grouped[chat_id].append(message)

    results = {}

    for chat_id, chat_messages in grouped.items():

        sender_counts = Counter(
            m.get("sender_id")
            for m in chat_messages
            if m.get("sender_id")
        )

        text_count = sum(
            1 for m in chat_messages
            if is_text_message(m)
        )

        results[chat_id] = {

            "message_count": len(chat_messages),

            "text_message_count": text_count,

            "sender_count": len(sender_counts),

            "me_messages": sender_counts.get("ME", 0),

            "other_messages": sum(
                count
                for sender, count in sender_counts.items()
                if sender != "ME"
            )
        }

    return results
