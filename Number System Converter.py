binary = "1110110.010111"

intPart, fracPart = binary.split('.')

#base 8
padLeft = (3 - len(intPart) % 3) %3
intPadded = '0' *padLeft + intPart

padRight = (3 - len(fracPart) % 3) %3
fracPadded = fracPart + '0' * padRight

octInt = ""
for i in range(0, len(intPadded), 3):
    group = intPadded[i:i+3]
    octInt += str(int(group, 2))

octFrac = ""
for i in range(0, len(fracPadded), 3):
    group = fracPadded[i:i+3]
    octFrac += str(int(group, 2))

fullOct = octInt + "." + octFrac

#to base 10
decInt = int(intPart, 2)
dexFrac = sum(int(bit) * 2**-(i+1) for i, bit in enumerate(fracPart))

dec = decInt + dexFrac

#base 16
pad = (4 - len(fracPart) % 4) % 4
fracPadded = fracPart + '0' * pad

hexInt = format(decInt, 'x')

hexDec = ""
for i in range(0, len(fracPadded), 4):
    group = fracPadded[i:i+4]
    value = int (group, 2)
    hexDigit = format(value, 'x')
    hexDec += hexDigit

fullHex = hexInt + "." + hexDec

print("---Base 2 to Base 8 to Base 16 converter---")

print(f"Binary numbers: {binary}")

print(f"Base 8: {fullOct}")
print(f"Base 10: {dec}")

print(f"Base 16: {fullHex}")
