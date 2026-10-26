
import pygame
import sys
import subprocess
from pathfinding import find_path

pygame.init()

# Window settings
CELL_SIZE = 35
ROWS = 15
COLS = 20
PANEL_HEIGHT = 100

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + PANEL_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "AeroPath AI - E-commerce Parcel Delivery Navigation"
)

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20, bold=True)
small_font = pygame.font.SysFont("arial", 15)

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (210, 210, 210)
GREEN = (50, 200, 100)
RED = (230, 70, 70)
BLUE = (60, 130, 240)
YELLOW = (255, 220, 100)
DARK_BLUE = (25, 55, 110)
CYAN = (40, 210, 230)
DARK_BG = (25, 32, 48)

# Start and destination
start = (1, 1)
goal = (13, 18)

# Fixed obstacles
obstacles = {
    (3, 4), (3, 5), (3, 6),
    (4, 6), (5, 6),
    (7, 10), (8, 10), (9, 10),
    (10, 10), (11, 10)
}

# Dynamic obstacles added during the simulation
dynamic_obstacles = set()


# Draw the grid
def draw_grid(path, explored):
    for row in range(ROWS):
        for col in range(COLS):
            cell = (row, col)

            rect = pygame.Rect(
                col * CELL_SIZE,
                PANEL_HEIGHT + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = WHITE

            if cell in explored:
                color = YELLOW

            if cell in path:
                color = BLUE

            if cell in obstacles or cell in dynamic_obstacles:
                color = BLACK

            if cell == start:
                color = GREEN

            if cell == goal:
                color = RED

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)


# Draw the drone
def draw_drone(cell):
    row, col = cell

    x = col * CELL_SIZE + CELL_SIZE // 2
    y = PANEL_HEIGHT + row * CELL_SIZE + CELL_SIZE // 2

    rotors = [
        (x - 9, y - 9),
        (x + 9, y - 9),
        (x - 9, y + 9),
        (x + 9, y + 9)
    ]

    # Draw arms connecting the rotors
    for rotor_x, rotor_y in rotors:
        pygame.draw.line(
            screen, DARK_BLUE,
            (x, y), (rotor_x, rotor_y), 3
        )

    # Draw rotors
    for rotor_x, rotor_y in rotors:
        pygame.draw.circle(screen, WHITE, (rotor_x, rotor_y), 5)
        pygame.draw.circle(
            screen, DARK_BLUE, (rotor_x, rotor_y), 5, 2
        )

    # Draw the drone body
    pygame.draw.circle(screen, DARK_BLUE, (x, y), 6)
    pygame.draw.circle(screen, CYAN, (x, y), 3)


# Calculate route and reset the simulation
def reset_simulation():
    all_obstacles = obstacles | dynamic_obstacles

    new_path, new_explored = find_path(
        start, goal, all_obstacles, ROWS, COLS
    )

    return new_path, new_explored, 0, False, "Ready for delivery"


# Initial simulation state
path, explored, drone_index, running_drone, status = reset_simulation()

replanning_count = 0
move_delay = 200
last_move_time = pygame.time.get_ticks()

# Main loop
app_running = True

while app_running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            app_running = False

        if event.type == pygame.KEYDOWN:

            # Exit the application
            if event.key == pygame.K_ESCAPE:
                app_running = False

            # Start or pause the drone
            elif event.key == pygame.K_SPACE:
                if path and drone_index < len(path) - 1:
                    running_drone = not running_drone

                    if running_drone:
                        status = "Delivery in progress"
                    else:
                        status = "Delivery paused"

            # Reset the simulation
            elif event.key == pygame.K_r:
                dynamic_obstacles.clear()

                path, explored, drone_index, running_drone, status = (
                    reset_simulation()
                )

                replanning_count = 0
                last_move_time = pygame.time.get_ticks()

            # Add a dynamic obstacle and recalculate the route
            elif event.key == pygame.K_o:
                if path and drone_index < len(path) - 1:
                    next_cell = path[drone_index + 1]

                    if (
                        next_cell not in obstacles
                        and next_cell not in dynamic_obstacles
                    ):
                        dynamic_obstacles.add(next_cell)
                        replanning_count += 1

                        current_cell = path[drone_index]

                        path, explored = find_path(
                            current_cell,
                            goal,
                            obstacles | dynamic_obstacles,
                            ROWS,
                            COLS
                        )

                        # New path begins at the drone's current position
                        drone_index = 0

                        if path:
                            status = "Delivery route recalculated!"
                        else:
                            running_drone = False
                            status = "No safe route available"

            # Open the separate BFS vs A* comparison window
            elif event.key == pygame.K_c:
                try:
                    subprocess.Popen(
                        [sys.executable, "compare_window.py"]
                    )
                except OSError as error:
                    status = f"Could not open comparison: {error}"

    current_time = pygame.time.get_ticks()

    # Animate the drone only when started
    if (
        running_drone
        and path
        and drone_index < len(path) - 1
        and current_time - last_move_time >= move_delay
    ):
        drone_index += 1
        last_move_time = current_time

        if drone_index == len(path) - 1:
            running_drone = False
            status = "Delivery completed!"

    # Draw the information panel
    screen.fill(DARK_BG)

    title = font.render(
        "AeroPath AI | E-commerce Delivery", True, WHITE
    )
    screen.blit(title, (10, 8))

    path_length = len(path) - 1 if path else 0
    explored_count = len(explored)

    metrics = small_font.render(
        f"Path length: {path_length} steps   |   "
        f"Explored cells: {explored_count}   |   "
        f"Obstacles: {len(obstacles) + len(dynamic_obstacles)}   |   "
        f"Replans: {replanning_count}",
        True, WHITE
    )
    screen.blit(metrics, (10, 38))

    controls = small_font.render(
        "SPACE: Start/Pause  O: Add Obstacle  "
        "R: Reset  C: Compare  ESC: Exit",
        True, CYAN
    )
    screen.blit(controls, (10, 60))

    status_color = (
        GREEN if status == "Delivery completed!" else WHITE
    )

    status_text = small_font.render(
        "Status: " + status,
        True, status_color
    )
    screen.blit(status_text, (10, 80))

    # Draw grid and drone
    draw_grid(path or [], explored)

    # Show the drone at its current position
    if path:
        draw_drone(path[drone_index])
    else:
        # No route exists: keep the drone at its current/start position
        draw_drone(start)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
