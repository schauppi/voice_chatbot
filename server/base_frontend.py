import gradio as gr
import requests
import logging
from Chatbot_Handler import ChatbotHandler

server = "http://127.0.0.1:5000"

chatbot_handler = ChatbotHandler(server + "/chat")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_audio(text):
    try:
        logging.info(f"Generating audio for text: {text}")
        response = requests.post(server + "/text_to_speech", json={'text': text})
        response.raise_for_status()
        with open('output.wav', 'wb') as file:
            file.write(response.content)
        logging.info("Audio generated successfully")
    except Exception as e:
        logging.error(f"Error occurred during audio generation: {str(e)}")

def chat(transcribed_audio):
    try:
        logging.info(f"Sending messages to server: {transcribed_audio}")
        response, _ = chatbot_handler.handle_chat(transcribed_audio)
        generate_audio(response)
        return response
    except Exception as e:
        logging.error(f"Error occurred during chat: {str(e)}")
        return "Error in chatbot response."

def transcribe_audio(audio):
    try:
        logging.info(f"Transcribing audio: {audio}")
        with open(audio, "rb") as file:
            file_content = file.read()
        response = requests.post(server + "/speech_to_text", data=file_content)
        response.raise_for_status()
        transcribed_audio = response.json()["transcribed_text"]
        return transcribed_audio[0]
    except Exception as e:
        logging.error(f"Error occurred during audio transcription: {str(e)}")
        return "Error in audio transcription."

def update_chat_with_transcription(transcribed_text, chat_history):
    chat_history.append((transcribed_text, "Waiting for assistant response..."))
    return chat_history

def handle_chatbot_response(transcribed_text, chat_history):
    transcribed_text = chat_history[-1][0]
    chatbot_response = chat(transcribed_text)
    # Update the last chat history entry with the bot's response
    chat_history[-1] = (transcribed_text, chatbot_response)
    return chat_history

def handle_audio_input(audio, chat_history):
    transcribed_text = transcribe_audio(audio)
    updated_chat_history = update_chat_with_transcription(transcribed_text, chat_history)
    return updated_chat_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()

    with gr.Row():
        audio = gr.Audio(sources=["microphone"], type="filepath", 
                        waveform_options=gr.WaveformOptions(
                        waveform_color="#01C6FF",
                        waveform_progress_color="#0066B4",
                        skip_length=2,
                        show_controls=False,
                         ))
        send_audio_button = gr.Button("Send Audio", interactive=True)

        # Split the handling into two steps: immediate transcription display and asynchronous chatbot response
        send_audio_button.click(
            handle_audio_input,
            inputs=[audio, chatbot],
            outputs=[chatbot]
        ).then(
            # Asynchronously handle the chatbot response
            handle_chatbot_response,
            inputs=[audio, chatbot],
            outputs=[chatbot]
        )

demo.launch(debug=True)