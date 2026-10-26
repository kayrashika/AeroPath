
import time
import pygame

from bfs import bfs_find_path
from pathfinding import find_path

# Grid settings
ROWS = 15
COLS = 20
REPEATS = 30

# Original obstacles from the main simulation
standard_obstacles = {
    (3, 4), (3, 5), (3, 6),
    (4, 6), (5, 6),
    (7, 10), (8, 10), (9, 10),
    (10, 10), (11, 10)
}

# A denser obstacle layout, with gaps for navigation
dense_obstacles = standard_obstacles | {
    (2, c) for c in range(3, 17) if c != 10
} | {
    (5, c) for c in range(1, 18) if c != 7
} | {
    (8, c) for c in range(2, 19) if c != 15
} | {
    (11, c) for c in range(1, 17) if c != 5
}

# Three test scenarios
scenarios = [
    {
        "name": "Standard Grid",
        "start": (1, 1),
        "goal": (13, 18),
        "obstacles": standard_obstacles
    },
    {
        "name": "Dense Obstacles",
        "start": (1, 1),
        "goal": (13, 18),
        "obstacles": dense_obstacles
    },
    {
        "name": "Different Start & Goal",
        "start": (13, 1),
        "goal": (1, 18),
        "obstacles": standard_obstacles
    }
]


def run_comparison(scenario):
    """Run BFS and A* repeatedly and calculate average timings."""

    start = scenario["start"]
    goal = scenario["goal"]
    obstacles = scenario["obstacles"]

    # Warm up both algorithms before measuring.
    bfs_find_path(start, goal, obstacles, ROWS, COLS)
    find_path(start, goal, obstacles, ROWS, COLS)

    bfs_times = []
    astar_times = []

    bfs_path = None
    bfs_explored = set()
    astar_path = None
    astar_explored = set()

    # Repeat each algorithm to reduce timing noise.
    for _ in range(REPEATS):
        begin = time.perf_counter()
        current_path, current_explored = bfs_find_path(
            start, goal, obstacles, ROWS, COLS
        )
        bfs_times.append((time.perf_counter() - begin) * 1000)

        bfs_path = current_path
        bfs_explored = current_explored

        begin = time.perf_counter()
        current_path, current_explored = find_path(
            start, goal, obstacles, ROWS, COLS
        )
        astar_times.append((time.perf_counter() - begin) * 1000)

        astar_path = current_path
        astar_explored = current_explored

    bfs_average = sum(bfs_times) / REPEATS
    astar_average = sum(astar_times) / REPEATS

    bfs_length = len(bfs_path) - 1 if bfs_path else None
    astar_length = len(astar_path) - 1 if astar_path else None

    return {
        "bfs_path": bfs_path,
        "bfs_explored": bfs_explored,
        "bfs_length": bfs_length,
        "bfs_time": bfs_average,
        "astar_path": astar_path,
        "astar_explored": astar_explored,
        "astar_length": astar_length,
        "astar_time": astar_average
    }


# Pygame setup
pygame.init()

WIDTH = 760
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AeroPath AI - BFS vs A* Comparison")

title_font = pygame.font.SysFont("arial", 28, bold=True)
heading_font = pygame.font.SysFont("arial", 22, bold=True)
text_font = pygame.font.SysFont("arial", 18)
small_font = pygame.font.SysFont("arial", 15)

WHITE = (245, 245, 245)
CYAN = (70, 220, 235)
BLUE = (100, 165, 255)
GREEN = (100, 230, 150)
DARK_BG = (25, 32, 48)
PANEL_BG = (39, 49, 68)
GRAY = (190, 200, 215)
YELLOW = (255, 220, 100)

current_scenario = 0
results = run_comparison(scenarios[current_scenario])

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Select a scenario using keys 1, 2, or 3.
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                current_scenario = event.key - pygame.K_1
                results = run_comparison(
                    scenarios[current_scenario]
                )

    screen.fill(DARK_BG)

    scenario = scenarios[current_scenario]

    screen.blit(
        title_font.render("AeroPath AI", True, WHITE),
        (25, 15)
    )

    screen.blit(
        text_font.render(
            "BFS vs A* Pathfinding Comparison", True, CYAN
        ),
        (25, 53)
    )

    screen.blit(
        heading_font.render(
            f"Scenario {current_scenario + 1}: {scenario['name']}",
            True, YELLOW
        ),
        (25, 88)
    )

    screen.blit(
        small_font.render(
            f"Grid: {ROWS} x {COLS} | "
            f"Obstacles: {len(scenario['obstacles'])} | "
            f"Average of {REPEATS} runs per algorithm",
            True, GRAY
        ),
        (25, 122)
    )

    # BFS panel
    pygame.draw.rect(
        screen, PANEL_BG, (25, 160, 345, 205),
        border_radius=10
    )

    screen.blit(
        heading_font.render("BFS", True, BLUE),
        (45, 175)
    )

    screen.blit(
        text_font.render(
            f"Path length: {results['bfs_length'] if results['bfs_length'] is not None else 'No path'}",
            True, WHITE
        ),
        (45, 220)
    )

    screen.blit(
        text_font.render(
            f"Explored cells: {len(results['bfs_explored'])}",
            True, WHITE
        ),
        (45, 255)
    )

    screen.blit(
        text_font.render(
            f"Average time: {results['bfs_time']:.4f} ms",
            True, WHITE
        ),
        (45, 290)
    )

    # A* panel
    pygame.draw.rect(
        screen, PANEL_BG, (390, 160, 345, 205),
        border_radius=10
    )

    screen.blit(
        heading_font.render("A*", True, GREEN),
        (410, 175)
    )

    screen.blit(
        text_font.render(
            f"Path length: {results['astar_length'] if results['astar_length'] is not None else 'No path'}",
            True, WHITE
        ),
        (410, 220)
    )

    screen.blit(
        text_font.render(
            f"Explored cells: {len(results['astar_explored'])}",
            True, WHITE
        ),
        (410, 255)
    )

    screen.blit(
        text_font.render(
            f"Average time: {results['astar_time']:.4f} ms",
            True, WHITE
        ),
        (410, 290)
    )

    # Summary
    if results["bfs_path"] and results["astar_path"]:
        difference = (
            len(results["bfs_explored"])
            - len(results["astar_explored"])
        )

        if difference > 0:
            summary = f"A* explored {difference} fewer cells."
        elif difference < 0:
            summary = f"BFS explored {-difference} fewer cells."
        else:
            summary = "Both explored the same number of cells."

        if results["bfs_length"] == results["astar_length"]:
            path_summary = "Both found paths of equal length."
        else:
            path_summary = "Path lengths differ; inspect algorithm results."

        screen.blit(
            heading_font.render(summary, True, CYAN),
            (25, 385)
        )

        screen.blit(
            small_font.render(path_summary, True, WHITE),
            (25, 416)
        )

    else:
        screen.blit(
            heading_font.render(
                "At least one algorithm found no route.",
                True, WHITE
            ),
            (25, 385)
        )

        screen.blit(
            small_font.render(
                "Check whether the obstacle layout blocks the route.",
                True, GRAY
            ),
            (25, 416)
        )

    screen.blit(
        small_font.render(
            "Press 1: Standard | 2: Dense | "
            "3: New start/goal | ESC: Close",
            True, GRAY
        ),
        (25, 465)
    )

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
