
import heapq


def heuristic(cell, goal):
    row, col = cell
    goal_row, goal_col = goal

    return abs(row - goal_row) + abs(col - goal_col)


def find_path(start, goal, obstacles, rows, cols):
    open_list = []
    heapq.heappush(
        open_list,
        (heuristic(start, goal), start)
    )

    came_from = {}
    cost_so_far = {start: 0}
    explored = set()

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in explored:
            continue

        explored.add(current)

        if current == goal:
            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()

            return path, explored

        row, col = current

        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        for neighbor in neighbors:
            r, c = neighbor

            if not (0 <= r < rows and 0 <= c < cols):
                continue

            if neighbor in obstacles or neighbor in explored:
                continue

            new_cost = cost_so_far[current] + 1

            if (
                neighbor not in cost_so_far
                or new_cost < cost_so_far[neighbor]
            ):
                cost_so_far[neighbor] = new_cost

                priority = new_cost + heuristic(neighbor, goal)

                heapq.heappush(
                    open_list,
                    (priority, neighbor)
                )

                came_from[neighbor] = current

    return None, explored
