from typing import List
from config import (
    OPENAI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER, EMERGENCY_CONTACT, OLLAMA_MODEL
)

# 1) Therapeutic reply via Ollama Med-Gemma (fallback safe message on error)
def therapeutic_reply(user_text: str) -> str:
    """
    Generate a warm, supportive reply for mental health conversations.
    Uses an on-device Ollama model if available.
    """
    try:
        import ollama  # requires `pip install ollama` and `ollama run <model>` once
        system_prompt = (
            "You are Dr. Riya Menon, a licensed clinical psychologist persona. "
            "Be empathetic, supportive, and practical. Do not diagnose. "
            "Invite gentle next steps and ask one open question to keep the user talking. "
            "If the user describes imminent danger, advise calling local emergency services."
        )
        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            options={"num_predict": 300, "temperature": 0.7, "top_p": 0.9}
        )
        return resp["message"]["content"].strip()
    except Exception:
        return (
            "I’m here with you. I can tell this matters a lot. "
            "If you want, tell me a bit more about when these feelings get strongest, "
            "and we can find one small step that might help."
        )

# 2) Emergency call via Twilio
def place_emergency_call(note: str = "") -> str:
    """
    Trigger a phone call to your configured emergency contact.
    Only call this when there is clear risk of harm.
    """
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT]):
        return "Emergency call not configured on the server."

    try:
        from twilio.rest import Client  # pip install twilio
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            to=EMERGENCY_CONTACT,
            from_=TWILIO_FROM_NUMBER,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        return f"Emergency call triggered (sid: {call.sid})."
    except Exception as e:
        return f"Failed to place emergency call: {e}"

# 3) DuckDuckGo therapist search
def find_therapists(location: str, limit: int = 5) -> str:
    """
    Look up nearby therapists using DuckDuckGo web search.
    Returns a short, readable list of options.
    """
    query = f'therapist "{location}" site:psychologytoday.com OR site:betterhelp.com OR "counseling center" "{location}"'
    try:
        # pip install duckduckgo-search
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=limit):
                title = r.get("title", "Result")
                href = r.get("href") or r.get("url") or ""
                source = r.get("source") or ""
                results.append(f"- {title} ({source})\n  {href}")

        if not results:
            return f"Could not find public listings for '{location}'. Try a nearby city name."
        return f"Here are some options near {location}:\n" + "\n".join(results)
    except Exception:
        # Library missing or network blocked
        return (
            "Live search is not available on the server. "
            "Try: Psychology Today directory, NAMI helpline, or your campus counseling center."
        )
