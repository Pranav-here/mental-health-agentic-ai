# Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Recieve and validate request from frontend
class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    # AI Agent 
    # response = ai_agent(query)
    response = "this is from backend"
    return response



# Send response to the frontend