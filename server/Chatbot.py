import requests, json

context = [] 

def generate(prompt, context):
    r = requests.post('http://localhost:11434/api/generate',
                     json={
                         'model': "mistral:latest",
                         'prompt': prompt,
                         'context': context,
                     },
                     stream=False)
    r.raise_for_status()
    return r

response = generate("Hello how are you?", [])
print(json.loads(response))

"""    response = ""  

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        print(response_part)
        if 'error' in body:
            raise Exception(body['error'])

        response += response_part

        if body.get('done', False):
            context = body.get('context', [])
            return response, context

def chat(input, chat_history):

    chat_history = chat_history or []

    global context
    output, context = generate(input, context)

    chat_history.append((input, output))

    return chat_history

chat_hist = chat("Hello how are you?", [])"""
