from sympy.logic.boolalg import SOPform, POSform
from sympy import symbols, And, Or, Not
from itertools import product

#grey code
def greyCode(n):
    return [i ^ (i >> 1) for i in range(2**n)]

#Turn the binary into str
def toBinaryStr(num, bits):
    return format(num, f'0{bits}b')

#layout for Karnaugh Map for three variables
def kMapgenerator(numVars, values, mode="min"):
    """
    Docstring for kMapgenerator
    
    numVars: numbers of the variables that user entered (3 or 4)
    values: list of minterms or maxterms
    mode: min -> values are minterms (mark 1s)
          max -> values are maxterms (mark 0s)
    """

    if numVars == 3:
        rowBits, colsBits = 1, 2
        rowLabelName, ColLabelName = "C", "AB"
    elif numVars == 4:
        rowBits, colsBits = 2, 2
        rowLabelName, ColLabelName = "CD", "AB"
    
    rowOrder = greyCode(rowBits)
    colOrder = greyCode(colsBits)

    print(f"Rows Grey ({rowLabelName}): ", [toBinaryStr(r, rowBits) for r in rowOrder])
    print(f"Cols Grey ({ColLabelName}): ", [toBinaryStr(c, colsBits) for c in colOrder])
    print()

    #column header
    header = "     " + " ".join([toBinaryStr(c, colsBits) for c in colOrder])
    print(header)

    #Generate the grid
    for r in rowOrder:
        rowLabel = toBinaryStr(r, rowBits)
        rowCells = []
        for c in colOrder:
            colLabel = toBinaryStr(c, colsBits)
            idx = int(colLabel + rowLabel, 2)
            
            # Mark 1 or 0 depends on the mode
            if mode == "min":
                cell = "1" if idx in values else " "
            elif mode == "max":
                cell = "0" if idx in values else " "
            rowCells.append(cell.ljust(2))

        print(rowLabel, "|", " ".join(rowCells))
    
def boolToAlgebra(expr):
    if expr.is_Symbol:
        return str(expr)
    elif expr.func == Not:
        return boolToAlgebra(expr.args[0]) + "'"
    elif expr.func == And:
        return "".join(boolToAlgebra(arg) for arg in expr.args)
    elif expr.func == Or:
        return "(" + " + ".join(boolToAlgebra(arg) for arg in expr.args) + ")"
    else:
        return str(expr)

#simplify the input for user
def simplifyFunctions(numVars, values, mode = "min"):
    vars = symbols('A B C D')[:numVars]
    allTerms = set(range(2**numVars))

    if mode == "min":
        simplified = SOPform(vars, values)
    elif mode == "max":
        minterms = sorted(allTerms - set(values))
        simplified = POSform(vars, minterms)
    else:
        raise ValueError("Mode must be 'min' or 'max'!!")
    
    return simplified, boolToAlgebra(simplified)

#Truth table for user to check the output
def truthTable(expr, numVars):
    vars = symbols('A B C D')[:numVars]
    print("\nTruth Table!")
    print(" ".join([str(v) for v in vars]) + " | F")
    print("-" * (3 * numVars + 5))
    
    for combo in product([0, 1], repeat=numVars):
        assignment = dict(zip(vars, combo))
        result = int(bool(expr.subs(assignment)))
        print(" ".join(map(str, combo)) + f" | {result}")

#Ask user what they're input in the terminal
numVars = int(input("Enter number of variables (3 or 4): "))

choice = input("Choose your choice!\n m for Minterms or x for maxterms: ").lower()

if choice.startswith("m"):
    values = list(map(int, input("Enter minterms separated by spaces: ").split()))
    kMapgenerator(numVars, values, mode="min")
    simplified, algebraic = simplifyFunctions(numVars, values, mode="min")
    print(f"Simplified SOP: ", algebraic)
    truthTable(simplified, numVars)
elif choice.startswith("x"):
    values = list(map(int, input("Enter maxterms separated by spaces: ").split()))
    kMapgenerator(numVars, values, mode="max")
    simplified, algebraic = simplifyFunctions(numVars, values, mode="max")
    print(f"Simplified POS: ", algebraic)
    truthTable(simplified, numVars)
else:
    raise ValueError("Error! Try again!")
