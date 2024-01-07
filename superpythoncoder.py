import os
import sys
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
    "A program that finds the kth smallest element in a given binary search tree.",
    "A program that puts the user in a pokemon battle with three pokemons to choose from.The user battles the computer"
]

#generates a code for a pyhton program based on an input program_description
def generate_code(program_description):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":f"You are an expert python developer. Create for me a python program that {program_description}. Do not write any explanations, just show me the code itself.Also please include unit tests that check the logic of the program using 5 different inputs and expected outputs.anything but the code in your answer is redundant."}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    generated_code = response.choices[0].message.content
    return generated_code

#extracts python code from a chat response
def extract_python_code(code):
    start_index = code.find('```python\n')
    if start_index != -1:
        start_index += len('```python\n')
        end_index = code.find('```', start_index)
        if end_index != -1:
            python_code = code[start_index:end_index]
            return python_code
    return ""

#writes a code to a file
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
    
    # Stores the description of the requested code 
    requested_code_description = chosen_program 

    attempts = 1
    generated_code = ""

    # Loop to attempt code generation and execution up to 5 times
    while attempts < 6:

        # Generate code based on the chosen program
        if attempts == 1:
            generated_code = generate_code(chosen_program)
        
        python_code = extract_python_code(generated_code)

        code_file = "generatedcode.py"
        write_to_file(python_code)
        print(f"The code for '{chosen_program}' has been written to '{code_file}'.")

        # Execute the generated Python code
        print("Running the program..")
        try:
            subprocess.run([sys.executable, code_file], stdout = subprocess.PIPE, stderr = subprocess.PIPE, check=True)
            print("The program executed successfully.")
            print(f"Python code executed successfully (in {attempts} attempts)")
            subprocess.call(["open", "generatedcode.py"])
            break #the code was executed and opened. superpythoncoder finished.
            # Print indicating successful execution
        except (subprocess.CalledProcessError, Exception) as error:
            # Handle subprocess errors or other unexpected exceptions
            # print(f"Error during subprocess execution: {error}")
            # might still be none
            error_description = error.stderr if error.stderr else None
            print(f"attempt number {attempts} has failed!\nError running generated code!\n")
            # print(f"attempt number {attempts} has failed!\nError running generated code! Error:\n{error_description}\n")

            # Sends the error to ChatGPT for fixing, referencing the original code request
            attempts += 1
            messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": f"I encountered an error: {error_description} while generating python code for '{requested_code_description}'. Here is the code you should fix:{python_code}. Make sure to write the whole corrected code when answering. Also, ensure the required modules are installed before running the script using the following lines of code:\n\nimport subprocess\nsubprocess.run(['pip', 'install', 'required_module'], check=True),you can only use 1 pyhton snippet in your answer."
    }
]

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            fixed_generated_code = response.choices[0].message.content
            generated_code = fixed_generated_code



    if attempts == 6:
        print("Code generation FAILED.")

if __name__ == "__main__":
    main()
