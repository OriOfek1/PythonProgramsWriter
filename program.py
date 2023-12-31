import os
from openai import OpenAI
from dotenv import load_dotenv

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()
chat_completion = client.chat.completions.create(

    model="gpt-3.5-turbo",
    messages = [
        {
            "role": "user",
            "content": "You are an expert python developer. Create for me a python program that checks if a number is prime. Do not write any explanations, just show me the code itself."
        }
    ]
)
print(chat_completion.choices[0].text.strip())
