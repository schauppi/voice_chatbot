import requests

class Frontend:
    def __init__(self, server_url):
        self.server_url = server_url
        self.messages = [{'role': 'system', 'content': "You are a helpful pirate assistant"}]

    def call_model(self, messages):
        try:
            response = requests.post(self.server_url, json={'messages': messages})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error in calling server: {e}")
            return None

    def run(self):
        while True:
            user_message = input("You: ")
            self.messages.append({'role': 'user', 'content': user_message})

            response_json = self.call_model(self.messages)

            if response_json:
                print(response_json["message"]["content"])
                self.messages.append({'role': 'assistant', 'content': response_json["message"]["content"]})
                print(self.messages)
            else:
                print("Error occurred, no response obtained.")

# Initialize and run the frontend
frontend = Frontend("http://127.0.0.1:5000/chat")
frontend.run()
