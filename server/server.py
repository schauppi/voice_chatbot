from flask import Flask, request, jsonify, Response
from AudioGenerator import TextToSpeech  # Assuming your TTS class is in this file
from Transcriber import Transcriber    # Assuming your Transcription class is in this file
import logging
import os
import io
import soundfile as sf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Global instances of TextToSpeech and Transcriber
try:
    logging.info("Initializing TextToSpeech and Transcriber models...")
    tts = TextToSpeech()       # Assuming TextToSpeech is properly imported
    transcriber = Transcriber() # Assuming Transcriber is properly imported
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
    Endpoint to convert speech to text. Expects JSON with 'file_path' key.
    """
    data = request.json
    file_path = data.get('file_path', '')

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        text_segments = transcriber.transcribe(file_path)
        return jsonify({"message": "Success", "transcribed_text": text_segments})
    except Exception as e:
        logging.error(f"Error in speech-to-text conversion: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


