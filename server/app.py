import requests

url = 'http://127.0.0.1:5000/text_to_speech'
data = {'text': 'Hello, world!'}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open('output.wav', 'wb') as f:
        f.write(response.content)
else:
    print("Error:", response.json())