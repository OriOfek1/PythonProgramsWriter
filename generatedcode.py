def is_palindrome(number):
    str_number = str(number)
    reversed_number = str_number[::-1]
    return str_number == reversed_number

# Unit tests
def test_is_palindrome():
    assert is_palindrome(12321) == True
    assert is_palindrome(12345) == False
    assert is_palindrome(121) == True
    assert is_palindrome(98789) == True
    assert is_palindrome(123421) == False

test_is_palindrome()
