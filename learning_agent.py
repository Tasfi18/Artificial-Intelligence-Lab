import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# Environment creation
def create_room(seed=None):
    if seed is not None:
        random.seed(seed)
    room = []
    for _ in range(8):
        row = []
        for _ in range(8):
            value = random.choice([0, 0, '#', 0, '#', 0])  # Free space (0) or object (#)
            row.append(value)
        room.append(row)
    return room


def start(room):
    while True:
        x = random.randint(0, 7)  # Adjusted to cover entire range
        y = random.randint(0, 7)
        if room[x][y] == 0:  # Ensure the starting position is not on an object
            return x, y


def plot_room(room, x, y, visited_path):
    grid = np.zeros((8, 8))

    for i in range(8):
        for j in range(8):
            if room[i][j] == '#':
                grid[i][j] = 1  # Object
            elif room[i][j] == "C":  # Collected object
                grid[i][j] = 2
            elif room[i][j] == "V":  # Visited but empty cell
                grid[i][j] = 3

    # Set the robot's position
    grid[x][y] = 4  # Robot's position

    # Custom color mapping
    cmap = ListedColormap(['white', 'blue', 'green', 'gray', 'red'])  # Use the correct colormap
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=4)

    # Adding probability text to the grid
    for i in range(8):
        for j in range(8):
            if learned_room[i][j] > 0:  # Only show text for cells that had been visited
                probability = learned_room[i][j] / 100  # Calculate probability (e.g., normalized to total attempts)
                plt.text(j, i, f"{probability:.2f}", ha='center', va='center', color='black')

    plt.colorbar(ticks=[0, 1, 2, 3, 4],
                 label='0: Free space, 1: Object (#), 2: Collected (C), 3: Visited empty (V), 4: Robot (R)')
    plt.xticks(range(8))
    plt.yticks(range(8))
    plt.gca().invert_yaxis()
    plt.title("Robot's Movement in the Room")
    plt.show(block=False)
    plt.pause(1.1)  # Brief pause to observe each movement
    plt.clf()  # Clear the figure for the next plot

def check_object(room, x, y):
    return room[x][y] == "#"  # Check for object

def collect_object(room, x, y):
    room[x][y] = "C"  # Mark as collected object

# Initialize learned_room based on frequency of objects in positions
learned_room = [[0 for _ in range(8)] for _ in range(8)]

def learning():
    for _ in range(100):  # Training iterations
        room = create_room()
        for i in range(8):
            for j in range(8):
                if room[i][j] == '#':  # Check if there's an object at this position
                    learned_room[i][j] += 1  # Increment the count in learned_room
    return learned_room

# Prioritize cells based on learned_room values
def get_prioritized_cells():
    cells = [(i, j) for i in range(8) for j in range(8)]
    return sorted(cells, key=lambda cell: learned_room[cell[0]][cell[1]], reverse=True)

# Main Execution
if __name__ == "__main__":
    learned_room = learning()
    print("Learned Room Object Counts:")
    for row in learned_room:
        print(row)

    total_move = 0
    total_object_collected = 0
    correct = 0
    error = 0

    for i in range(10):
        room = create_room()
        x, y = start(room)
        visited_path = []
        print(f"--- Iteration {i + 1} ---")
        print("Initial Room:")
        plot_room(room, x, y, visited_path)  # Plot the initial room

        prioritized_cells = get_prioritized_cells()

        for cell in prioritized_cells:
            target_x, target_y = cell
            x, y = target_x, target_y
            total_move += 1

            if check_object(room, x, y):
                collect_object(room, x, y)
                room[x][y] = "C"  # Mark as collected object
                total_object_collected += 1
                correct += 1
            else:
                error += 1
                room[x][y] = "V"  # Mark as visited but empty cell

            visited_path.append((x, y))
            plot_room(room, x, y, visited_path)  # Plot after each move

    # Final Summary
    print(f"\nTotal robot moves : {total_move}")
    print(f"Total objects collected : {total_object_collected}")
    print(f"Total success : {correct}")
    print(f"Total errors : {error}")
    print(f"Success Rate : {correct / total_move}")