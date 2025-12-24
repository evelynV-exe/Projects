from sympy.logic.boolalg import SOPform, POSform
from sympy import symbols, And, Or, Not

# Grey code generator
def greyCode(n):
    return [i ^ (i >> 1) for i in range(2**n)]

# Binary string formatting
def toBinaryStr(num, bits):
    return format(num, f'0{bits}b')

# Karnaugh Map generator (3 or 4 variables)
def kMapgenerator(numVars, values, dontcares=None, mode="min"):
    if dontcares is None:
        dontcares = []

    if numVars == 3:
        rowBits, colsBits = 1, 2
        rowLabelName, ColLabelName = "C", "AB"
    elif numVars == 4:
        rowBits, colsBits = 2, 2
        rowLabelName, ColLabelName = "CD", "AB"
    else:
        raise ValueError("Only 3 or 4 variables supported")

    rowOrder = greyCode(rowBits)
    colOrder = greyCode(colsBits)

    print(f"Rows Grey ({rowLabelName}): ", [toBinaryStr(r, rowBits) for r in rowOrder])
    print(f"Cols Grey ({ColLabelName}): ", [toBinaryStr(c, colsBits) for c in colOrder])
    print()

    header = "     " + " ".join([toBinaryStr(c, colsBits) for c in colOrder])
    print(header)

    for r in rowOrder:
        rowLabel = toBinaryStr(r, rowBits)
        rowCells = []
        for c in colOrder:
            colLabel = toBinaryStr(c, colsBits)
            idx = int(colLabel + rowLabel, 2)

            if idx in dontcares:
                cell = "d"
            elif mode == "min":
                cell = "1" if idx in values else " "
            elif mode == "max":
                cell = "0" if idx in values else " "
            rowCells.append(cell.ljust(2))

        print(rowLabel, "|", " ".join(rowCells))

# Convert Sympy expression to algebraic string
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

# Simplify function using SOP/POS
def simplifyFunctions(numVars, values, dontcares=None, mode="min"):
    vars = symbols('A B C D')[:numVars]
    allTerms = set(range(2**numVars))

    if dontcares is None:
        dontcares = []

    if mode == "min":
        simplified = SOPform(vars, values, dontcares)
    elif mode == "max":
        minterms = sorted(allTerms - set(values))
        safe_dontcares = [dc for dc in dontcares if dc not in minterms]
        simplified = POSform(vars, minterms, safe_dontcares)
    else:
        raise ValueError("Mode must be 'min' or 'max'!!")

    return simplified, boolToAlgebra(simplified)

# Convert cells to term
def cellsToTerm(cells, numVars):
    if numVars == 3:
        row_bits, col_bits = 1, 2
    elif numVars == 4:
        row_bits, col_bits = 2, 2
    else:
        raise ValueError("Only 3 or 4 variables supported")

    rows, cols = 2 ** row_bits, 2 ** col_bits
    row_order = [i ^ (i >> 1) for i in range(2 ** row_bits)]
    col_order = [i ^ (i >> 1) for i in range(2 ** col_bits)]

    bitstrings = []
    for cell in cells:
        r = cell // cols
        c = cell % cols
        r_label = format(row_order[r], f'0{row_bits}b')
        c_label = format(col_order[c], f'0{col_bits}b')
        bitstrings.append(c_label + r_label)

    term = []
    for i in range(numVars):
        bits = {b[i] for b in bitstrings}
        if len(bits) == 1:
            var = chr(65 + i)
            bit = next(iter(bits))
            term.append(var if bit == '1' else var + "'")

    return ''.join(term) if term else '1'

# Build grid
def buildGrid(numVars, values, dontcares):
    if numVars == 3:
        row_bits, col_bits = 1, 2
    elif numVars == 4:
        row_bits, col_bits = 2, 2
    else:
        raise ValueError("Only 3 or 4 variables supported")

    rows, cols = 2 ** row_bits, 2 ** col_bits
    row_order = greyCode(row_bits)
    col_order = greyCode(col_bits)

    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    marked = set(values) | set(dontcares)

    for r_idx, r in enumerate(row_order):
        r_label = format(r, f'0{row_bits}b')
        for c_idx, c in enumerate(col_order):
            c_label = format(c, f'0{col_bits}b')
            idx = int(c_label + r_label, 2)
            grid[r_idx][c_idx] = 1 if idx in marked else 0

    return grid, rows, cols

# Find largest groups
def largestGroups(numVars, values, dontcares=None):
    if dontcares is None:
        dontcares = []
    grid, rows, cols = buildGrid(numVars, values, dontcares)
    groups = []

    # Full rows/cols
    for r in range(rows):
        if all(grid[r][c] == 1 for c in range(cols)):
            cells = [r * cols + c for c in range(cols)]
            groups.append((cellsToTerm(cells, numVars), cells))
    for c in range(cols):
        if all(grid[r][c] == 1 for r in range(rows)):
            cells = [r * cols + c for r in range(rows)]
            groups.append((cellsToTerm(cells, numVars), cells))

    # 2x2 blocks
    for r in range(rows):
        for c in range(cols):
            block = [
                r * cols + c,
                r * cols + ((c + 1) % cols),
                ((r + 1) % rows) * cols + c,
                ((r + 1) % rows) * cols + ((c + 1) % cols),
            ]
            if all(grid[cell // cols][cell % cols] == 1 for cell in block):
                groups.append((cellsToTerm(block, numVars), block))

    # Adjacent pairs
    for r in range(rows):
        for c in range(cols):
            pairH = [r * cols + c, r * cols + ((c + 1) % cols)]
            if all(grid[cell // cols][cell % cols] == 1 for cell in pairH):
                groups.append((cellsToTerm(pairH, numVars), pairH))

            pairV = [r * cols + c, ((r + 1) % rows) * cols + c]
            if all(grid[cell // cols][cell % cols] == 1 for cell in pairV):
                groups.append((cellsToTerm(pairV, numVars), pairV))

    # Singletons
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                cell = r * cols + c
                groups.append((cellsToTerm([cell], numVars), [cell]))

    # Deduplicate
    uniq = {}
    for term, cells in groups:
        key = tuple(sorted(cells))
        if key not in uniq:
            uniq[key] = (term, cells)

    return list(uniq.values())

def filterPrimeImplicants(groups):
    prime_group = []
    for i, (term_i, cells_i) in enumerate(groups):
        is_subset = False
        for j, (_, cells_j) in enumerate(groups):
            if i != j and set(cells_i).issubset(set(cells_j)):
                is_subset = True
                break
        if not is_subset:
            prime_group.append((term_i, cells_i))
    return prime_group

# CLI
numVars = int(input("Enter number of variables (3 or 4): "))
choice = input("Choose your choice!\n m for Minterms or x for Maxterms: ").lower()
dcChoice = input("Do you have don't cares? (y/n): ").lower()

dontcares = list(range(10, 16)) if dcChoice.startswith("y") else []

if choice.startswith("m"):
    values = list(map(int, input("Enter minterms separated by spaces: ").split()))
    kMapgenerator(numVars, values, dontcares, mode="min")
    simplified, algebraic = simplifyFunctions(numVars, values, dontcares, mode="min")
    print(f"Simplified SOP: {algebraic}\n")

    groups = largestGroups(numVars, values, dontcares)
    prime_groups = filterPrimeImplicants(groups)
    for term, cells in prime_groups:
        print(f"Term {term} covers squares {cells}")
elif choice.startswith("x"):
    values = list(map(int, input("Enter maxterms separated by spaces: ").split()))
    kMapgenerator(numVars, values, dontcares, mode="max")
    simplified, algebraic = simplifyFunctions(numVars, values, dontcares, mode="max")
    print(f"Simplified POS: {algebraic}\n")

    # For grouping, we need to look at the minterms (the complement of maxterms)
    minterms_for_grouping = sorted(set(range(2 ** numVars)) - set(values))
    groups = largestGroups(numVars, minterms_for_grouping, dontcares)
    prime_groups = filterPrimeImplicants(groups)
    for term, cells in prime_groups:
        print(f"Term {term} covers squares {cells}")
else:
    raise ValueError("Error! Try again!")
   
