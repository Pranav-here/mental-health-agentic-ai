from fastapi import FastAPI
from pydantic import BaseModel
from ai_agents import run_engine

app = FastAPI(title="CalmCurrent API", version="0.1.0")

class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(q: Query):
    tool_used, text = run_engine(q.message)
    return {"response": text, "tool_called": tool_used}
