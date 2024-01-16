import torch
from TTS.api import TTS

device = "cpu"

text = """Das ist ein Test Text Amenakoi Papuschi Kuraz"""

tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=True)

tts.tts_to_file(text=text, file_path="output.wav")

"""speaker_wav = "/Users/davidschaupp/Documents/voice_chatbot/speech/output.wav"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

text = "Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language"

#tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path="tts_output.wav")

wav = tts.tts(text=text, speaker_wav=speaker_wav, language="en")"""


