def rangereader(file):
    r = []
    with open(file, 'r') as f:
        for line in f:
            if line!='\n':
                start, end = map(int, line.strip().split('-'))
                r.append(range(start, end + 1))
            else: return r
    return r

def idReader(file):
    ids = []
    start = False
    with open(file, 'r') as f:
        for line in f:
            if line!='\n' and not start:
                continue
            elif line=='\n':
                start = True
            else:
                ids.append(int(line.strip()))
    return ids

def idsInRange(ids, ranges):
        c=0
        breakout = False
        for id in ids:
            for r in ranges:
                if id in r and not breakout:
                    # print(f"ID {id} is in range {r.start}-{r.stop-1}")
                    c+=1
                    breakout = True
                    continue 
            breakout = False
                
        return c
    
def totalFreshIDs(ranges): # bruteforce, too slow
    total = 0
    s = set()
    for r in ranges:
        for i in r:
            s.add(i)
    return len(s)

def rangeMerger(ranges):
    sorted_ranges = sorted(ranges, key=lambda x: x.start)
    merged = []
    for current in sorted_ranges:
        if not merged:
            merged.append(current)
        else:
            last = merged[-1]
            if current.start <= last.stop:
                merged[-1] = range(last.start, max(last.stop, current.stop))
            else:
                merged.append(current)
    return merged

def totalFreshIDsOptimized(ranges):
    merged_ranges = rangeMerger(ranges)
    total = 0
    for r in merged_ranges:
        total += (r.stop - r.start)
    return total
        
    
def test_part1():
    ranges = [range(3,6), range(10,15), range(16,21), range(12,19)]
    ids = [1,5,8,11,17,32]
    print(idsInRange(ids, ranges))  # Expected output: 3
    
def test_part2():
    ranges = [range(3,6), range(10,15), range(16,21), range(12,19)]
    print(totalFreshIDs(ranges))  # Expected output: 14
    
if __name__ == "__main__":
    # test_part1()
    ranges = rangereader('Day 5/input.txt')
    # ids = idReader('Day 5/input.txt')
    # print(idsInRange(ids, ranges))
    # test_part2()
    print(totalFreshIDsOptimized(ranges))