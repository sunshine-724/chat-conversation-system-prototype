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
