import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def generate_room(seed=None):
    if seed is not None:
        random.seed(seed)
    room = []
    for _ in range(5):
        row = []
        for _ in range(5):
            value = random.choice([0, '#', 0, '#', 0])
            row.append(value)
        room.append(row)
    return room

def initialize_position(room):
    while True:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if room[x][y] == 0:
            return x, y

def visualize_room(room, x, y, visited_cells, learned_room):
    grid = np.zeros((5, 5))

    for i in range(5):
        for j in range(5):
            if room[i][j] == '#':
                grid[i][j] = 1 
            elif room[i][j] == "C":
                grid[i][j] = 2  
            elif room[i][j] == "V":
                grid[i][j] = 3  

    grid[x][y] = 5  


    cmap = ListedColormap(['#F0F8FF', '#00FF00', '#9370DB', '#0000FF', '#FF6347'])
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=4)

    for i in range(5):
        for j in range(5):
            if learned_room[i][j] > 0:
                probability = learned_room[i][j] / 100
                plt.text(j, i, f"{probability:.2f}", ha='center', va='center', color='black')

    plt.title("Robot's Movement in the Room", fontsize=14, color='#4B0082')

    for i in range(5):
        for j in range(5):
            if room[i][j] == "C": 
                circle = plt.Circle((j, i), 0.2, color='green', fill=True)
                plt.gca().add_artist(circle)
            elif room[i][j] == "V":  
                square = plt.Rectangle((j - 0.3, i - 0.3), 0.6, 0.6, color='blue', fill=True)
                plt.gca().add_artist(square)
                plt.plot([j - 0.2, j + 0.2], [i - 0.2, i + 0.2], color='black', lw=2)  
                plt.plot([j - 0.2, j + 0.2], [i + 0.2, i - 0.2], color='black', lw=2)  

    plt.show(block=False)
    plt.pause(0.25)
    plt.clf()

def initialize_learned_room():
    return [[0 for _ in range(5)] for _ in range(5)]

def train_learning_model():
    learned_room = initialize_learned_room()
    for _ in range(100):
        room = generate_room()
        for i in range(5):
            for j in range(5):
                if room[i][j] == '#':
                    learned_room[i][j] += 1
    return learned_room

def prioritize_cells(learned_room):
    cells = [(i, j) for i in range(5) for j in range(5)]
    return sorted(cells, key=lambda cell: learned_room[cell[0]][cell[1]], reverse=True)

def is_object_present(room, x, y):
    return room[x][y] in {"#", "C"}

def collect_item(room, x, y):
    room[x][y] = "C"

def update_learning_model(learned_room, room):
    for r in range(5):
        for c in range(5):
            prob = learned_room[r][c] / 100
            if prob >= 0.4:
                if is_object_present(room, r, c):
                    learned_room[r][c] += 5
                else:
                    learned_room[r][c] -= 5
def move_robot_to_cell(x, y, room, visited_cells, learned_room):
    visited_cells.add((x, y))
    probability = learned_room[x][y] / 100
    #print(f"Moving to: ({x}, {y}), Probability: {probability:f}")

    if probability >= 0.4:
        if is_object_present(room, x, y):
            collect_item(room, x, y)
            print(f"Object collected at: ({x}, {y})")
        else:
            room[x][y] = "V"
            print(f"Empty cell visited at: ({x}, {y})")
    else:
        update_learning_model(learned_room, room)
        #print(f"Low probability at: ({x}, {y}), updating learning model...")
        return False
    return True

def execute_movement_for_step(step, room, x, y, visited_cells, learned_room):
    print(f"--- Step {step + 1} ---")
    print("--------Room:----------")
    visualize_room(room, x, y, visited_cells, learned_room)

    prioritized_cells = prioritize_cells(learned_room)

    for cell in prioritized_cells:
        target_x, target_y = cell

        if (target_x, target_y) in visited_cells:
            continue

        x, y = target_x, target_y
        if not move_robot_to_cell(x, y, room, visited_cells, learned_room):
            break

        visualize_room(room, x, y, visited_cells, learned_room)

def track_progress(visited_cells, room):
    total_moves = len(visited_cells)
    total_collected = sum([1 for i in range(5) for j in range(5) if room[i][j] == "C"])
    successful = total_collected
    errors = sum([1 for i in range(5) for j in range(5) if room[i][j] == "V"])

    return total_moves, total_collected, successful, errors

def calculate_success_rate(total_moves, successful):
    return successful / total_moves if total_moves > 0 else 0

def display_summary(total_moves, total_collected, successful, errors, success_rate):
    print(f"\nTotal Moves: {total_moves}")
    print(f"Total Objects Collected: {total_collected}")
    print(f"Successful Attempts: {successful}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {success_rate:.2f}")

def execute_robot_movement():
    learned_room = train_learning_model()

    for step in range(5):
        room = generate_room()
        x, y = initialize_position(room)
        visited_cells = set()

        execute_movement_for_step(step, room, x, y, visited_cells, learned_room)

        total_moves, total_collected, successful, errors = track_progress(visited_cells, room)

        success_rate = calculate_success_rate(total_moves, successful)

        display_summary(total_moves, total_collected, successful, errors, success_rate)

if __name__ == "__main__":
    execute_robot_movement()
