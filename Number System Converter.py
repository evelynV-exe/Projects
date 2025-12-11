def detect_base(numStr):
    #clear the decimal number and uppercase everything
    num = numStr.replace(".", "").upper()

    #set of number systems
    bases = {
        2: set("01"),
        8: set("01234567"),
        10: set("0123456789"),
        16: set("0123456789ABCDEF")
    }

    #what base user enter in
    for base in (2, 8, 10, 16):
        if all(ch in bases[base] for ch in num):
            return base
    
    raise ValueError("Invalid number for bases 2, 8, 10, or 16.")

#to base 2
def toBinary(x):
    intPart = int(x)
    fracPart = x - intPart

    binaryInt = bin(intPart)[2:]

    #convert the decimal part
    binaryFrac = ""
    for _ in range(12):
        fracPart *= 2
        bit = int(fracPart)
        binaryFrac += str(bit)
        fracPart -= bit
    return binaryInt + "." + binaryFrac


#base 8
def toOctal(x):
    intPart = int(x)
    fracPart = x - intPart

    octInt = oct(intPart)[2:]

    octFrac = ""
    for _ in range(12):
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
    for _ in range(12):
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

user_number = input("Enter a number in any base (2, 8, 10, 16): ")

base = detect_base(user_number)
decimalVal = toDecimal(user_number, base)

print("-------------Converter-------------")
print(f"Input: {user_number}")
print(f"Detected base: {base}")

print("Base 10: ", decimalVal)
print("Base 2: ", trimFraction(toBinary(decimalVal)))
print("Base 8: ", trimFraction(toOctal(decimalVal)))
print("Base 16: ", trimFraction(toHex(decimalVal)))
