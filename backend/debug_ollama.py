import ollama
import json

try:
    models = ollama.list()
    print(json.dumps(models, indent=2))
except Exception as e:
    print(f"Error: {e}")
