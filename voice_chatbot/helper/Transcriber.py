import logging
import yaml
from faster_whisper import WhisperModel
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Transcriber:
    def __init__(self, config_file):
        """
        Initialize the Transcriber class with a WhisperModel.

        Args:
            config_file (str): The path to the configuration file.
        """
        # Load the configuration
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        model_name = config["Transcription"]["model"]
        device = config["Transcription"]["device"]

        if device == "cuda":
            compute_type = "int8_float16"
        else:
            compute_type = "int8"

        try:
            self.model = WhisperModel(model_name, device=device, compute_type=compute_type)
            logging.info(f"Initialized WhisperModel with model={model_name}, device={device}, compute_type={compute_type}")
        except Exception as e:
            logging.error(f"Failed to initialize WhisperModel with CUDA: {e}")
            logging.info("Fallback to CPU")
            self.model = WhisperModel(model_name, device='cpu', compute_type=compute_type)

    def transcribe(self, file):
        """
        Transcribes the given audio file.

        Args:
            file (file-like object): The audio file to be transcribed.

        Returns:
            list: A list of transcribed text segments.
        """
        print(file)
        try:
            # Save the file to a temporary location and transcribe it
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                temp.write(file.read())
                temp.flush()

                segments, info = self.model.transcribe(temp.name)
                logging.info("Successfully transcribed the audio file")

                text = [segment.text for segment in segments]
                return text
        except Exception as e:
            logging.error(f"Failed to transcribe audio: {e}")
            raise