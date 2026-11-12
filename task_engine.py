
import re
from collections import defaultdict

from nlp_engine import clean_text, is_text_message


# ==========================================
# 1. NON-TASK MESSAGES
# ==========================================

NON_TASK_PATTERNS = [
    r"\bi will join\b",
    r"\bi'll join\b",
    r"\bwill join\b",
    r"\bi will attend\b",
    r"\bi'll attend\b",
    r"\bi will be there\b",
    r"\bi am joining\b",
    r"\bi'm joining\b",
    r"\bsee you there\b",
    r"\bthanks for sharing\b",
    r"\bthank you for sharing\b",
]


# ==========================================
# 2. COMPLETION PATTERNS
# ==========================================

COMPLETION_PATTERNS = [
    r"^\s*(done|completed|finished|fixed|sent|shared|resolved|submitted|uploaded|paid|booked|ordered|purchased|delivered)\s*[.! ]*$",

    r"\bi have sent\b",
    r"\bi've sent\b",
    r"\bi have shared\b",
    r"\bi've shared\b",
    r"\bi have completed\b",
    r"\bi've completed\b",
    r"\bi have paid\b",
    r"\bi've paid\b",
    r"\bi have booked\b",
    r"\bi've booked\b",
    r"\bi have ordered\b",
    r"\bi have uploaded\b",
    r"\bi have submitted\b",

    r"\btask is completed\b",
    r"\bwork is done\b",
    r"\bissue is fixed\b",
    r"\bit is done\b",
    r"\bits done\b",
    r"\ball done\b",
    r"\bhas been completed\b",
    r"\bhas been sent\b",
    r"\bhas been paid\b",
    r"\bhas been booked\b",
    r"\bhas been ordered\b",
    r"\bgot it done\b",
    r"\bsent it\b",
    r"\bpaid it\b",
    r"\bbooked it\b",
    r"\bordered it\b",
]


# ==========================================
# 3. DEADLINE PATTERNS
# ==========================================

DEADLINE_PATTERNS = [
    r"\bdeadline\b",
    r"\bdue date\b",
    r"\bby tomorrow\b",
    r"\bby today\b",
    r"\bby monday\b",
    r"\bby tuesday\b",
    r"\bby wednesday\b",
    r"\bby thursday\b",
    r"\bby friday\b",
    r"\bbefore friday\b",
    r"\bby evening\b",
    r"\bby next week\b",
    r"\bas soon as possible\b",
    r"\basap\b",
    r"\btomorrow at \d",
    r"\btoday at \d",
    r"\bby \d{1,2}(?:st|nd|rd|th)?\b",
    r"\bwithin \d+\s+(?:hours?|days?|weeks?)\b",
    r"\bno later than\b",
]


# ==========================================
# 4. COMMITMENT PATTERNS
# ==========================================

COMMITMENT_PATTERNS = [

    r"\b(?:i will|i'll|we will|we'll)\s+"
    r"(?:send|share|update|confirm|check|arrange|order|pay|book|call|ask|buy|get|prepare|complete|finish|speak|talk|revert|purchase|deliver|submit|upload|reimburse|transfer)\b",

    r"\bwill\s+(?:send|share|update|confirm|check|arrange|order|pay|book|call|ask|buy|get|prepare|complete|finish|speak|talk|revert|purchase|deliver|submit|upload|reimburse|transfer)\b",

    r"\b(?:i can|i'll|i will)\s+(?:take care of|handle|look into|follow up|coordinate)\b",

    r"\blet me\s+(?:check|confirm|verify|speak|ask|call|arrange|book|find|send|share|update|prepare|coordinate)\b",

    r"\b(?:i am going to|i'm going to)\s+"
    r"(?:send|share|call|ask|buy|order|book|arrange|prepare|complete|finish|pay|check|confirm)\b",

    r"\bi promise to\b",
    r"\bi(?:'|’)ll\s+buy\b",
    r"\bi\s+will\s+buy\b",
    r"\bi(?:'|’)ll\s+order\b",
    r"\bi\s+will\s+order\b",
    r"\bill\s+buy\b",

    r"\b(?:we'll|we will)\s+(?:connect|discuss|sit|meet|take)\b",
    r"\b(?:let's|lets)\s+(?:discuss|fix|arrange|send|connect|do)\b",
    r"\bwe\s+discuss\s+this\b",
    r"\bwe\s+can\s+sit\b",
    r"\bgo ahead and\s+(?:order|buy|book|purchase)\b",
    r"\bneed to discuss\b",
    r"\binvite to be made\b",
    r"\bwill incorporate\b",
    r"\breverting tomorrow\b",
    r"\bi will reach\b",
    r"\bi'll reach\b",
]


# ==========================================
# 5. FOLLOW-UP PATTERNS
# ==========================================

FOLLOWUP_PATTERNS = [
    r"\bany update\b",
    r"\bjust following up\b",
    r"\bfollowing up\b",
    r"\bremind me\b",
    r"\bplease remind\b",
    r"\blet me know when\b",
    r"\blet me know once\b",
    r"\bkeep me posted\b",
    r"\bget back to me\b",
    r"\bwaiting for\b",
    r"\bstill waiting\b",
    r"\bchecking on\b",
    r"\bstatus of\b",
    r"\bwhen can we expect\b",
    r"\bwhen will you\b",
    r"\blet's send a save the date\b",
    r"\bwhich date to book\b",
    r"\bneed your help to update\b",
    r"\bneed the .* to raise the\b",
    r"\bmeasurements required for quotation\b",
    r"\bstill not delivered\b",
    r"\bconfirm.*was executed\b",
    r"\bplease update me\b",
    r"\bany progress\b",
    r"\bawaiting your response\b",
    r"\bawaiting confirmation\b",
]


# ==========================================
# 6. QUESTION PATTERNS
# ==========================================

QUESTION_PATTERNS = [
    r"^\s*(?:should i|shall i|should we)\b",

    r"^\s*(?:can we|could we)\s+"
    r"(?:meet|discuss|schedule|arrange|have|connect|speak|talk|call)\b",

    r"^\s*(?:would it be possible|is it possible)\b",

    r"^\s*(?:when can|when will|where can|where should)\b",

    r"^\s*do we need to\b",

    r"\bcan we have a meeting\b",
    r"\bpossible to get\b",
    r"\bwhen are you available\b",
    r"\bwhat time works\b",
    r"\bwhat would work\b",
    r"\bany idea when\b",
    r"\bcan we pls have\b",
    r"\bcan we please have\b",
    r"\bany plans for\b",
    r"\bshall we zoom\b",
    r"\byou both coming for\b",
    r"\bright\?\s*$",
    r"\blets fix a call\b",
    r"\blet's fix a call\b",
    r"\bcan we take\b",
    r"\bwhich date works\b",
    r"\bwhat time should\b",
    r"\bwould tomorrow work\b",
]


# ==========================================
# 7. REQUEST PATTERNS
# ==========================================

REQUEST_PATTERNS = [

    r"\b(?:please|pls|plz|kindly)\s+"
    r"(?:send|share|update|confirm|check|arrange|order|pay|book|call|ask|buy|get|prepare|give|submit|upload|reimburse|transfer|deliver|add|remove|enter|create|fix|make|schedule|review|reply|forward|provide)\b",

    r"\b(?:can you|could you|can u|could u|would you)\s+"
    r"(?:please\s+)?"
    r"(?:send|share|update|confirm|check|arrange|order|pay|book|call|ask|buy|get|prepare|give|submit|upload|reimburse|transfer|deliver|add|remove|enter|create|fix|make|schedule|review|reply|forward|provide|take|handle)\b",

    r"\bneed you to\s+"
    r"(?:send|share|update|confirm|check|arrange|order|pay|book|call|ask|buy|get|prepare|give|submit|upload|reimburse|transfer|deliver|add|remove|enter|create|fix|make|schedule|review|reply|forward|provide)\b",

    r"\blet me know\b",
    r"\bpay\s+\d+\b",
    r"\bpls give\b",
    r"\bplease give\b",
    r"\bplease ask\b",
    r"\bneed to ask\b",
    r"\bask the\b",
    r"\bsend me\b",
    r"\bsend your\b",
    r"\bi need a good\b",
    r"\bi need .* for\b",
    r"\bneed to clean\b",
    r"\bneed cleaning\b",
    r"\bneed to discuss\b",
    r"\bplease discuss\b",
    r"\bcan we take\b",
    r"\bplease buy\b",
    r"\bplease confirm your spot\b",
    r"\binvite to be made\b",
    r"\bplease get me\b",
    r"\bcan u take that over\b",
    r"\bneed another\b",
r"\bpaste .*link\b",
r"\badd .*calendar\b",
r"\breply to\b",
r"\border this\b",
r"\bpay .*fees\b",
]


# ==========================================
# 8. PATTERN HELPER
# ==========================================

def matches_any(text, patterns):

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            return True

    return False


# ==========================================
# 9. CLASSIFY MESSAGE
# ==========================================

def classify_message(message):

    if not is_text_message(message):
        return "other"

    text = clean_text(
        message.get("body", "")
    )

    if not text:
        return "other"

    text = text.lower().strip()

    # Ignore casual attendance messages
    if matches_any(text, NON_TASK_PATTERNS):
        return "other"

    # Completion messages
    if matches_any(text, COMPLETION_PATTERNS):
        return "completion"

    # Explicit deadlines
    if matches_any(text, DEADLINE_PATTERNS):

        if matches_any(
            text,
            REQUEST_PATTERNS + COMMITMENT_PATTERNS
        ):
            return "deadline"

    # Explicit commitments
    if matches_any(text, COMMITMENT_PATTERNS):
        return "commitment"

    # Follow-ups
    if matches_any(text, FOLLOWUP_PATTERNS):
        return "followup"

    # Questions
    if matches_any(text, QUESTION_PATTERNS):
        return "question"

    # Requests
    if matches_any(text, REQUEST_PATTERNS):
        return "request"

    return "other"


# ==========================================
# 10. GROUP MESSAGES BY CHAT
# ==========================================

def group_by_chat(messages):

    grouped = defaultdict(list)

    for message in messages:

        chat_id = message.get("chat_id")

        if chat_id:
            grouped[chat_id].append(message)

    for chat_id in grouped:

        grouped[chat_id].sort(
            key=lambda m: m.get("ts", 0)
        )

    return dict(grouped)


# ==========================================
# 11. QUOTED MESSAGE IDENTIFICATION
# ==========================================

def get_quoted_id(message):

    quoted = message.get("quoted_id")

    if isinstance(quoted, str):
        return quoted

    if isinstance(quoted, dict):

        return (
            quoted.get("id")
            or quoted.get("message_id")
        )

    return None


# ==========================================
# 12. MATCH COMPLETIONS TO TASKS
# ==========================================

def match_completion_to_request(messages, max_gap=30):

    chat_groups = group_by_chat(messages)

    matched_pairs = []

    task_types = [
        "request",
        "commitment",
        "deadline",
        "followup",
        "question"
    ]

    for chat_id, chat_messages in chat_groups.items():

        pending = []

        for index, message in enumerate(chat_messages):

            # Remove tasks outside the context window
            pending = [
                item
                for item in pending
                if index - item["index"] <= max_gap
            ]

            message_type = classify_message(message)

            # Store actionable message
            if message_type in task_types:

                pending.append({
                    "index": index,
                    "message": message,
                    "type": message_type
                })

                continue

            if message_type != "completion":
                continue

            completion_sender = message.get("sender_id")

            quoted_id = get_quoted_id(message)

            source_item = None

            # Priority 1: Exact quoted message
            if quoted_id:

                for item in pending:

                    if item["message"].get("id") == quoted_id:

                        source_item = item
                        break

            # Priority 2: Compatible sender relationship
            if source_item is None:

                possible = []

                for item in pending:

                    source = item["message"]

                    source_sender = source.get("sender_id")

                    if not source_sender or not completion_sender:
                        continue

                    if item["type"] == "commitment":

                        compatible = (
                            source_sender == completion_sender
                        )

                    else:

                        compatible = (
                            source_sender != completion_sender
                        )

                    if compatible:
                        possible.append(item)

                # Match only when exactly one candidate exists.
                # Avoid arbitrary matches when multiple tasks are pending.
                if possible:
                    source_item = max(
                        possible,
                        key=lambda item: item["index"]
                    )
            if source_item is None:
                continue

            source = source_item["message"]

            matched_pairs.append({

                "chat_id": chat_id,

                "request_message_id": source.get("id"),

                "request_sender": source.get("sender_id"),

                "request_text": source.get("body"),

                "completion_message_id": message.get("id"),

                "completion_sender": completion_sender,

                "completion_text": message.get("body")

            })

            pending.remove(source_item)

    return matched_pairs


# ==========================================
# 13. EXTRACT ACTIONABLE CANDIDATES
# ==========================================

def extract_open_candidates(messages, max_gap=30):

    chat_groups = group_by_chat(messages)

    candidates = []

    task_types = [
        "request",
        "commitment",
        "deadline",
        "followup",
        "question"
    ]

    for chat_id, chat_messages in chat_groups.items():

        for index, message in enumerate(chat_messages):

            message_type = classify_message(message)

            if message_type not in task_types:
                continue

            next_messages = chat_messages[
                index + 1:index + max_gap + 1
            ]

            context = []

            for next_message in next_messages:

                context.append({

                    "message_id": next_message.get("id"),

                    "sender_id": next_message.get("sender_id"),

                    "text": next_message.get("body", ""),

                    "type": classify_message(next_message)

                })

            candidates.append({

                "chat_id": chat_id,

                "message_id": message.get("id"),

                "sender_id": message.get("sender_id"),

                "text": message.get("body", ""),

                "type": message_type,

                "context": context

            })

    return candidates
