# Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


# Recieve and validate request from frontend
class Query(BaseModel):
    message: str


@app.post("/ask")
async def ask(query: Query):
    # AI Agent 
    # response = ai_agent(query)
    response = "this is from backend"
    # Send response to the frontend
    return response


if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
