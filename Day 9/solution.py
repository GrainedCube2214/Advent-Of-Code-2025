from itertools import combinations
from pathlib import Path
import os


Point = tuple[int, int]
Segment = tuple[int, int, int]


def solve_unconstrained_max_area(raw_points: list[Point]) -> int:
    best_area = 0
    
    for p1, p2 in combinations(raw_points, 2):
        delta_x = abs(p1[0] - p2[0]) + 1
        delta_y = abs(p1[1] - p2[1]) + 1
        current_area = delta_x * delta_y
        
        if current_area > best_area:
            best_area = current_area
            
    return best_area


def simplify_vertex_list(points: list[Point]) -> list[Point]:
    count = len(points)
    if count <= 2:
        return list(points)
    
    critical_vertices = []
    
    for idx in range(count):
        prev = points[(idx - 1 + count) % count]
        curr = points[idx]
        nxt = points[(idx + 1) % count]
        
        is_vertical_run = (prev[0] == curr[0] == nxt[0])
        is_horizontal_run = (prev[1] == curr[1] == nxt[1])
        
        if not (is_vertical_run or is_horizontal_run):
            critical_vertices.append(curr)
            
    return critical_vertices


def categorize_boundaries(perimeter: list[Point]) -> tuple[list[Segment], list[Segment]]:
    v_segs = []
    h_segs = []
    
    for k in range(len(perimeter) - 1):
        start_node = perimeter[k]
        end_node = perimeter[k + 1]
        
        if start_node[0] == end_node[0]:
            seg = (
                start_node[0], 
                min(start_node[1], end_node[1]), 
                max(start_node[1], end_node[1])
            )
            v_segs.append(seg)
        else:
            seg = (
                start_node[1], 
                min(start_node[0], end_node[0]), 
                max(start_node[0], end_node[0])
            )
            h_segs.append(seg)
            
    return v_segs, h_segs


def check_boundary_intrusion(
    x_start: int, x_end: int, 
    y_start: int, y_end: int, 
    v_segs: list[Segment], 
    h_segs: list[Segment]
) -> bool:
    for vx, vy_min, vy_max in v_segs:
        if x_start < vx < x_end:
            overlap_low = max(vy_min, y_start)
            overlap_high = min(vy_max, y_end)
            
            if overlap_low < overlap_high:
                return True
    
    for hy, hx_min, hx_max in h_segs:
        if y_start < hy < y_end:
            overlap_low = max(hx_min, x_start)
            overlap_high = min(hx_max, x_end)
            
            if overlap_low < overlap_high:
                return True
                
    return False


def is_point_enclosed(target_x: float, target_y: float, poly_path: list[Point]) -> bool:
    is_inside = False
    
    num_pts = len(poly_path)
    for i in range(num_pts - 1):
        p1 = poly_path[i]
        p2 = poly_path[i + 1]
        
        x1, y1 = float(p1[0]), float(p1[1])
        x2, y2 = float(p2[0]), float(p2[1])
        
        intersects_y = (y1 > target_y) != (y2 > target_y)
        
        if intersects_y:
            intersect_x = (x2 - x1) * (target_y - y1) / (y2 - y1) + x1
            
            if target_x < intersect_x:
                is_inside = not is_inside
                
    return is_inside


def solve_constrained_max_area(raw_points: list[Point]) -> int:
    vertices = simplify_vertex_list(raw_points)
    
    closed_loop = vertices + [vertices[0]]
    
    v_walls, h_walls = categorize_boundaries(closed_loop)
    
    max_found_area = 0
    
    for v1, v2 in combinations(vertices, 2):
        left, right = min(v1[0], v2[0]), max(v1[0], v2[0])
        bottom, top = min(v1[1], v2[1]), max(v1[1], v2[1])
        
        w = right - left + 1
        h = top - bottom + 1
        candidate_area = w * h
        
        if candidate_area <= max_found_area:
            continue
        
        if check_boundary_intrusion(left, right, bottom, top, v_walls, h_walls):
            continue
        
        mid_x = left + 0.5
        mid_y = bottom + 0.5
        if not is_point_enclosed(mid_x, mid_y, closed_loop):
            continue
        
        max_found_area = candidate_area
        
    return max_found_area


def parse_coordinates(filename) -> list[Point]:
    content = Path(filename).read_text(encoding="utf-8").strip()
    points = []
    for line in content.splitlines():
        if not line.strip(): continue
        parts = line.strip().split(',')
        points.append((int(parts[0]), int(parts[1])))
    return points


def run_tests():
    test_filename = "temp_test_input.txt"
    test_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    
    with open(test_filename, "w") as f:
        f.write(test_data)
        
    try:
        print("--- Running Tests ---")
        test_points = parse_coordinates(test_filename)
        
        p1_result = solve_unconstrained_max_area(test_points)
        expected_p1 = 50
        if p1_result == expected_p1:
            print(f"Part 1: PASS (Got {p1_result})")
        else:
            print(f"Part 1: FAIL (Expected {expected_p1}, Got {p1_result})")
            
        p2_result = solve_constrained_max_area(test_points)
        expected_p2 = 24
        if p2_result == expected_p2:
            print(f"Part 2: PASS (Got {p2_result})")
        else:
            print(f"Part 2: FAIL (Expected {expected_p2}, Got {p2_result})")
            
    finally:
        if os.path.exists(test_filename):
            os.remove(test_filename)
            print("--- Test File Deleted ---")


if __name__ == "__main__":
    run_tests()
    
    real_input = "Day 9/input.txt"
    if os.path.exists(real_input):
        print("\n--- Real Input ---")
        data = parse_coordinates(real_input)
        print("Part 1:", solve_unconstrained_max_area(data))
        print("Part 2:", solve_constrained_max_area(data))
    else:
        print(f"\nNo '{real_input}' found. Place your puzzle input in this file to run the full solution.")