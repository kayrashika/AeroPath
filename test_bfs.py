
from bfs import bfs_find_path

# Grid dimensions
ROWS = 15
COLS = 20

# Starting point and destination
start = (1, 1)
goal = (13, 18)

# Same fixed obstacles used in AeroPath AI
obstacles = {
    (3, 4), (3, 5), (3, 6),
    (4, 6), (5, 6),
    (7, 10), (8, 10), (9, 10),
    (10, 10), (11, 10)
}

# Run BFS
path, explored = bfs_find_path(
    start, goal, obstacles, ROWS, COLS
)

# Display results
if path:
    print("BFS found a path!")
    print("Path length:", len(path) - 1, "steps")
    print("Explored cells:", len(explored))
    print("Starting cell:", path[0])
    print("Destination cell:", path[-1])
else:
    print("No safe route available.")
