from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import ollama
import asyncio
import json
import datetime

class Message(BaseModel):
    role: str
    content: str

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

@app.get("/models")
def get_models():
    try:
        response = ollama.list()
        # response is an object with a 'models' attribute, containing a list of Model objects
        # Each Model object has a 'model' attribute
        return {"models": [m.model for m in response.models]}
    except Exception as e:
        print(f"Error fetching models: {e}")
        return {"models": []}



class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = "qwen2.5:32b"

@app.post("/chat")
async def chat(request: ChatRequest):
    async def generate_response():
        try:
            # Convert Pydantic models to dicts for Ollama
            messages = [m.model_dump() for m in request.messages]
            
            stream = ollama.chat(
                model=request.model,
                messages=messages,
                stream=True,
            )
            
            for chunk in stream:
                # Yield content chunk
                if 'message' in chunk and 'content' in chunk['message']:
                    content_data = {
                        "type": "content",
                        "content": chunk['message']['content']
                    }
                    yield json.dumps(content_data) + "\n"
                
                # Yield usage chunk if available (usually in the last chunk)
                if chunk.get('done') is True:
                    usage_data = {
                        "type": "usage",
                        "prompt_eval_count": chunk.get('prompt_eval_count', 0),
                        "eval_count": chunk.get('eval_count', 0)
                    }
                    yield json.dumps(usage_data) + "\n"
            
        except Exception as e:
            print(f"Ollama error: {e}")
            error_data = {
                "type": "content", 
                "content": f"Error: {str(e)}"
            }
            yield json.dumps(error_data) + "\n"

    return StreamingResponse(generate_response(), media_type="application/x-ndjson")

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
