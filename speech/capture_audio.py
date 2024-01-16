import pyaudio
import numpy as np
import wave
import logging

class AudioRecorder:
    def __init__(self, chunk=1024, format=pyaudio.paInt16, channels=1, rate=16000, record_seconds=20, filename='speech/output.wav'):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
        self.filename = filename
        self.frames = []
        self.stream = None
        self.pyaudio_instance = None

        logging.basicConfig(level=logging.INFO)

    def start_recording(self):
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = self.pyaudio_instance.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        logging.info("* Recording")

        try:
            for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
                data = self.stream.read(self.chunk)
                self.frames.append(data)
        except KeyboardInterrupt:
            pass

        logging.info("* Done recording")

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio_instance.terminate()

    def save_recording(self):
        logging.info("* Saving recording")
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.pyaudio_instance.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

# Example usage
if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.start_recording()
    recorder.stop_recording()
    recorder.save_recording()
