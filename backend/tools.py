# Setup Ollama with Medgemma tool
import ollama

def query_medgemma(prompt: str) -> str:
    """
        Calls medgemma model with a therepist personality profile.
        Returns  response as an emphetetic medical professional
    """
    system_prompt = """You are Dr. Pranav Kuchibhotla, a warm and experienced clinical psychologist. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """

    try:
        response=ollama.chat(
            model="alibayram/medgemma:4b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                'num_predict': 350,  # Slightly higher for structural purposes
                'temperature': 0.7,  # Balanced
                'top_p': 0.9  # For diverse but relevent response
            }
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"I'm having technical difficulties, but I want you to know your feeling matter. Please try again shortly."


# print(query_medgemma(prompt="Hi. How are you?"))

# Setup Twilio calling API tool
# Setup location tool