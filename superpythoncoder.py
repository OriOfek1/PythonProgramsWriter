import os
import random
import subprocess
from openai import OpenAI, Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

PROGRAMS_LIST = [
    '''Given two strings str1 and str2, prints all interleavings of the given
two strings. You may assume that all characters in both strings are
different.Input: str1 = "AB",  str2 = "CD"
Output:
    ABCD
    ACBD
    ACDB
    CABD
    CADB
    CDAB
Input: str1 = "AB",  str2 = "C"
Output:
    ABC
    ACB
    CAB  ''',
    "a program that checks if a number is a palindrome",
    "A program that finds the kth smallest element in a given binary search tree."
]

def generate_code(program_description):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":f"You are an expert python developer. Create for me a python program that {program_description}. Do not write any explanations, just show me the code itself.Also please include unit tests that check the logic of the program using 5 different inputs and expected outputs."}
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


# Main function to initiate the code generation process
def main():
    user_input = input("Tell me, which program would you like me to code for you? If you don't have an idea, just press enter and I will choose a random program to code: ")

    # Choosing a program from the list or user's input
    if not user_input.strip():
        chosen_program = random.choice(PROGRAMS_LIST)
    else:
        chosen_program = user_input.strip()

    attempts = 0
    generated_code = ""

    # Loop to attempt code generation and execution up to 5 times
    while attempts < 5:
        # Generate code based on the chosen program
        generated_code = generate_code(chosen_program)
        python_code = extract_python_code(generated_code)

        filename = "generatedcode.py"
        write_to_file(python_code)
        print(f"The code for '{chosen_program}' has been written to '{filename}'.")

        try:
            # Execute the generated Python code
            subprocess.run(["python", filename], check=True)
            print("Python code executed successfully.")
            break  # No errors, exit the loop
        except subprocess.CalledProcessError as e:
            attempts += 1
            print(f"Error running generated code! Error: {e}")

            # Send error to ChatGPT for fixing
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"I encountered an error: {e}. Please fix the code."}
            ]
            response = client.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            generated_code = response.choices[0].message.content.strip()
            chosen_program = generated_code  # Use the fixed code in the next attempt

    if attempts == 5:
        print("Code generation FAILED.")

if __name__ == "__main__":
    main()
