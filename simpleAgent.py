import random
import  time

# Environment
def create_room():
    room = []
    for _ in range(8):
        row = []
        for _ in range(8):
            value = random.choice([0, 0, '#'])
            row.append(value)
        room.append(row)
    return room

# Sensor
def check_object(room, x, y):
    # Sensor to detect if there's an object at the robot's current location
    return room[x][y] == "#"

# Percept
def perceive_boundaries(x, y, room):
    return x == 0 or y == 0 or x == (len(room) - 1) or y == (len(room[0]) - 1)

# Actuator
def move_up(x, y):
    return x - 1, y

def move_down(x, y):
    return x + 1, y

def move_left(x, y):
    return x, y - 1

def move_right(x, y):
    return x, y + 1

# Actuator to move robot in a valid direction based on previous movement
def move_robot(room, x, y, prev_direction):
    directions = ['up', 'down', 'left', 'right']

    # Avoid reverse moves
    if prev_direction == 'up':
        directions.remove('down')
    elif prev_direction == 'down':
        directions.remove('up')
    elif prev_direction == 'left':
        directions.remove('right')
    elif prev_direction == 'right':
        directions.remove('left')

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

# Actuator
def collect_object(room, x, y):
    room[x][y] = 0

# Percept: Starting position
def start():
    x = random.randint(1, 6)
    y = random.randint(1, 6)
    return x, y

# Visualization: Show the room and robot position
def print_room(room, x, y):
    for i, row in enumerate(room):
        for j, cell in enumerate(row):
            if i == x and j == y:
                print("R", end=" ")
            else:
                print(cell, end=" ")
        print()
    print("\n")


# Main process
total_move = 0
total_object_collected = 0
total_action = 0
prev_direction = None

for i in range(10):
    x, y = start()
    print("Step:", i)
    objects_collected = 0
    move = 0
    room = create_room()

    while True:
        time.sleep(2)
        # Sense if there's an object
        if check_object(room, x, y):
            # Actuator to collect the object if it's present
            collect_object(room, x, y)
            objects_collected += 1
            total_object_collected += 1
            total_action += 1

        # Visualize the environment
        print_room(room, x, y)

        # Sense if the robot is near the boundary
        if perceive_boundaries(x, y, room):
            print("Objects collected in step", i, "is", objects_collected)
            print("Robot moves in", i, "step is", move, "times")
            break

        # Actuator to move the robot
        new_x, new_y, prev_direction, moved = move_robot(room, x, y, prev_direction)

        if not moved:
            print("Objects collected in step", i, "is", objects_collected)
            print("Robot moves in", i, "step is", move, "times")
            print("Robot is blocked by boundaries, stopping this step.")
            break

        move += 1
        total_move += 1
        total_action += 1
        x, y = new_x, new_y

# Performance metrics
performance = total_action / total_object_collected
print("\nTotal objects collected:", total_object_collected)
print("Total moves:", total_move)
print("\n")
print("Total Action:", total_action)
print("Total Object Collected:", total_object_collected)
print("Total Performance:", performance)