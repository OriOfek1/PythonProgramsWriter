import os
import subprocess
from openai import OpenAI, Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_code():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":"You are an expert python developer. Create for me a python program that checks if a number is prime. Do not write any explanations, just show me the code itself.Also please include unit tests that check the logic of the program using 5 different inputs and expected outputs."}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    generated_code = response.choices[0].message.content
    return generated_code

def extract_python_code(code):
    python_code = code.split('```python\n')[1].split('```')[0]
    return python_code

def write_to_file(code):
    with open('generatedcode.py', 'w') as file:
        file.write(code)


# Generate code
generated_code = generate_code()

# Extract Python code
python_code = extract_python_code(generated_code)

# Write generated Python code to file
write_to_file(python_code)

# Run the generated Python code using subprocess.run()
try:
    subprocess.run(["python", "generatedcode.py"], check=True)
    print("Python code executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing Python code: {e}")

