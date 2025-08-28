# Setup FastAPI backend
from fastapi import FastAPI

app = FastAPI()


@app.post("/ask")
async def ask():
    # AI Agent 
    return "This is the response"

# Recieve and validate request from frontend

# Send response to the frontend