import random

def convertNumber(num, base):
    if base == 2:
        return bin(num)[2::]
    elif base == 8:
        return oct(num)[2::]
    elif base == 10:
        return str(num)
    elif base == 16: 
        return hex(num)[2:].upper()

operations = ["+", "-", "*", "/"]
bases = [2, 8, 10, 16]
MAX_INT = 9999
score = 0
roundNum = 1

while True:

    randomBase = random.choice(bases)
    operation = random.choice(operations)

    if operation == "*" or operation == "/":
        randomInt1 = random.randint(1, 100)
        randomInt2 = random.randint(1, 100)
    else:
        randomInt1 = random.randint(1, MAX_INT)
        randomInt2 = random.randint(1, MAX_INT)

    if randomInt1 < randomInt2:
        randomInt1, randomInt2 = randomInt2, randomInt1

    num1 = convertNumber(randomInt1, randomBase)
    num2 = convertNumber(randomInt2, randomBase)

    print("------------------------Welcome!------------------------")
    print(f"Round: {roundNum}")
    print(f"Your first number: {num1}\nYour second number: {num2}\nBase: {randomBase}\nOperation: {operation}\nGood luck!")

    if operation == "+":
        result = randomInt1 + randomInt2
    elif operation == "-":
        result = randomInt1 - randomInt2
    elif operation == "*":
        result  = randomInt1 * randomInt2
    elif operation == "/":
        if randomInt2 == 0:
            result =  "Error."
        else:
            result = round(randomInt1/randomInt2)

    if isinstance(result, int):
        resultStr = convertNumber(result, randomBase)
    else:
        resultStr = result

    playerAnswer = input("\nEnter your answer in the chosen base: ")

    if playerAnswer.strip().upper() == resultStr.upper():
        print("CORRECT!!!!!!!")
        score += 10
    else:
        print(f"WRONGGGGGG!! The correct answer was {resultStr}")
        score -= 10

    print(f"Current score: {score}\n")
    roundNum += 1

    again = input("\nDo you want another round? (y/n): ").lower()
    if again != "y":
        print(f"Final score: {score}")
        print("Well... You did great. But you still sucks at it. :) BYE!")
        break