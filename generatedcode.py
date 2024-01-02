import sys

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        return "Cannot divide by zero"

def calculator():
    while True:
        num1 = float(input("Enter first number: "))
        if num1 == "q":
            sys.exit()
        operation = input("Enter operation (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if operation == "+":
            print("Result:", add(num1, num2))
        elif operation == "-":
            print("Result:", subtract(num1, num2))
        elif operation == "*":
            print("Result:", multiply(num1, num2))
        elif operation == "/":
            print("Result:", divide(num1, num2))
        else:
            print("Invalid operation")

calculator()
