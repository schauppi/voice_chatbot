import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChatbotHandler:
    """
    This class handles the interaction with the chatbot server.
    It maintains a list of messages and sends them to the server for processing.
    """

    def __init__(self, server_url):
        """
        Initialize the ChatbotHandler with the server URL.
        """
        self.server_url = server_url
        self.messages = [{'role': 'system', 'content': "You are a helpful pirate assistant"}]

    def call_model(self, messages):
        """
        Send the messages to the server and return the server's response.
        If an error occurs during the request, log the error and return None.
        """
        try:
            response = requests.post(self.server_url, json={'messages': messages})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error in calling server: {e}")
            return None

    def handle_chat(self, message):
        """
        Add the user's message to the list of messages and send them to the server.
        Append the server's response to the list of messages and return it.
        """
        self.messages.append({'role': 'user', 'content': message})
        response_json = self.call_model(self.messages)
        if response_json is None:
            logging.error("No response from server.")
            return None
        self.messages.append({'role': 'assistant', 'content': response_json["message"]["content"]})
        return response_json["message"]["content"], self.messages
