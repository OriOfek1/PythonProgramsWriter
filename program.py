import os
from openai import OpenAI

# Define your OpenAI API key
secret_key = "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"
s = "fakekey"
client = OpenAI(
    api_key = os.environ.get(s), 
)
chat_completion = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": "Say this is a test"
        }
    ],
    model="gpt-3.5-turbo",
)