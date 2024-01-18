import logging
from TTS.api import TTS
import soundfile as sf
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextToSpeech:
    def __init__(self, config_file="config.yaml"):
        """
        Initialize the TextToSpeech class.

        Args:
            config_file (str): The path to the configuration file.
        """
        # Load the configuration
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        model_name = config["AudioGeneration"]["model"]
        device = config["AudioGeneration"]["device"]

        try:
            self.device = device
            self.TTS = TTS(model_name=model_name, progress_bar=True).to(self.device)
            logging.info(f"Initialized TextToSpeech with device={device} and model_name={model_name}")
        except Exception as e:
            logging.error(f"Failed to initialize TextToSpeech with CUDA: {e}")
            logging.info("Fallback to CPU")
            self.device = 'cpu'
            self.TTS = TTS(model_name=model_name, progress_bar=True).to(self.device)

    def text_to_speech(self, text):
        """
        Convert text to speech.

        Args:
            text (str): The text to be converted to speech.

        Returns:
            numpy.ndarray: The waveform of the generated speech.
        """
        try:
            wav = self.TTS.tts(text=text)
            logging.info("Successfully converted text to speech")
            return wav
        except Exception as e:
            logging.error(f"Error in converting text to speech: {e}")
            raise

    def save_wav(self, wav, output_path):
        """
        Save the generated waveform to a file.

        Args:
            wav (numpy.ndarray): The waveform array of the speech.
            output_path (str): The path where the output file will be saved.
        """
        try:
            sf.write(output_path, wav, samplerate=22050)
            logging.info(f"Waveform saved successfully to {output_path}")
        except Exception as e:
            logging.error(f"Failed to save waveform: {e}")
            raise

# Example usage
#tts = TextToSpeech()
#wav = tts.text_to_speech("Hello, world!")