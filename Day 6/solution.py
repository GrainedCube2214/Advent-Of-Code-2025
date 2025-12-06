def parser(file):
    with open(file, 'r') as f:
        rows = []
        for line in f.readlines():
            line = line.strip().split(' ') 
            numbers = [int(i) for i in line if i.isnumeric()]
            if '+' in line or '*' in line:
                for i in line:
                    if i in ['+','*']:
                        numbers.append(i)
            rows.append(numbers)
    return rows

def worksheet_solver(rows):
    results = []
    
    for i in range(len(rows[0])):
        column = []
        for j in range(len(rows)):
            column.append(rows[j][i])
        op = column.pop()
        if op=='+': results.append(sum(column))
        elif op=='*':
            ans = 1
            for _ in column:
                ans*= _
            results.append(ans)
    return sum(results)

def test_worksheet_solver():
    test = [[123, 328, 51, 64],[45, 64, 387, 23], [6,98,215,314],['*', '+', '*', '+']]
    print(worksheet_solver(test)) # Expected 4277556
    return

def parser_part2(file=None, sfile=None):
    if sfile:
        lines = sfile.strip().split('\n')
    else:
        with open(file, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    
    grid = []
    for line in lines:
        grid.append(list(line))
    
    columns = []
    max_len = max(len(row) for row in grid)
    
    for row in grid:
        while len(row) < max_len:
            row.append(' ')
    
    for i in range(max_len):
        column = []
        for row in grid:
            column.append(row[i])
        if any(c != ' ' for c in column):
            columns.append(column)
    
    return columns

def worksheet_solver_part2(columns):
    if not columns:
        return 0
    
    columns = columns[::-1]
    results = []
    stack = []
    
    for column in columns:
        temp_num = ''
        
        for char in column:
            if char.isdigit():
                temp_num += char
            elif char in ['+', '*']:
                if temp_num:
                    stack.append(int(temp_num))
                
                if stack:
                    if char == '+':
                        result = sum(stack)
                    else:  # char == '*'
                        result = 1
                        for num in stack:
                            result *= num
                    results.append(result)
                    stack = []
                temp_num = ''
        
        if temp_num:
            stack.append(int(temp_num))
    
    return sum(results)

def test_worksheet_solver_part2():
    sfile = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    
    columns = parser_part2(sfile=sfile)
    result = worksheet_solver_part2(columns)
    print(f"Test result: {result}")  # Expected 3263827
    
    if result == 3263827:
        print("✓ Test passed!")
    else:
        print(f"✗ Test failed. Expected 3263827, got {result}")
    
    return result

def solve_part2(file):
    columns = parser_part2(file=file)
    result = worksheet_solver_part2(columns)
    return result

if __name__ == "__main__":
    # test_worksheet_solver()
    # rows = parser(file='Day 6/input.txt')
    # print(worksheet_solver(rows))
    # test_worksheet_solver_part2()
    print(solve_part2(file='Day 6/input.txt'))

"""
Working:
def gridbuilder(sfile):
    lines = sfile.split('\n')
    grid = []
    for line in lines:
        grid.append(list(line))
        
    return grid

def gridprinter(grid):
    for row in grid:
        print(row)

sfile = \"""123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  \"""

def column_maker(grid):
    columns = []
    for i in range(len(grid[0])):
        column = []
        for row in grid:
            column.append(row[i])
        if any(c != ' ' for c in column):
            columns.append(column)
    return columns
print("Original Grid:")
gridprinter(gridbuilder(sfile))
print("\nColumns:")
columns = column_maker(gridbuilder(sfile))
for col in columns[::-1]:
    print(col)
    
def solver(columns):
    columns=columns[::-1]
    result = 0
    stack = []
    for i in columns:
        c = ''
        for j in i:
            if j.isdigit():
                c+=j
            elif j in ['+', '*']:
                stack.append(int(c))
                if j=='+':
                    print(' + '.join(map(str, stack)), '=', end=' ')
                    r = sum(stack)
                    print('=',r)
                elif j=='*':
                    print(' * '.join(map(str, stack)), '=', end=' ')
                    r=1
                    for _ in stack:
                        r*=_
                    print('=',r)
                result+=r
                stack = []
                c = ''
        if c!='':
            stack.append(int(c))
        print('----')
    print("Final Result:", result)
    return result
                
solver(columns)
"""