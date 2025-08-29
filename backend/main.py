# Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agents import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()


# Recieve and validate request from frontend
class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    # AI Agent 
    # response = ai_agent(query)
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)
    # Send response to the frontend
    return {
        "response": final_response,
        "tool_caller": tool_called_name
    }


if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
