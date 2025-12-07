def beamsplitter(file):
    with open(file, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    splits = 0

    start_col = None
    for col in range(len(lines[0])):
        if lines[0][col] == 'S':
            start_col = col
            break

    curr_beams = {start_col}

    for row in range(1, len(lines)):
        next_beams = set()
        for col in curr_beams:
            if col < 0 or col >= len(lines[row]):
                continue  # Beam went out of bounds

            if lines[row][col] == '.':
                next_beams.add(col)
            elif lines[row][col] == '^':
                splits += 1
                if col - 1 >= 0:
                    next_beams.add(col - 1)
                if col + 1 < len(lines[row]):
                    next_beams.add(col + 1)
        curr_beams = next_beams

    return splits

def test_beamsplitter():
    t = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

    with open('temp.txt', 'w') as f:
        f.write(t)

    result = beamsplitter('temp.txt')
    print(f"Result: {result}, Expected: 21")

    import os
    os.remove('temp.txt')
    return

def multiversal_beamsplitter(file):
    with open(file, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0

    start_col = lines[0].index('S')

    prev_row = [1] * cols
    curr_row = [0] * cols

    for r in range(rows - 1, -1, -1):
        curr_row = [0] * cols
        for c in range(cols):
            if lines[r][c] == '^':
                if c - 1 >= 0:
                    curr_row[c] += prev_row[c - 1]
                if c + 1 < cols:
                    curr_row[c] += prev_row[c + 1]
            elif lines[r][c] in '.S':
                curr_row[c] = prev_row[c]

        prev_row = curr_row

    return prev_row[start_col]

def test_multiversal_beamsplitter():
    t = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    with open('temp.txt', 'w') as f:
        f.write(t)
    result = multiversal_beamsplitter('temp.txt')
    print(f"Result: {result}, Expected: 40")
    import os
    os.remove('temp.txt')
    return

if __name__ == "__main__":
    # test_beamsplitter()
    # print(beamsplitter('Day 7/input.txt'))

    # test_multiversal_beamsplitter()
    print(multiversal_beamsplitter('Day 7/input.txt'))