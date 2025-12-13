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

while True:
    randBase = random.choice(bases)
    randInt = random.randint(1, MAX_INT)
    randFrac = random.random()
    randNum = randInt + randFrac

    if randBase == 10:
        numStr = str(randNum)
    elif randBase == 2:
        numStr = toBinary(randNum)
    elif randBase == 8:
        numStr = toOctal(randNum)
    elif randBase == 16:
        numStr = toHex(randNum)

    print(f"\nTry to Convert!\nYour number is {numStr}.\nBase: {randBase}\n")

    decimalVal = toDecimal(numStr, randBase)

    print("Base 10: ", round(decimalVal, 4))
    print("Base 2: ", toBinary(decimalVal))
    print("Base 8: ", toOctal(decimalVal))
    print("Base 16: ", toHex(decimalVal))

    again = input("\nDo you want another round? {y/n}: ").lower()

    if again != "y":
        print("Good job practicing. You still sucks at it. :]")
        break