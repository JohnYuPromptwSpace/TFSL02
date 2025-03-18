import openai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

while True:
    message = input("User : ")
    if message:
        messages = [{"role": "user", "content": message}]
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
            )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")