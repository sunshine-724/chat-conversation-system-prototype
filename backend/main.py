from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

from fastapi.responses import StreamingResponse
import asyncio
import json

@app.post("/chat")
async def chat(message: str, model: str = "qwen2.5:32b"):
    async def generate_response():
        try:
            # Try to use Ollama if available
            # stream = ollama.chat(
            #     model=model,
            #     messages=[{'role': 'user', 'content': message}],
            #     stream=True,
            # )
            # for chunk in stream:
            #     yield chunk['message']['content']
            
            # Fallback/Simulation
            full_response = f"Echo [{model}] (Streamed): {message} "
            for word in full_response.split():
                yield word + " "
                await asyncio.sleep(0.1)
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(generate_response(), media_type="text/plain")

from pydantic import BaseModel
from typing import List
import datetime

class Message(BaseModel):
    role: str
    content: str

class ChatHistory(BaseModel):
    messages: List[Message]

@app.post("/export")
async def export_chat(history: ChatHistory):
    # Create a formatted string or JSON structure
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}.json"
    
    # For now, just dumping the JSON
    content = history.model_dump_json(indent=2)
    
    return StreamingResponse(
        iter([content]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
