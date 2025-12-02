def rotateDial(instruction, position):
    # Part 1: Simple rotation
    direction, clicks = instruction[0], int(instruction[1:])
    if direction == 'L':
        position = (position - clicks) % 100
    elif direction == 'R':
        position = (position + clicks) % 100
    return position

def newRotateDial(instr, position):
    direction = -1 if instr[0] == 'L' else 1
    steps = int(instr[1:])
    
    # Count full cycles
    full_cycles, remainder = divmod(steps, 100)
    crossings = full_cycles
    
    # Count crossings in remaining steps
    for i in range(1, remainder + 1):
        if (position + direction * i) % 100 == 0:
            crossings += 1
    
    # Update position
    position = (position + direction * steps) % 100
    return position, crossings


def getRealPassword(file, pos = 50):
    # Part 1: Simple rotation
    realPass = 0
    with open(file, 'r') as file:
        for instr in file.readlines():
            pos = rotateDial(instr, pos)
            if pos==0: 
                realPass+=1
    return realPass

def method0x434C49434B(file, pos=50):
    realPass = 0
    with open(file, 'r') as f:
        for instr in f:
            instr = instr.strip()
            if not instr:
                continue
            pos, crossings = newRotateDial(instr, pos)
            realPass += crossings
    return realPass

def test_with_example():
    example = "L68,L30,R48,L5,R60,L55,L1,L99,R14,L82"
    pos = 50
    total = 0
    for instr in example.split(','):
        instr = instr.strip()
        if not instr:
            continue
        pos, crossings = newRotateDial(instr, pos)
        total += crossings
        print(f"{instr}: crossings={crossings}, new_pos={pos}, total={total}")
    print(f"Example answer: {total} (expected: 6)")
    return total

if __name__ == "__main__":
    # Part 1: Simple rotation
    print('Actual password:', getRealPassword('Day 1/input.txt', 50))
    # Part 2: Count crossings of 0
    print('Method 0x434C49434B password:', method0x434C49434B('Day 1/input.txt', 50))
    test_with_example()