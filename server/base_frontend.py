import requests
from Chatbot_Handler import ChatbotHandler

server = "http://127.0.0.1:5000"

chatbot = ChatbotHandler(server + "/chat")

"""while True: 
    print(chatbot.handle_chat(input("You: ")))"""

###