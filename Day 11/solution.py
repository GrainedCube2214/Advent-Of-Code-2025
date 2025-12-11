"""
Advent of Code 2025 - Day 11: Reactor
Complete Solution for Part 1 and Part 2
"""
import sys
from functools import lru_cache

# Increase recursion depth just in case the graph is extremely deep
sys.setrecursionlimit(100000)

class ReactorSolver:
    def __init__(self, filename):
        self.graph = self._parse_graph(filename)

    def _parse_graph(self, filename):
        """Reads the input file into a dictionary: graph[node] = [neighbors]"""
        graph = {}
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    # Parse line "node: out1 out2 out3"
                    parts = line.strip().split(":")
                    node = parts[0].strip()
                    
                    # Handle nodes with outputs vs dead ends
                    if len(parts) > 1 and parts[1].strip():
                        outputs = parts[1].strip().split(" ")
                        graph[node] = outputs
                    else:
                        graph[node] = []
            return graph
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)

    @lru_cache(maxsize=None)
    def count_paths(self, start_node, end_node):
        """
        Efficiently counts paths from start_node to end_node using Memoization.
        Time Complexity: O(Nodes + Edges)
        """
        # Base Case: We reached the target
        if start_node == end_node:
            return 1
        
        # Base Case: Dead end or node not in graph
        if start_node not in self.graph:
            return 0
        
        # Recursive Step: Sum paths from all neighbors
        total_paths = 0
        for neighbor in self.graph[start_node]:
            total_paths += self.count_paths(neighbor, end_node)
        
        return total_paths
    
    def test_part1(self):
        t = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        with open("test_input.txt", "w") as f:
            f.write(t)
        self.graph = self._parse_graph("test_input.txt")
        assert self.count_paths("you", "out") == 5, f"Expected 5, got {self.count_paths('you', 'out')}"
        print("Part 1 test passed, got 5 paths as expected.")
        import os
        os.remove("test_input.txt")
        return
    
    def solve_part1(self):
        """Part 1: Count paths from 'you' to 'out'"""
        # Note: Depending on your specific input, the start node might be different.
        # The prompt examples used 'you', but sometimes AoC inputs vary.
        start = "you"
        end = "out"
        
        if start not in self.graph:
            print(f"Warning: Start node '{start}' not found in graph. Skipping Part 1.")
            return 0
            
        return self.count_paths(start, end)
    
    def test_part2(self):
        t = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
        with open("test_input2.txt", "w") as f:
            f.write(t)
        
        start = "svr"
        end = "out"
        mid1 = "dac"
        mid2 = "fft"
        
        self.graph = self._parse_graph("test_input2.txt")
        self.count_paths.cache_clear()
        valid_paths = (
            self.count_paths(start, mid1) * self.count_paths(mid1, mid2) * self.count_paths(mid2, end)
        ) + (
            self.count_paths(start, mid2) * self.count_paths(mid2, mid1) * self.count_paths(mid1, end)
        )
        
        assert valid_paths == 2, f"Expected 2, got {valid_paths}"
        print("Part 2 test passed, got 2 paths as expected.")
        import os
        os.remove("test_input2.txt")
        return

    def solve_part2(self):
        """
        Part 2: Count paths from 'svr' to 'out' that visit BOTH 'dac' and 'fft'.
        
        Since it's a Directed Acyclic Graph (DAG), data can't flow backwards.
        Therefore, the path must be either:
        1. svr -> ... -> dac -> ... -> fft -> ... -> out
        OR
        2. svr -> ... -> fft -> ... -> dac -> ... -> out
        """
        start = "svr"
        end = "out"
        mid1 = "dac"
        mid2 = "fft"

        if start not in self.graph:
            print(f"Warning: Start node '{start}' not found in graph. Skipping Part 2.")
            return 0

        # Clear cache to ensure clean state (though not strictly necessary for same graph)
        self.count_paths.cache_clear()

        # Calculate Scenario A: svr -> dac -> fft -> out
        # Paths = (svr->dac) * (dac->fft) * (fft->out)
        paths_via_dac_then_fft = (
            self.count_paths(start, mid1) * self.count_paths(mid1, mid2) * self.count_paths(mid2, end)
        )

        # Calculate Scenario B: svr -> fft -> dac -> out
        # Paths = (svr->fft) * (fft->dac) * (dac->out)
        paths_via_fft_then_dac = (
            self.count_paths(start, mid2) * self.count_paths(mid2, mid1) * self.count_paths(mid1, end)
        )

        total_constrained_paths = paths_via_dac_then_fft + paths_via_fft_then_dac
        return total_constrained_paths

if __name__ == "__main__":
    # Specify your input file here
    input_file = "Day 11/input.txt"
    
    print(f"--- Processing {input_file} ---")
    solver = ReactorSolver(input_file)
    
    # --- Part 1 ---
    # Calculates total paths from 'you' to 'out'
    # solver.test_part1()
    p1_ans = solver.solve_part1()
    print(f"Part 1 Solution: {p1_ans}")

    # --- Part 2 ---
    # Calculates paths from 'svr' to 'out' passing through 'dac' and 'fft'
    # solver.test_part2()
    p2_ans = solver.solve_part2()
    print(f"Part 2 Solution: {p2_ans}")
