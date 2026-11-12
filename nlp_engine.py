
import re
from collections import Counter, defaultdict


def clean_text(text):
    """
    Text ko clean aur normalize karta hai.
    English, Hindi aur Hinglish characters preserve karta hai.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()

    # URLs remove
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Email addresses remove
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        " ",
        text
    )

    # Extra whitespace remove
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """
    Unicode-aware tokenization.
    Hindi, English, numbers aur apostrophe words preserve karta hai.
    """
    text = clean_text(text)

    words = re.findall(
        r"[^\W_]+(?:['’][^\W_]+)*",
        text,
        flags=re.UNICODE
    )

    return words


def get_message_text(message):
    """Message dictionary se safe text return karta hai."""
    body = message.get("body", "")

    if not isinstance(body, str):
        return ""

    return clean_text(body)


def is_text_message(message):
    """Check karta hai ki message text type ka hai ya nahi."""
    return (
        message.get("kind") == "text"
        and bool(get_message_text(message))
    )


# KEYWORD MATCHING
def find_keywords(text, keywords):
    """Find relevant keywords inside a message."""
    words = set(tokenize(text))
    matched = []

    for keyword in keywords:
        keyword_words = set(tokenize(keyword))

        if keyword_words and keyword_words.issubset(words):
            matched.append(keyword)

    return matched


# GROUP MESSAGES BY CHAT
def group_messages_by_chat(messages):
    grouped = defaultdict(list)

    for message in messages:
        chat_id = message.get("chat_id")

        if chat_id:
            grouped[chat_id].append(message)

    return dict(grouped)


# GROUP MESSAGES BY SENDER
def group_messages_by_sender(messages):
    grouped = defaultdict(list)

    for message in messages:
        sender_id = message.get("sender_id")

        if sender_id:
            grouped[sender_id].append(message)

    return dict(grouped)


# CHAT ACTIVITY FEATURES
def get_chat_features(messages):
    grouped = group_messages_by_chat(messages)
    features = {}

    for chat_id, chat_messages in grouped.items():

        senders = Counter(
            message.get("sender_id", "UNKNOWN")
            for message in chat_messages
        )

        text_messages = [
            message for message in chat_messages
            if is_text_message(message)
        ]

        features[chat_id] = {
            "total_messages": len(chat_messages),
            "unique_senders": len(senders),
            "sender_counts": dict(senders),
            "text_messages": len(text_messages),
            "sample_messages": [
                message.get("body", "")
                for message in text_messages[:10]
            ]
        }

    return features


# MESSAGE EVIDENCE
def get_message_evidence(messages, keywords):
    evidence = []

    for message in messages:
        body = message.get("body", "")
        matched = find_keywords(body, keywords)

        if matched:
            evidence.append({
                "message_id": message.get("id"),
                "chat_id": message.get("chat_id"),
                "sender_id": message.get("sender_id"),
                "text": body,
                "matched_keywords": matched
            })

    return evidence


# SENDER ACTIVITY
def get_sender_activity(messages):
    activity = Counter()

    for message in messages:
        sender = message.get("sender_id")

        if sender:
            activity[sender] += 1

    return dict(activity)
