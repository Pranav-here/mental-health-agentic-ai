from langchain.agents import tool
from tools import query_medgemma


@tool
def ask_mental_health_specialist(query: str) -> str:
    """
        Generate a therapuetic response using the Medgemma model
        use this for all general user queries, mental health questions, emotional concerns,
        or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)


# Setup AI agent and link to the backend

