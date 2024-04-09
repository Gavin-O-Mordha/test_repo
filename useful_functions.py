# Module of useful functions
# Author: Gavin Moore

def get_string(prompt):
    while True:
        answer = input(prompt)
        test_answer = answer.replace(" ", "")
        if len(test_answer)>0 and test_answer.isalpha():
            answer = answer.capitalize()
            break
        print("ERROR: only enter letters")
    return answer

def get_positive_integer(prompt: str):
    while True:
        try:
            number = int(input(prompt))
            if 0 <= number:
                break
            else:
                number = int(input("Enter a positive number: "))
        except ValueError:
            print('Enter a numeric value')
    return number

def get_negative_integer(prompt: str):
    while True:
        try:
            number = int(input(prompt))
            if 0 >= number:
                break
            else:
                number = int(input("Enter a positive number: "))
        except ValueError:
            print('Enter a numeric value')
    return number