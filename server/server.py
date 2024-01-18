from flask import Flask, request, jsonify, Response
from AudioGenerator import TextToSpeech  
from Transcriber import Transcriber    
from Chatbot import Chatbot
import logging
import os
import io
import soundfile as sf
from werkzeug.datastructures import FileStorage
from io import BytesIO
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config', type=str, help='The path to the config file')
args = parser.parse_args()
config_path = args.config

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
    Endpoint to convert text to speech. Returns the speech as a WAV file.
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
    Endpoint to convert speech to text. Expects the audio file in the request's body.
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
    Endpoint to interact with the chat model. Expects JSON with 'messages' key.
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
    app.run(debug=True)


