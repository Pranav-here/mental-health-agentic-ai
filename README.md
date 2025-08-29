# CalmCurrent

A small, practical mental health support app with a Streamlit front end and a FastAPI backend. It offers supportive chat, a light therapist lookup, and an emergency call trigger that you must configure yourself. This is not medical advice.

> If you are in immediate danger, call your local emergency number right now or go to the nearest ER.

---

## Features

- **Supportive chat** via an Ollama-hosted model (Med-Gemma 4B by default). Falls back to a safe message if Ollama is not available.
- **Therapist lookup** using DuckDuckGo Search for Psychology Today, BetterHelp, and common counseling directories.
- **Emergency call trigger** through Twilio to a number you control. Only runs when the router sees clear risk keywords. Nothing calls at import time.

Low key credits in the UI sidebar and footer link back to the author. You can disable them with an env flag.

---

## Project structure

```
frontend.py        # Streamlit UI with subtle promo and a safety notice
server.py          # FastAPI endpoint /ask
ai_agents.py       # Simple intent router (support, therapist search, emergency)
tools.py           # Therapeutic reply, Twilio call, DuckDuckGo search
config.py          # Centralized env and model defaults
requirements.txt   # Python deps
Dockerfile         # One-container run for API and UI
.gitignore         # Standard Python ignores plus secrets
```

---

## Quick start (local)

### Prereqs
- Python 3.11
- Optional: [Ollama](https://ollama.com) running a local model. The code defaults to `alibayram/medgemma:4b`. Use any text model if you prefer.
- Optional: Twilio account for calls
- Optional: Internet connectivity for therapist search

### Setup

```bash
# clone your repo first, then
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Create your environment variables. Do not hardcode secrets in code.

```bash
export OPENAI_API_KEY=your_key_if_you_add_openai
export OLLAMA_MODEL="alibayram/medgemma:4b"   # or any local text model
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export TWILIO_FROM_NUMBER=+10000000000
export EMERGENCY_CONTACT=+10000000001
export BACKEND_URL=http://localhost:8000/ask
```

Run both services from the project root:
```bash
# Terminal 1
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2
streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0
```

Open http://localhost:8501 in your browser.

---

## Docker

Build and run a single container with both API and UI inside.

```bash
docker build -t calmcurrent .

# Map 8501 for UI and 8000 for API
docker run --rm -p 8501:8501 -p 8000:8000   -e BACKEND_URL="http://localhost:8000/ask"   -e OLLAMA_HOST="http://host.docker.internal:11434"   -e TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   -e TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   -e TWILIO_FROM_NUMBER=+10000000000   -e EMERGENCY_CONTACT=+10000000001   calmcurrent
```

If you use Ollama on the host, keep the `OLLAMA_HOST` value as shown above. On Linux you may prefer `--network=host` or map port 11434.

---

## API

### POST `/ask`

Request
```json
{
  "message": "hi, I need to find a therapist in Chicago"
}
```

Response
```json
{
  "response": "Here are some options near Chicago: ...",
  "tool_called": "find_therapists"
}
```

Router behavior:
- If message matches emergency keywords, the server returns a safety message and tries the Twilio call if configured.
- If message mentions therapy or counseling and contains a location at the end of the sentence, the server runs a DuckDuckGo query.
- Otherwise it returns a supportive reply using Ollama or a safe fallback.

---

## Configuration

`config.py` reads values from your environment:

- `OPENAI_API_KEY` (optional) only needed if you later swap to OpenAI
- `OLLAMA_MODEL` default `alibayram/medgemma:4b`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, `EMERGENCY_CONTACT` for emergency calls
- `BACKEND_URL` points the UI to the API

Keep a `.env` locally if you use direnv or dotenv. Never commit secrets. The `.gitignore` already ignores `.env` and `.env.*`.

---

## Safety and privacy

- This app is for supportive conversation. It does not diagnose or replace licensed care.
- Emergency flow is simple. You are responsible for verifying the phone number and voice content that Twilio calls.
- Do not log sensitive content in production. Streamlit and Uvicorn logs are for development.
- Rotate any keys you pasted earlier. If your repo is public, rotate now.

---

## Troubleshooting

- **Streamlit cannot reach the API**: check `BACKEND_URL` in your env and the API port. Try `curl http://localhost:8000/ask` with a small JSON payload.
- **Ollama errors**: verify `ollama serve` is running and that the model tag exists. Change `OLLAMA_MODEL` to a model you have.
- **Therapist search returns a fallback**: install `duckduckgo-search` and check network access from the server.
- **Twilio call fails**: confirm SID, token, and phone numbers. Some destinations require verified caller IDs on trial accounts.

---

## Credit

Built by **Pranav Kuchibhotla**. Low key links are in the UI. You can turn them off with `SHOW_PROMO=0`.

## License

MIT
