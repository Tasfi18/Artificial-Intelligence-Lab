# Artificial Intelligence Lab

Intelligent agent exercises from the Artificial Intelligence lab course: vacuum cleaners, a simple reflex robot, a model-based robot, learning agents and a path-finding robot. Each agent moves around a grid world, senses objects and obstacles, and reports how well it did.

## The agents

| File | Agent | What it does |
| --- | --- | --- |
| `main.py` | Simple reflex vacuum | Two rooms, A and B. Cleans the current room if it's dirty, then moves to the other. Runs 1,000 trials and prints the performance. |
| `cleaner.py` | Vacuum on a row of tiles | Visits every tile once, sucking up dirt, and reports actions per dirty tile over 1,000 runs. |
| `simpleAgent.py` | Simple reflex robot | Wanders an 8×8 room, collects objects (`#`) it lands on and stops at the wall. Printed step by step in the terminal. |
| `modelAgent.py` | Model-based robot | Remembers where it has been and avoids holes (`H`). Shown in a Tkinter window. |
| `demo.py` | Goal-based robot | Finds the nearest object with breadth-first search, going around hurdles. Asks how many runs to make and plots each one. |
| `robot_navigation.py` | Path-finding robot | A 9×9 Pygame world: in five rounds, the robot follows the shortest path to a target cell around randomly placed hurdles. |
| `learning_agent.py` | Learning agent | Learns from earlier rooms where objects usually are and visits the likeliest cells first. Animated with Matplotlib. |
| `learning_agent1.py` | Learning agent (probability grid) | Builds a probability map from 50 sample grids, then searches a new grid in order of probability. Animated. |
| `reinforcement.py` | Learning from experience | Trains on random rooms, then collects objects and reports its success rate. |

The PDFs are the lab reports: `model_based_agent.pdf` and `learning_agent_report.pdf`.

## Run

Python 3.10 or later.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python demo.py                 # or any other file in the table
```

`modelAgent.py` and `learning_agent1.py` use Tkinter, which comes with Python on Windows and macOS (on Linux: `sudo apt install python3-tk`).

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

25 tests cover the vacuum cleaner, the breadth-first path finding in `demo.py`, the Pygame robot's grid, moves and shortest paths, and the learning agent's room generation, training and item collection. GitHub Actions runs them on every push.
