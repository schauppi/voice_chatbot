from TTS.api import TTS
import soundfile as sf

class TextToSpeech:
    def __init__(self, device="cuda", model_name="tts_models/en/ljspeech/vits"):
        self.device = device
        self.TTS = TTS(model_name=model_name, progress_bar=True).to(self.device)


    def save_wav(self, wav, output_path="data/output.wav"):
        """
        Save the .wav file to output path
        """
        sf.write(output_path, wav, samplerate=22050)

    def text_to_speech(self, text):
        """
        Converts text to speech using a specified TTS model.
        """
        wav = self.TTS.tts(text=text)
        return wav

    def voice_cloning(self, text, speaker_wav, language="en", output_path="data/vc_output.wav"):
        """
        Clones voice from a given speaker's sample and synthesizes speech from text.
        """
        wav = self.TTS.tts(text=text, speaker_wav=speaker_wav, language=language)
        return wav

"""
vc_model = "tts_models/multilingual/multi-dataset/xtts_v2"
tts_model = "tts_models/en/ljspeech/vits"
"""
"""
tts_model = "tts_models/en/ljspeech/vits"
tts = TextToSpeech()
wav = tts.text_to_speech("Hello how are you papuschi kuraz")
tts.save_wav(wav)"""