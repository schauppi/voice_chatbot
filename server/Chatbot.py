import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Chatbot:
    def __init__(self, url):
        """
        Initialize the Server class with a specific URL for model communication.

        Args:
            url (str): The URL to which the model requests are sent.
        """
        self.url = url
        logging.info(f"Server initialized with URL: {url}")

    def call_model(self, messages):
        """
        Send a request to the model with the given messages and return the response.

        Args:
            messages (list): A list of message dictionaries to be sent to the model.

        Returns:
            dict: The JSON response from the model.

        Raises:
            Exception: If the request to the model fails.
        """
        try:
            data = {"model": "mistral", "messages": messages, "stream": False, "options": {"temperature": 0}}
            response = requests.post(self.url, data=json.dumps(data))
            response.raise_for_status()  # Raises HTTPError for bad requests
            response_text = response.content.decode('utf-8')
            logging.info("Successfully received response from the model")
            return json.loads(response_text)
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred during model call: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred during model call: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during model call: {e}")
            raise
