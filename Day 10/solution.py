import re
from itertools import product

try:
    from z3 import *
    HAS_Z3 = True
except ImportError:
    HAS_Z3 = False
    print("Error: z3 not found. Install with: pip install z3-solver")
    exit(1)

def line_config(line, part2=False):
    # Parse Lights (Part 1 Target)
    raw_config_str = line[line.index('[')+1:line.index(']')]
    lights_target = [1 if c == '#' else 0 for c in raw_config_str]
    
    # Parse Joltages (Part 2 Target)
    raw_jolt_match = re.search(r'\{([\d,]+)\}', line)
    jolts_target = [int(x) for x in raw_jolt_match.group(1).split(',')] if raw_jolt_match else []

    # Parse Buttons
    button_matches = re.findall(r'\(([\d,]+)\)', line)
    buttons = []
    for m in button_matches:
        buttons.append([int(x) for x in m.split(',')])

    num_buttons = len(buttons)

    # Part 1: Light Toggling (brute force is sufficient)
    if not part2:
        num_lights = len(lights_target)
        min_presses = float('inf')
        
        for press_pattern in product([0, 1], repeat=num_buttons):
            current_count = sum(press_pattern)
            if current_count >= min_presses: 
                continue

            state = [0] * num_lights
            for b_idx, pressed in enumerate(press_pattern):
                if pressed:
                    for light_idx in buttons[b_idx]:
                        state[light_idx] ^= 1
            
            if state == lights_target:
                min_presses = current_count
        
        return min_presses if min_presses != float('inf') else 0

    # Part 2: Joltage using Z3
    else:
        num_counters = len(jolts_target)
        
        # Create Z3 optimizer
        opt = Optimize()
        
        # Create integer variables for button presses
        presses = [Int(f'b_{i}') for i in range(num_buttons)]
        
        # Add non-negativity constraints
        for p in presses:
            opt.add(p >= 0)
        
        # Add counter constraints
        for c_idx in range(num_counters):
            # Sum of effects on this counter must equal target
            counter_sum = 0
            for b_idx in range(num_buttons):
                if c_idx in buttons[b_idx]:
                    counter_sum += presses[b_idx]
            opt.add(counter_sum == jolts_target[c_idx])
        
        # Minimize total presses
        opt.minimize(Sum(presses))
        
        # Solve
        if opt.check() == sat:
            model = opt.model()
            return sum(model[p].as_long() for p in presses)
        
        return 0

def factory_pt1(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    total_presses = 0
    for line in lines:
        total_presses += line_config(line.strip())
    return total_presses

def factory_pt2(file):
    # print("Starting Part 2 Processing using Z3 solver...")
    with open(file, 'r') as f:
        lines = f.readlines()
    # print("File read complete. Processing lines...")
    
    total_presses = 0
    total_lines = len(lines)
    
    import time
    start_time = time.time()
    
    for line_num, line in enumerate(lines, 1):
        line_start = time.time()
        result = line_config(line.strip(), part2=True)
        line_time = time.time() - line_start
        total_presses += result
        
        # Show progress every 10 lines or if slow
        if line_num % 10 == 0 or line_time > 0.5:
            elapsed = time.time() - start_time
            avg_time = elapsed / line_num
            eta = avg_time * (total_lines - line_num)
            # print(f"Line {line_num}/{total_lines}: result={result}, "
                #   f"time={line_time:.3f}s, total={total_presses}, "
                #   f"ETA={eta:.1f}s")
    
    # print(f"\nCompleted all {total_lines} lines in {time.time() - start_time:.2f}s")
    return total_presses

def test_pt1():
    t = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    with open('test_input.txt', 'w') as f:
        f.write(t)

    ans = factory_pt1('test_input.txt')
    assert ans == 7, f"Test Pt1: {ans}, expected 7"
    print(f"Test Pt1: PASSED, got {ans}")
    
    import os
    os.remove('test_input.txt')

def test_pt2():
    t = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    
    with open('test_input.txt', 'w') as f:
        f.write(t)

    ans = factory_pt2('test_input.txt')
    assert ans == 33, f"Test Pt2: {ans}, expected 33"
    print(f"Test Pt2: PASSED, got {ans}")
    
    import os
    os.remove('test_input.txt')

if __name__ == "__main__":
    import time
    
    # print(f"Z3 solver loaded successfully\n")
    
    # start = time.time()
    test_pt1()
    # print(f"Test Pt1 finished in: {time.time() - start:.6f} seconds\n")
    
    # start = time.time()
    result = factory_pt1('Day 10/input.txt')
    print(f"Part 1 Result: {result}")
    # print(f"Part 1 finished in: {time.time() - start:.6f} seconds\n")

    # start = time.time()
    test_pt2()
    # print(f"Test Pt2 finished in: {time.time() - start:.6f} seconds\n")
    
    # start = time.time()
    result = factory_pt2('Day 10/input.txt')
    print(f"Part 2 Result: {result}")
    # print(f"Part 2 finished in: {time.time() - start:.6f} seconds")