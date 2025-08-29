from langchain.agents import tool
from tools import query_medgemma, call_emergency


@tool
def ask_mental_health_specialist(query: str) -> str:
    """
        Generate a therapuetic response using the Medgemma model
        use this for all general user queries, mental health questions, emotional concerns,
        or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)


@tool
def emergency_call_tool(query: str) -> str:
    """
        Place an emergency call to the safety helpline's phone number via Twilio.
        Use this only if the user expresses sucidal ideation, intent to self-harm,
        or decribes a mental health emergency requireing immediate help.
    """
    return call_emergency(query)


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )

# Setup AI agent and link to the backend

