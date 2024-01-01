import os
from openai import OpenAI, Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_code():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":"You are an expert python developer. Create for me a python program that checks if a number is prime. Do not write any explanations, just show me the code itself."}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    code = response.choices[0].message.content
    return code

print(get_code())


