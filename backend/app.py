from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .brain import think

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

class Query(BaseModel):
    text: str

@app.post("/voice-agent")
async def voice_agent(query: Query):
    return think(query.text)
