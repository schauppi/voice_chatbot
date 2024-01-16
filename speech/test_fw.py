from faster_whisper import WhisperModel

#model_size = "large-v3"
model = "base.en"

model = WhisperModel(model, device="cuda", compute_type="int8_float16")

file = "/home/js/workspace/voice_chatbot/data/lisbo.wav"

segments, info = model.transcribe(file)

text = []

for segment in segments:
    text.append(segment.text)

print(text)