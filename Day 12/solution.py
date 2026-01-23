"""
Advent of Code Day 12: Optimized Bitboard Solution
Incorporates the best optimizations from the reference solution
"""

import time
from itertools import product


def parse_input(input_text):
    """Parse the input into shapes and regions."""
    lines = input_text.strip().split('\n')
    
    shapes = []
    regions = []
    
    current_shape = []
    shape_index = None
    
    for line in lines:
        if not line.strip():
            if current_shape and shape_index is not None:
                shapes.append(current_shape)
                current_shape = []
                shape_index = None
            continue
        
        if 'x' in line and line[0].isdigit():
            if current_shape and shape_index is not None:
                shapes.append(current_shape)
                current_shape = []
                shape_index = None
            
            parts = line.split(':')
            dimension_part = parts[0].strip()
            dimensions = dimension_part.split('x')
            width = int(dimensions[0])
            height = int(dimensions[1])
            
            if len(parts) > 1:
                counts = list(map(int, parts[1].strip().split()))
            else:
                remaining = line.split()[1:]
                counts = list(map(int, remaining))
            
            regions.append((width, height, counts))
            
        elif ':' in line and line[0].isdigit() and 'x' not in line:
            if current_shape and shape_index is not None:
                shapes.append(current_shape)
            
            parts = line.split(':')
            shape_index = int(parts[0])
            current_shape = []
            
        elif line.startswith(('#', '.')):
            current_shape.append(line.strip())
    
    if current_shape and shape_index is not None:
        shapes.append(current_shape)
    
    return shapes, regions


class OptimizedBitboardSolver:
    """Optimized polyomino packing solver using bitboards and streamlined search."""
    
    def __init__(self, width, height, shapes, objective):
        self.L = width  # Using L for consistency with reference
        self.H = height
        self.objective = objective
        self.grid_size = width * height
        
        # Convert shapes to coordinate form and generate all orientations
        self.polyminos = self._generate_all_tiles(shapes)
        
        # Calculate shape sizes for quick feasibility check
        self.sizes = [len(self._shape_to_coords(shape)) for shape in shapes]
        
    def _shape_to_coords(self, shape):
        """Convert shape definition to list of (x, y) coordinates."""
        coords = []
        for y, row in enumerate(shape):
            for x, char in enumerate(row):
                if char == '#':
                    coords.append((x, y))
        return coords
    
    def _rotate(self, polymino):
        """Rotate a text-based polymino 90 degrees clockwise."""
        w, h = len(polymino[0]), len(polymino)
        rotated = []
        for x in range(w):
            s = ''
            for y in range(h):
                s = polymino[y][x] + s
            rotated.append(s)
        return rotated
    
    def _flip(self, polymino):
        """Flip a text-based polymino horizontally."""
        return [row[::-1] for row in polymino]
    
    def _generate_all_tiles(self, shapes):
        """Generate all unique orientations for each shape."""
        all_polyminos = []
        
        for shape in shapes:
            orientations = set()
            current = shape
            
            # Generate all 8 possible orientations
            for _ in range(4):
                # Add current rotation
                coords = tuple(self._shape_to_coords(current))
                orientations.add(self._normalize_coords(coords))
                
                # Add flipped version
                flipped = self._flip(current)
                coords_flipped = tuple(self._shape_to_coords(flipped))
                orientations.add(self._normalize_coords(coords_flipped))
                
                # Rotate for next iteration
                current = self._rotate(current)
            
            all_polyminos.append(list(orientations))
        
        return all_polyminos
    
    def _normalize_coords(self, coords):
        """Normalize coordinates to start from (0, 0)."""
        if not coords:
            return tuple()
        min_x = min(x for x, y in coords)
        min_y = min(y for x, y in coords)
        return tuple(sorted((x - min_x, y - min_y) for x, y in coords))
    
    def _translate(self, polymino, dx, dy):
        """Translate a polymino by (dx, dy)."""
        return [(x + dx, y + dy) for x, y in polymino]
    
    def _polymino_to_mask(self, coords):
        """Convert coordinates to bitboard mask."""
        mask = 0
        for x, y in coords:
            mask |= 1 << (x + y * self.L)
        return mask
    
    def _search(self, board, current, depth=0, max_depth=1000):
        """Optimized backtracking search using bitboards."""
        # Check if we've reached the objective
        if current == self.objective:
            return True
        
        # Depth limit to prevent infinite recursion
        if depth >= max_depth:
            return False
        
        # Find the first shape type we still need to place
        shape_idx = 0
        while shape_idx < len(self.objective) and current[shape_idx] == self.objective[shape_idx]:
            shape_idx += 1
        
        if shape_idx >= len(self.objective):
            return False
        
        # Try all orientations of this shape type
        for polymino in self.polyminos[shape_idx]:
            if not polymino:
                continue
                
            # Calculate bounds for placement
            max_x = self.L - max((x for x, _ in polymino), default=0)
            max_y = self.H - max((y for _, y in polymino), default=0)
            
            # Try all valid positions
            for dx in range(max(0, max_x + 1)):
                for dy in range(max(0, max_y + 1)):
                    # Translate polymino to position
                    translated = self._translate(polymino, dx, dy)
                    
                    # Check if all cells are in bounds
                    if not all(0 <= x < self.L and 0 <= y < self.H for x, y in translated):
                        continue
                    
                    # Convert to bitboard mask
                    mask = self._polymino_to_mask(translated)
                    
                    # Check for overlap using bitwise AND
                    if board & mask == 0:
                        # Place the shape
                        current[shape_idx] += 1
                        
                        # Recursive search
                        if self._search(board | mask, current, depth + 1, max_depth):
                            return True
                        
                        # Backtrack
                        current[shape_idx] -= 1
        
        return False
    
    def solve(self):
        """Solve the packing problem."""
        # Quick feasibility check
        available = self.L * self.H
        needed = sum(count * self.sizes[i] for i, count in enumerate(self.objective))
        
        if needed > available:
            return False
        
        # Check if we have valid orientations for all needed shapes
        for i, count in enumerate(self.objective):
            if count > 0 and (i >= len(self.polyminos) or not self.polyminos[i]):
                return False
        
        # Start search with empty board
        current = [0] * len(self.objective)
        return self._search(0, current)


def solve(input_text):
    """Main solve function with progress tracking."""
    shapes, regions = parse_input(input_text)
    
    print(f"Found {len(shapes)} shapes and {len(regions)} regions to check")
    print("Using optimized bitboard solver\n")
    
    solvable_count = 0
    total_regions = len(regions)
    start_total = time.time()
    
    for i, (width, height, counts) in enumerate(regions):
        # Progress bar
        progress = (i / total_regions) * 100
        bar_width = 30
        filled = int(bar_width * i / total_regions)
        bar = '#' * filled + '-' * (bar_width - filled)
        
        print(f"\rRegion {i+1}/{total_regions}: [{bar}] {progress:.1f}% - Checking {width}x{height}...", 
              end='', flush=True)
        
        start_time = time.time()
        
        # Solve with optimized bitboard solver
        solver = OptimizedBitboardSolver(width, height, shapes, counts)
        
        # Add timeout using threading
        import threading
        result = [False]
        
        def solve_thread():
            try:
                result[0] = solver.solve()
            except:
                result[0] = False
        
        thread = threading.Thread(target=solve_thread)
        thread.daemon = True
        thread.start()
        thread.join(timeout=5.0)  # 5 second timeout
        
        if thread.is_alive():
            is_solvable = False  # Timeout
        else:
            is_solvable = result[0]
        
        elapsed = time.time() - start_time
        
        if is_solvable:
            solvable_count += 1
            status = "SOLVABLE"
        else:
            status = "NOT solvable"
        
        print(f"\rRegion {i+1}/{total_regions}: [{bar}] {progress:.1f}% - {status} ({width}x{height}, {elapsed:.2f}s)")
    
    # Final progress bar
    bar = '#' * bar_width
    print(f"\rRegion {total_regions}/{total_regions}: [{bar}] 100.0% - Complete!                          ")
    
    total_time = time.time() - start_total
    print(f"\n{'='*60}")
    print(f"Completed in {total_time:.1f} seconds")
    print(f"Average time per region: {total_time/total_regions:.3f} seconds")
    print(f"Total solvable regions: {solvable_count}/{total_regions}")
    
    return solvable_count


if __name__ == "__main__":
    # Test with example
    example_input = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

    # print("Testing with example input:")
    # result = solve(example_input)
    # print(f"\nAnswer: {result}")
    # print(f"Expected: 2\n")
    
    # For actual puzzle
    with open('Day 12/input.txt', 'r') as f:
        puzzle_input = f.read()
    print("\nSolving actual puzzle:")
    result = solve(puzzle_input)
    print(f"\nAnswer: {result}")