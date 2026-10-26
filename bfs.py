
from collections import deque


def bfs_find_path(start, goal, obstacles, rows, cols):
    # Queue stores cells waiting to be explored
    queue = deque([start])

    # Remember which cell we came from
    parent = {start: None}

    # Track cells that have been explored
    explored = set()

    while queue:
        current = queue.popleft()
        explored.add(current)

        # If the destination is reached, rebuild the path
        if current == goal:
            path = []
            cell = goal

            while cell is not None:
                path.append(cell)
                cell = parent[cell]

            path.reverse()
            return path, explored

        row, col = current

        # Check the four neighboring cells
        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        for neighbor in neighbors:
            r, c = neighbor

            # Ignore cells outside the grid
            if not (0 <= r < rows and 0 <= c < cols):
                continue

            # Ignore obstacles and already discovered cells
            if neighbor in obstacles or neighbor in parent:
                continue

            # Record the parent and add the cell to the queue
            parent[neighbor] = current
            queue.append(neighbor)

    # No route exists
    return None, explored
