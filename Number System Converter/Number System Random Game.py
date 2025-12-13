import random

def isValid(numStr, base):
    #clear the decimal number and uppercase everything
    num = numStr.replace(".", "").upper()

    #set of number systems
    bases = {
        2: set("01"),
        8: set("01234567"),
        10: set("0123456789"),
        16: set("0123456789ABCDEF")
    }
    
    return all(ch in bases[base] for ch in num)

#to base 2
def toBinary(x):
    intPart = int(x)
    fracPart = x - intPart

    binaryInt = bin(intPart)[2:]

    #convert the decimal part
    binaryFrac = ""
    for _ in range(16):
        fracPart *= 2
        bit = int(fracPart)
        binaryFrac += str(bit)
        fracPart -= bit
    return binaryInt + "." + binaryFrac.ljust(4, "0")


#base 8
def toOctal(x):
    intPart = int(x)
    fracPart = x - intPart

    octInt = oct(intPart)[2:]

    octFrac = ""
    for _ in range(4):
        fracPart *= 8
        digit = int(fracPart)
        octFrac += str(digit)
        fracPart -= digit

    return octInt + "." + octFrac

#to base 10
def toDecimal(numStr, base):
    decFrac = 0
    #check for the decimal
    if "." not in numStr:
        return int(numStr, base)

    intPart, fracPart = numStr.split(".")

    decInt = int(intPart, base)
    for i, digit in enumerate(fracPart, start=1):
        decFrac += int(digit, base) * base**-(i)
    
    return decInt + decFrac

#base 16
def toHex(x):
    intPart = int(x)
    fracPart = x - intPart

    hexInt = format(intPart, "X")

    hexFrac = ""
    for _ in range(4):
        fracPart *= 16
        digit = int(fracPart)
        hexFrac += format(digit, "X")
        fracPart -= digit

    return hexInt + "." + hexFrac

def trimFraction(resultStr):
    if "." not in resultStr:
        return resultStr

    intPart, fracPart = resultStr.split(".")

    fracPart = fracPart.rstrip("0")

    if fracPart == "":
        return intPart
    
    return intPart + "." + fracPart

bases = [2, 8, 10, 16]
MAX_INT = 9999
userRound = 0
score = 0
incorrectScore = 0

while True:
    #random the number and base
    randBase = random.choice(bases)
    randInt = random.randint(1, MAX_INT)
    places = random.random(1, 7)
    randFrac = round(random.random(), places)
    randNum = randInt + randFrac

    if randBase == 10:
        numStr = str(randNum)
    elif randBase == 2:
        numStr = toBinary(randNum)
    elif randBase == 8:
        numStr = toOctal(randNum)
    elif randBase == 16:
        numStr = toHex(randNum)

    #print the numbers out for user to convert
    print("---------------------------Welcome!-------------------------")
    print("Try to convert the number! To the base that it asks!")
    print(f"Round: {userRound}")
    print(f"Your number is {numStr}.\nBase: {randBase}\n")

    decimalVal = toDecimal(numStr, randBase)

    correct = {
        10: str(round(decimalVal, 4)),
        2: toBinary(decimalVal),
        8: toOctal(decimalVal),
        16: toHex(decimalVal)
    }

    for base in bases:
        if base == randBase:
            continue

        userAns = input(f"Conver to Base {base}: ")
        userRound += 1

        if userAns == correct[base]:
            print(f"Base {base} corrected!!!!!")
            score += 10
        else:
            print(f"Base {base} incorrect!!!!!!!!!!!!")
            print(f"Correct: {correct[base]}")
            incorrectScore += 1

    if incorrectScore > 0:
        print("\nYou really bad at this huh? Try harder.")

    print(f"\nYour score: {score}")

    again = input("\nDo you want another round? {y/n}: ").lower()

    if again != "y":
        print("Good job. You still sucks at it. :P")
        break
