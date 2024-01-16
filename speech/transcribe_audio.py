import requests

class AudioTranscriber:
    def __init__(self, endpoint='http://127.0.0.1:8080/inference'):
        self.endpoint = endpoint

    def transcribe_audio(self, file_path, temperature=0.0, temperature_inc=0.0):
        files = {'file': open(file_path, 'rb')}
        data = {
            'temperature': temperature,
            'temperature_inc': temperature_inc,
            'response_format': 'json'
        }

        response = requests.post(self.endpoint, files=files, data=data)
        return response.json()

# Example usage
if __name__ == "__main__":
    transcriber = AudioTranscriber()
    response = transcriber.transcribe_audio('/Users/davidschaupp/Documents/voice_chatbot/speech/output.wav')
    print(response["text"])
