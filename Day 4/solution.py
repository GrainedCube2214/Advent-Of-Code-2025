def isRemoveable(grid, i, j, threshold=4):
    n8_dirs = [((-1, -1)), ((-1, 0)), ((-1, 1)), ((0, -1)), ((0, 1)), ((1, -1)), ((1, 0)), ((1, 1))]
    count = 0
    for d in n8_dirs:
        ni, nj = i + d[0], j + d[1]
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
            if grid[ni][nj] == '@':
                count += 1
                
    if count < threshold: return True
    return False

def countRemoveable(grid, threshold=4, remove=False):
    removeable = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '@' and isRemoveable(grid, i, j, threshold):
                removeable += 1
                if remove:
                    grid[i][j] = '.'
    return removeable

def gridFromFile(file):
    grid = []
    with open(file, 'r') as f:
        for line in f:
            grid.append(list(line.strip()))
    return grid

def test_countRemoveable():
    test_grid = [['.', '.', '@', '@', '.', '@', '@', '@', '@', '.'], 
                 ['@', '@', '@', '.', '@', '.', '@', '.', '@', '@'], 
                 ['@', '@', '@', '@', '@', '.', '@', '.', '@', '@'], 
                 ['@', '.', '@', '@', '@', '@', '.', '.', '@', '.'], 
                 ['@', '@', '.', '@', '@', '@', '@', '.', '@', '@'], 
                 ['.', '@', '@', '@', '@', '@', '@', '@', '.', '@'], 
                 ['.', '@', '.', '@', '.', '@', '.', '@', '@', '@'], 
                 ['@', '.', '@', '@', '@', '.', '@', '@', '@', '@'], 
                 ['.', '@', '@', '@', '@', '@', '@', '@', '@', '.'], 
                 ['@', '.', '@', '.', '@', '@', '@', '.', '@', '.']]
    result = countRemoveable(test_grid, threshold=4)
    print(f"Test countRemoveable result: {result} (expected: 13)")
    
def multipass_countRemoveable(grid, threshold=4):
    total_removeable = 0
    while True:
        current_removeable = countRemoveable(grid, threshold, remove=True)
        if current_removeable == 0:
            break
        total_removeable += current_removeable

    return total_removeable

def test_multipass_countRemoveable():
    test_grid = [['.', '.', '@', '@', '.', '@', '@', '@', '@', '.'], 
                 ['@', '@', '@', '.', '@', '.', '@', '.', '@', '@'], 
                 ['@', '@', '@', '@', '@', '.', '@', '.', '@', '@'], 
                 ['@', '.', '@', '@', '@', '@', '.', '.', '@', '.'], 
                 ['@', '@', '.', '@', '@', '@', '@', '.', '@', '@'], 
                 ['.', '@', '@', '@', '@', '@', '@', '@', '.', '@'], 
                 ['.', '@', '.', '@', '.', '@', '.', '@', '@', '@'], 
                 ['@', '.', '@', '@', '@', '.', '@', '@', '@', '@'], 
                 ['.', '@', '@', '@', '@', '@', '@', '@', '@', '.'], 
                 ['@', '.', '@', '.', '@', '@', '@', '.', '@', '.']]
    result = multipass_countRemoveable(test_grid, threshold=4)
    print(f"Test multipass_countRemoveable result: {result} (expected: 43)")

if __name__ == "__main__":
    # test_countRemoveable()
    grid = gridFromFile('Day 4/input.txt')
    # print(countRemoveable(grid, threshold=4))
    # test_multipass_countRemoveable()
    print(multipass_countRemoveable(grid, threshold=4))