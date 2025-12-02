def rangemaker(file):
    with open(file, 'r') as f:
        ranges = f.read().split(',')
    for i in range(len(ranges)):
        a, b = map(int, ranges[i].split('-'))
        ranges[i] = (a, b)
    return ranges

def validateID_pt1(ranges):
    invalid = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            l  = len(str(i))
            if l%2!=0: continue
            half = l//2
            left = str(i)[:half]
            right = str(i)[half:]
            if left == right:
                invalid += i
    return invalid

def validateID_pt2(ranges):
    invalid = 0
    for r in ranges:
        for i in range(r[0], r[1] + 1):
            s = str(i)
            l = len(s)
            
            # Check all possible pattern lengths
            is_invalid = False
            for pattern_len in range(1, l // 2 + 1):
                # Pattern length must divide evenly into total length
                if l % pattern_len == 0:
                    repetitions = l // pattern_len
                    if repetitions >= 2:  # Must repeat at least twice
                        pattern = s[:pattern_len]
                        # Check if the entire string is just this pattern repeated
                        if s == pattern * repetitions:
                            is_invalid = True
                            break
            
            if is_invalid:
                invalid += i
    
    return invalid

if __name__ == "__main__":
    ranges = rangemaker("Day 2/input.txt")
    
    # Part 1
    result = validateID_pt1(ranges)
    print("Part 1:", result)
    
    # Part 2
    result = validateID_pt2(ranges)
    print("Part 2:", result)