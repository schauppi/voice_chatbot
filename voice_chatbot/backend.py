from flask import Flask, request, jsonify, Response
from helper.AudioGenerator import TextToSpeech  
from helper.Transcriber import Transcriber    
from helper.Chatbot import Chatbot
import logging
import os
import io
import soundfile as sf
from werkzeug.datastructures import FileStorage
from io import BytesIO
import argparse
import yaml

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config', type=str, help='The path to the config file')
args = parser.parse_args()
config_path = args.config

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)

try:
    logging.info("Initializing TextToSpeech and Transcriber models...")
    tts = TextToSpeech(config_path)      
    transcriber = Transcriber(config_path) 
    chatbot = Chatbot(config_path)
    logging.info("Models loaded successfully.")
except Exception as e:
    logging.error(f"Failed to initialize models: {e}")
    raise

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    """
    Convert text to speech and return the speech as a WAV file.

    Args:
        text (str): The text to be converted to speech.

    Returns:
    """
    data = request.json
    text = data.get('text', '')

    try:
        wav = tts.text_to_speech(text)
        
        # Convert WAV data to binary
        buffer = io.BytesIO()
        sf.write(buffer, wav, samplerate=22050, format='WAV')
        buffer.seek(0)
        
        return Response(buffer, mimetype='audio/wav')
    except Exception as e:
        logging.error(f"Error in text-to-speech conversion: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    """
    Convert speech to text.

    Args:
        audio (bytes): The audio data to be transcribed.

    Returns:
        dict: A dictionary containing the transcribed text.
    """
    # Convert the request data to a file-like object
    file = FileStorage(stream=BytesIO(request.data), filename='audio.wav')

    try:
        text_segments = transcriber.transcribe(file)
        return jsonify({"message": "Success", "transcribed_text": text_segments})
    except Exception as e:
        logging.error(f"Error in speech-to-text conversion: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Interact with the chat model.

    Args:
        messages (list): A list of messages to be processed by the chat model.

    Returns:
        dict: A dictionary containing the chat model's response.
    """
    data = request.json
    messages = data.get('messages', [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    try:
        response = chatbot.call_model(messages)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in chat model communication: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=config["ServerPort"]["port"])


