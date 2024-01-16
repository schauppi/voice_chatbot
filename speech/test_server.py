import requests

# URL of the Flask server (change the port if your server is running on a different one)
url = "http://localhost:5000/tts"

# Data to be sent (the text to be converted)
data = {
    "text": "Hello, world!"
}

# Sending a POST request with JSON data
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Save the received audio file
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio file saved as output.wav")
else:
    print("Error:", response.status_code, response.text)
