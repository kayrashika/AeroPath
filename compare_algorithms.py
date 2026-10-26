import time

from bfs import bfs_find_path
from pathfinding import find_path

ROWS = 15
COLS = 20

start = (1, 1)
goal = (13, 18)

obstacles = {
    (3, 4), (3, 5), (3, 6),
    (4, 6), (5, 6),
    (7, 10), (8, 10), (9, 10),
    (10, 10), (11, 10)
}

# Run BFS and measure execution time
bfs_start_time = time.perf_counter()

bfs_path, bfs_explored = bfs_find_path(
    start, goal, obstacles, ROWS, COLS
)

bfs_time = (time.perf_counter() - bfs_start_time) * 1000

# Run A* and measure execution time
astar_start_time = time.perf_counter()

astar_path, astar_explored = find_path(
    start, goal, obstacles, ROWS, COLS
)

astar_time = (time.perf_counter() - astar_start_time) * 1000

# Display comparison
print("\n===== BFS vs A* Comparison =====")

print("\nBFS:")
print("Path length:", len(bfs_path) - 1 if bfs_path else "No path")
print("Explored cells:", len(bfs_explored))
print(f"Execution time: {bfs_time:.4f} ms")

print("\nA*:")
print("Path length:", len(astar_path) - 1 if astar_path else "No path")
print("Explored cells:", len(astar_explored))
print(f"Execution time: {astar_time:.4f} ms")

print("\n===== Result =====")

if bfs_path and astar_path:
    if len(bfs_path) == len(astar_path):
        print("Both algorithms found paths of equal length.")
    else:
        print("The algorithms found paths of different lengths.")

    if len(astar_explored) < len(bfs_explored):
        print("A* explored fewer cells in this test.")
    elif len(astar_explored) > len(bfs_explored):
        print("BFS explored fewer cells in this test.")
    else:
        print("Both explored the same number of cells.")
