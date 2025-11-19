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

from fastapi.responses import StreamingResponse
import asyncio
import json

@app.post("/chat")
async def chat(message: str, model: str = "qwen2.5:32b"):
    async def generate_response():
        try:
            stream = ollama.chat(
                model=model,
                messages=[{'role': 'user', 'content': message}],
                stream=True,
            )
            for chunk in stream:
                yield chunk['message']['content']
            
            # Stop here if successful
            return

        except Exception as e:
            print(f"Ollama error: {e}")
            # Fallback/Simulation only on error
            full_response = f"Echo [{model}] (Streamed): {message} "
            for word in full_response.split():
                yield word + " "
                await asyncio.sleep(0.1)

    return StreamingResponse(generate_response(), media_type="text/plain")
