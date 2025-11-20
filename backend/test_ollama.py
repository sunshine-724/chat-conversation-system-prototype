import ollama

try:
    models_response = ollama.list()
    if not models_response['models']:
        print("No models found")
        exit(1)
    
    model_name = models_response['models'][0]['model']
    print(f"Using model: {model_name}")

    stream = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': 'Hello'}],
        stream=True,
    )
    for chunk in stream:
        print(chunk)
except Exception as e:
    print(f"Error: {e}")
