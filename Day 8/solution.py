def solve_playground(filename, max_connections=1000, verbose=False):
    boxes = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                x, y, z = map(int, line.strip().split(','))
                boxes.append((x, y, z))
    
    n = len(boxes)

    if verbose:
        print(f"[INFO] Loaded {n} junction boxes.")

    parent = list(range(n))
    size = [1] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x]) # Path compression
        return parent[x]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            if verbose:
                print(f"  [SKIP] {a} and {b} already in the same cluster.")
            return False 

        if size[ra] < size[rb]:
            ra, rb = rb, ra
        
        parent[rb] = ra
        size[ra] += size[rb]
        
        if verbose:
            print(f"  [MERGE] Connected {a} <-> {b}. New root: {ra}, size = {size[ra]}")
        return True

    edges = []
    for i in range(n):
        xi, yi, zi = boxes[i]
        for j in range(i + 1, n):
            xj, yj, zj = boxes[j]
            dist = (xi - xj)**2 + (yi - yj)**2 + (zi - zj)**2
            edges.append((dist, i, j))
            
    edges.sort()

    if verbose:
        print(f"[INFO] Sorted {len(edges)} edges. Processing top {max_connections}...")
    
    top_edges = edges[:max_connections]
    
    for idx, (dist, a, b) in enumerate(top_edges):
        if verbose and idx % 200 == 0:
             print(f"[KRUSKAL] Processing edge {idx+1}/{max_connections}")
        

        union(a, b)

    final_sizes = [size[i] for i in range(n) if parent[i] == i]
    final_sizes.sort(reverse=True)

    if verbose:
        print(f"[INFO] Top 3 cluster sizes: {final_sizes[:3]}")

    result = 1
    for s in final_sizes[:3]:
        result *= s

    return result

def test_solve_playground():
    import os
    t = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    
    filename = 'test_input.txt'
    with open(filename, 'w') as f:
        f.write(t)

    try:
        result = solve_playground(filename, max_connections=10, verbose=True)
        assert result == 40, f"Expected 40, got {result}"
        print("\nSUCCESS: Test passed! The answer is 40.")
    finally:
        if os.path.exists(filename):
            os.remove(filename)
    return
            
def solve_playground_part2(filename, verbose=False):
    boxes = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                x, y, z = map(int, line.strip().split(','))
                boxes.append((x, y, z))
    
    n = len(boxes)
    
    edges = []
    for i in range(n):
        xi, yi, zi = boxes[i]
        for j in range(i + 1, n):
            xj, yj, zj = boxes[j]
            dist = (xi - xj)**2 + (yi - yj)**2 + (zi - zj)**2
            edges.append((dist, i, j))
            
    edges.sort()
    
    if verbose:
        print(f"[INFO] Loaded {n} boxes, generated {len(edges)} edges.")


    parent = list(range(n))
    size = [1] * n 
    
    num_components = n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False 

        # Merge logic
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True


    for dist, u, v in edges:
        if union(u, v):
            num_components -= 1
            
            if verbose and num_components % 50 == 0:
                 print(f"[PROGRESS] Components remaining: {num_components}")


            if num_components == 1:
                if verbose:
                    print(f"[DONE] Final Connection between {u} and {v}")
                    print(f"       Box {u}: {boxes[u]}")
                    print(f"       Box {v}: {boxes[v]}")
                
                return boxes[u][0] * boxes[v][0]

    return -1 

def test_part2():
    import os
    t = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    
    import os
    filename = 'test_part2.txt'
    with open(filename, 'w') as f:
        f.write(t)

    try:
        result = solve_playground_part2(filename, verbose=True)
        print(f"\nCalculated Result: {result}")
        assert result == 25272, f"Expected 25272, got {result}"
        print("SUCCESS: Part 2 Test passed!")
    finally:
        if os.path.exists(filename):
            os.remove(filename)
    return

if __name__ == "__main__":
    # test_solve_playground()
    # print(solve_playground('Day 8/input.txt'))
    
    # test_part2()
    print(solve_playground_part2('Day 8/input.txt'))