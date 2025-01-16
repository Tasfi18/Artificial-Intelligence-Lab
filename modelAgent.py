import random
import time
import tkinter as tk

def create_room():
    room = []
    for _ in range(8):
        row = []
        for _ in range(8):
            value = random.choice([0, 0, 'H', '#', '#']) 
            row.append(value)
        room.append(row)
    return room

def start():
    x = random.randint(1, 6)
    y = random.randint(1, 6)
    return x, y

def print_room(room, x, y, path):
    for i, row in enumerate(room):
        for j, cell in enumerate(row):
            if i == x and j == y:
                print("R", end=" ")
            elif (i, j) in path:
                print(".", end=" ") 
            else:
                print(cell, end=" ")
        print()
    print("\n")

def update_gui(room, x, y, path, gui_labels):
    for i, row in enumerate(room):
        for j, cell in enumerate(row):
            if i == x and j == y:
                gui_labels[i][j].config(text="R", bg="yellow") 
            elif (i, j) in path:
                gui_labels[i][j].config(text=".", bg="lightgreen") 
            else:
                gui_labels[i][j].config(text=cell, bg="white" if cell == 0 else "lightgrey")
    root.update()


def check_object(room, x, y):
    return room[x][y] == "#"


def perceive_boundaries(x, y, room):
    return x == 0 or y == 0 or x == (len(room) - 1) or y == (len(room[0]) - 1)


def move_up(x, y):
    return x - 1, y

def move_down(x, y):
    return x + 1, y

def move_left(x, y):
    return x, y - 1

def move_right(x, y):
    return x, y + 1

def move_robot(room, x, y, prev_direction):
    directions = ['up', 'down', 'left', 'right']

    if prev_direction == 'up':
        directions.remove('down')
    elif prev_direction == 'down':
        directions.remove('up')
    elif prev_direction == 'left':
        directions.remove('right')
    elif prev_direction == 'right':
        directions.remove('left')


    if room[x - 1][y] == "H" and 'up' in directions:
        directions.remove('up')
    if room[x + 1][y] == "H" and 'down' in directions:
        directions.remove('down')
    if room[x][y - 1] == "H" and 'left' in directions:
        directions.remove('left')
    if room[x][y + 1] == "H" and 'right' in directions:
        directions.remove('right')

    if len(directions) == 0:
        return x, y, prev_direction, False

    direction = random.choice(directions)

    if direction == 'up':
        new_x, new_y = move_up(x, y)
    elif direction == 'down':
        new_x, new_y = move_down(x, y)
    elif direction == 'left':
        new_x, new_y = move_left(x, y)
    elif direction == 'right':
        new_x, new_y = move_right(x, y)
    else:
        return x, y, prev_direction, False

    return new_x, new_y, direction, True

def collect_object(room, x, y):
    room[x][y] = 0

root = tk.Tk()
root.title("Robot Room Simulation")

room_size = 8
gui_labels = [[tk.Label(root, text=" ", width=3, height=2, relief="solid") for _ in range(room_size)] for _ in range(room_size)]

for i in range(room_size):
    for j in range(room_size):
        gui_labels[i][j].grid(row=i, column=j)

total_move = 0
total_object_collected = 0
total_action = 0
prev_direction = None

for i in range(3):
    x, y = start()
    print("Step:", i)
    move = 0
    objects_collected = 0
    room = create_room()
    path = [] 

    while True:
        time.sleep(1)
        if check_object(room, x, y):
            collect_object(room, x, y)
            objects_collected += 1
            total_object_collected += 1
            total_action += 1

        path.append((x, y))  
        update_gui(room, x, y, path, gui_labels)
        print_room(room, x, y, path)

        if perceive_boundaries(x, y, room):
            print(f"Objects collected in step {i} is: {objects_collected}")
            print(f"Robot moves in step {i} is: {move} times")
            break

        new_x, new_y, prev_direction, moved = move_robot(room, x, y, prev_direction)

        if not moved:
            print(f"Objects collected in step {i} is: {objects_collected}")
            print(f"Robot moves in step {i} is: {move} times")
            print("Robot is blocked by hurdles")
            break

        move += 1
        total_move += 1
        total_action += 1
        x, y = new_x, new_y

performance = total_action / total_object_collected if total_object_collected > 0 else 0
print("Total objects collected:", total_object_collected)
print("Total moves:", total_move)
print("Total Action:", total_action)
print("Final Performance:", performance)

root.mainloop()
