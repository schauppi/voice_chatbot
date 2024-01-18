import gradio as gr
import requests
import logging
from Chatbot_Handler import ChatbotHandler
import argparse
import yaml

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config', type=str, help='The path to the config file')
args = parser.parse_args()
config_path = args.config

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

class FrontEnd:
    def __init__(self, server_url, context):
        """
        Initialize the FrontEnd class.

        Args:
            server (str): The server URL.

        """
        self.server = server_url
        self.chatbot_handler = ChatbotHandler(self.server + "/chat", context)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def generate_audio(self, text):
        """
        Generate audio from the given text.

        Args:
            text (str): The text to be converted to audio.

        Raises:
            Exception: If the request to generate audio fails.
        """
        try:
            logging.info(f"Generating audio for text: {text}")
            response = requests.post(self.server + "/text_to_speech", json={'text': text})
            response.raise_for_status()
            with open('output.wav', 'wb') as file:
                file.write(response.content)
            logging.info("Audio generated successfully")
        except Exception as e:
            logging.error(f"Error occurred during audio generation: {str(e)}")

    def chat(self, transcribed_audio):
        """
        Send the transcribed audio to the server and get the response.

        Args:
            transcribed_audio (str): The transcribed audio to be sent to the server.

        Returns:
            str: The response from the server.

        Raises:
            Exception: If the request to the server fails.
        """
        try:
            logging.info(f"Sending messages to server: {transcribed_audio}")
            response, _ = self.chatbot_handler.handle_chat(transcribed_audio)
            self.generate_audio(response)
            return response
        except Exception as e:
            logging.error(f"Error occurred during chat: {str(e)}")
            return "Error in chatbot response."

    def transcribe_audio(self, audio):
        """
        Transcribe the given audio to text.

        Args:
            audio (str): The audio to be transcribed.

        Returns:
            str: The transcribed text.

        Raises:
            Exception: If the transcription fails.
        """
        try:
            logging.info(f"Transcribing audio: {audio}")
            with open(audio, "rb") as file:
                file_content = file.read()
            response = requests.post(self.server + "/speech_to_text", data=file_content)
            response.raise_for_status()
            transcribed_audio = response.json()["transcribed_text"]
            return transcribed_audio[0]
        except Exception as e:
            logging.error(f"Error occurred during audio transcription: {str(e)}")
            return "Error in audio transcription."


    def update_chat_with_transcription(self, transcribed_text, chat_history):
        """
        Update the chat history with the transcribed text.

        Args:
            transcribed_text (str): The transcribed text.
            chat_history (list): The chat history.

        Returns:
            list: The updated chat history.

        Raises:
            Exception: If the chat history update fails.
        """
        try:
            chat_history.append((transcribed_text, "Waiting for assistant response..."))
            return chat_history
        except Exception as e:
            logging.error(f"Failed to update chat with transcription: {e}")
            raise


    def handle_chatbot_response(self, transcribed_text, chat_history):
        """
        Handle the chatbot response.

        Args:
            transcribed_text (str): The transcribed text.
            chat_history (list): The chat history.

        Returns:
            list: The updated chat history.

        Raises:
            Exception: If the chatbot response handling fails.
        """
        try:
            transcribed_text = chat_history[-1][0]
            chatbot_response = self.chat(transcribed_text)
            chat_history[-1] = (transcribed_text, chatbot_response)
            return chat_history
        except Exception as e:
            logging.error(f"Failed to handle chatbot response: {e}")
            raise

    def handle_audio_input(self, audio, chat_history):
        """
        Handle the audio input.

        Args:
            audio (str): The audio input.
            chat_history (list): The chat history.

        Returns:
            list: The updated chat history.
        """
        transcribed_text = self.transcribe_audio(audio)
        updated_chat_history = self.update_chat_with_transcription(transcribed_text, chat_history)
        return updated_chat_history

    def run(self):
        """
        Run the frontend.

        Raises:
            Exception: If the frontend fails to run.
        """
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot()

            with gr.Row():
                audio = gr.Audio(sources=["microphone"], type="filepath", 
                                waveform_options=gr.WaveformOptions(
                                waveform_color="#01C6FF",
                                waveform_progress_color="#0066B4",
                                skip_length=2,
                                show_controls=False,
                                 ))
                send_audio_button = gr.Button("Send Audio", interactive=True)

                # Split the handling into two steps: immediate transcription display and asynchronous chatbot response
                send_audio_button.click(
                    self.handle_audio_input,
                    inputs=[audio, chatbot],
                    outputs=[chatbot]
                ).then(
                    # Asynchronously handle the chatbot response
                    self.handle_chatbot_response,
                    inputs=[audio, chatbot],
                    outputs=[chatbot]
                )

        demo.launch(debug=True)

if __name__ == "__main__":
    server_url = config["Frontend"]["server_url"] + ":" + config["ServerPort"]["port"]
    context = config["Chatbot"]["context"]
    frontend = FrontEnd(server_url, context)
    frontend.run()