# AeroPath AI — Drone Navigation Simulation

## Project Overview

AeroPath AI is a Python-based drone navigation simulation designed to explore pathfinding in a grid environment. It demonstrates how a drone can navigate from a starting point to a destination while avoiding obstacles.

The project uses the A* pathfinding algorithm and compares its performance with Breadth-First Search (BFS). It also demonstrates dynamic obstacle handling, where a newly introduced obstacle triggers route recalculation.

## Features

- Visual grid-based drone navigation.
- A* pathfinding for route planning.
- BFS implementation for algorithm comparison.
- Dynamic obstacle placement and route recalculation.
- Three test scenarios for comparing pathfinding algorithms.
- Comparison of path length, explored cells, and execution time.
- Handling of situations where no valid route is available.

## Technologies Used

- Python 3
- Pygame
- A* pathfinding
- Breadth-First Search (BFS)

## Project Files

- `main.py` — Main simulation.
- `pathfinding.py` — A* pathfinding implementation.
- `bfs.py` — BFS implementation.
- `compare_window.py` — Visual algorithm comparison window.
- `compare_algorithms.py` — Algorithm comparison support.
- `test_bfs.py` — BFS testing.
- `main_backup.py` — Backup of the main simulation.

## Requirements

- Python 3 installed on your computer.
- Pygame installed.

Install Pygame using:

```bash
python -m pip install pygame
```

On Windows, if the `python` command does not work, try:

```bash
py -m pip install pygame
```

## How to Run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Install Pygame using the command above.
4. Start the main simulation:

```bash
python main.py
```

On Windows, you can also try:

```bash
py main.py
```

## Controls

- `SPACE` — Start or pause the simulation.
- `R` — Reset the simulation.
- `O` — Introduce a dynamic obstacle and trigger route recalculation.
- `C` — Open the BFS versus A* comparison window.
- `ESC` — Exit or close the relevant window.

## Limitations

This project is a grid-based simulation and does not control a physical drone. It does not currently use real-world GPS, cameras, sensors, flight physics, or battery measurements. Its results demonstrate algorithm behaviour in simulated scenarios and should not be interpreted as proof of real-world delivery performance.

## Future Scope

Possible improvements include larger grid environments, more complex obstacle patterns, additional performance experiments, and integration with real-world navigation data in a future version.