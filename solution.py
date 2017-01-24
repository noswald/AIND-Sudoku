assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    # return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    naked_pot = [box for box in values.keys() if len(values[box]) == 2]
    naked_pots = cross(naked_pot,naked_pot)
    naked_pots = [box for box in naked_pots if box[0:2]!=box[2:4] and values[box[0:2]]==values[box[2:4]] and (box[0]==box[2] or box[1]==box[3])]
    for i in naked_pots:
        #check row units
        if i[0] == i[2]:
            rowT = [r for r in row_units if i[0:2] in r][0]
            rowT = [box for box in rowT if box!= i[0:2] and box!=i[2:4]]
            digits = values[i[0:2]]
            for r in rowT:
                for d in digits:
                    values[r] = values[r].replace(d,'')
                    assign_value(values, r, values[r])
        #check col units
        if i[1] == i[3]:
            colT = [c for c in column_units if i[0:2] in c][0]
            colT = [box for box in colT if box!= i[0:2] and box!=i[2:4]]
            digits = values[i[0:2]]
            for c in colT:
                for d in digits:
                    values[c] = values[c].replace(d,'')
                    assign_value(values, c, values[c])
    return values


    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

rows = 'ABCDEFGHI'
cols = '123456789'    
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
boxes = cross(rows,cols)
row_units = [cross(r,cols) for r in rows]
column_units = [cross(rows,c) for c in cols]
square_units = [cross(rs,cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[r + cols[rows.index(r)] for r in rows],[r + cols[sorted(rows,reverse=True).index(r)] for r in rows]]
unitlist = row_units + column_units + square_units + diag_units
#unitlist = row_units + column_units + square_units
units = dict((s,[u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
def grid_values(grid):
    "Convert grid into a dict of {square: char} with '.' for empties."
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
            assign_value(values, peer, values[peer])
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
                assign_value(values, dplaces[0], values[dplaces[0]])
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        # assign_value(values, box, value)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
def solve(grid):
    values = grid_values(grid)
    values = search(values)
    return values
def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
            
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
