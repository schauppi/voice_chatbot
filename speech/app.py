from flask import Flask, request, send_file, jsonify
from generate_audio import TextToSpeech
from transcribe_audio import AudioTranscriber
import logging
from io import BytesIO
import io
import wave
import numpy as np

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

app = Flask(__name__)

# Initialize your TTS class
tts_model = "tts_models/en/ljspeech/vits"
tts = TextToSpeech(model_name=tts_model)

transcriber = AudioTranscriber()

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return "No text provided", 400

        wav_samples = tts.text_to_speech(text=text)

        # Convert the samples to a WAV file in memory
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(1)  # or the appropriate number of channels
            wf.setsampwidth(2)  # or the appropriate sample width in bytes
            wf.setframerate(22050)  # or the appropriate frame rate
            wf.writeframes(np.array(wav_samples, dtype=np.int16).tobytes())  # converting to bytes
        buffer.seek(0)  # rewind to the start of the file

        return send_file(
            buffer,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="output.wav"
        )
    except Exception as e:
        logging.error(f"Error in text_to_speech: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 