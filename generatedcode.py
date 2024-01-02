import re


def calculator(expression):
    expression = expression.replace(' ', '')

    if not re.match(r'^[0-9+\-*/().]+$', expression):
        return "Invalid input"

    if not re.match(r'^[0-9]', expression):
        return "Start expression with a number"

    try:
        result = eval(expression)
        return result
    except:
        return "Invalid expression"


# Unit tests
assert calculator("1 + 2 * 3") == 7
assert calculator("4 / 2 + 3 - 1") == 4
assert calculator("(5 - 2) * 6") == 18
assert calculator("10 / (2 + 3)") == 2
assert calculator("2 ** 3 - 1") == 7
