import logging
from faster_whisper import WhisperModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Transcriber:
    def __init__(self, model_name="base.en", device="cuda", compute_type="int8_float16"):
        """
        Initialize the Transcriber class with a WhisperModel.

        Args:
            model_name (str): The name of the Whisper model to use, defaults to 'base.en'.
            device (str): The device to run the model on, defaults to 'cuda'.
            compute_type (str): The compute type for the model, defaults to 'int8_float16'.
        """
        try:
            self.model = WhisperModel(model_name, device=device, compute_type=compute_type)
            logging.info(f"Initialized WhisperModel with model={model_name}, device={device}, compute_type={compute_type}")
        except Exception as e:
            logging.error(f"Failed to initialize WhisperModel: {e}")
            raise

    def transcribe(self, file_path):
        """
        Transcribes the given audio file.

        Args:
            file_path (str): Path to the audio file to be transcribed.

        Returns:
            list: A list of transcribed text segments.
        """
        try:
            segments, info = self.model.transcribe(file_path)
            logging.info("Successfully transcribed the audio file")

            text = [segment.text for segment in segments]
            return text
        except Exception as e:
            logging.error(f"Failed to transcribe audio: {e}")
            raise

# Example usage
# transcriber = Transcriber()
# file_path = "/home/js/workspace/voice_chatbot/data/lisbo.wav"
# transcribed_text = transcriber.transcribe(file_path)
# print(transcribed_text)
