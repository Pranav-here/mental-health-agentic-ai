from typing import Tuple
import re
from tools import therapeutic_reply, place_emergency_call, find_therapists

# Simple rule-based router. It is boring but stable and testable.
# You can swap this for LangGraph later if you want tool learning.

EMERGENCY_PATTERNS = [
    r"\bkill myself\b", r"\bsuicide\b", r"\bself[-\s]?harm\b",
    r"\bend it all\b", r"\bno reason to live\b"
]
THERAPIST_PATTERNS = [
    r"\btherapist\b", r"\bcounsel(or|ling)\b", r"\bpsy(chologist|chiatrist)\b"
]

def classify_intent(text: str) -> str:
    t = text.lower()
    if any(re.search(p, t) for p in EMERGENCY_PATTERNS):
        return "emergency"
    if any(re.search(p, t) for p in THERAPIST_PATTERNS):
        return "therapist_search"
    return "support_chat"

def run_engine(message: str) -> Tuple[str, str]:
    """
    Route to the right tool and return (tool_called, response_text).
    """
    intent = classify_intent(message)

    if intent == "emergency":
        tool_used = "place_emergency_call"
        # We do both: immediately recommend local services, and try a call if configured.
        status = place_emergency_call("Triggered by urgent user message.")
        reply = (
            "I’m concerned for your safety. If you are in immediate danger, "
            "call your local emergency number right now or go to the nearest ER. "
            f"{status}"
        )
        return tool_used, reply

    if intent == "therapist_search":
        tool_used = "find_therapists"
        # Try to guess a location from the message, otherwise ask for one
        m = re.search(r"in ([A-Za-z .,-]{2,})$", message.strip())
        location = m.group(1).strip() if m else ""
        if not location:
            # Fallback wording if no location was detected
            return tool_used, "Tell me a city or area and I’ll look up therapists near you."
        listing = find_therapists(location)
        return tool_used, listing

    # Default to supportive chat
    tool_used = "therapeutic_reply"
    reply = therapeutic_reply(message)
    return tool_used, reply
