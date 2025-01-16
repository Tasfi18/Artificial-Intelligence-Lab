import random
import math
from collections import deque
import matplotlib.pyplot as plt
import numpy as np


def environmenCreate(world: list) -> None:
    """Creates the world with black space, objects, and hurdles"""
    for i in range(5):
        for j in range(7):
            world[i][j] = random.choice([0, 0, 1, 9, 0, 1])
    return world


def detectingObjPos(world: list) -> list:
    """Returns the list of all the objects' rows and columns"""
    objPosRow, objPosCol = [], []
    for i in range(5):
        for j in range(7):
            if world[i][j] == 1:
                objPosRow.append(i)
                objPosCol.append(j)
    return objPosRow, objPosCol


def randomInitPosition(world: list) -> list:
    """Returns a random initial position row and column"""
    a, b = random.randint(1, 3), random.randint(1, 5)  # row, column
    while world[a][b] == 9 or world[a][b] == 1:
        a, b = random.randint(1, 3), random.randint(1, 5)
    return a, b


def closestObjPos(objPosRow: list, objPosCol: list, row: int, column: int) -> int:
    """Returns the closest object's row and column"""
    minDist, closestObjRow, closestObjCol = float('inf'), -1, -1
    for i in range(len(objPosRow)):
        dist = abs(row - objPosRow[i]) + abs(column - objPosCol[i])
        if minDist > dist:
            minDist, closestObjRow, closestObjCol = dist, objPosRow[i], objPosCol[i]
    return closestObjRow, closestObjCol


def pathSelection(world: list, column: int, row: int, closestObjRow: int, closestObjCol: int) -> list:
    """Returns the shortest path if exists"""
    start = (row, column)
    queue = deque([(start, [])])
    visited = set([start])
    hurdleAvoided = 0
    
    while queue:
        (x, y), path = queue.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 5 and 0 <= ny < 7:
                if world[nx][ny] == 9:
                    hurdleAvoided += 1
                if world[nx][ny] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(x, y)]))
                    visited.add((nx, ny))
                if nx == closestObjRow and ny == closestObjCol:
                    return path + [(x, y), (nx, ny)], hurdleAvoided       
    return [], hurdleAvoided


def plot_test_instance(ax, world, path, row, column, closestObjRow, closestObjCol):
    """Plot each test case on a separate subplot"""
    ax.imshow(world, cmap='gray_r', interpolation='none')
    for r in range(len(world)):
        for c in range(len(world[0])):
            if world[r][c] == 1:
                ax.scatter(c, r, color='blue', s=100)  # Object
            elif world[r][c] == 9:
                ax.scatter(c, r, color='black', s=100)  # Hurdle
                
    ax.scatter(column, row, color='red', s=200)  # Robot
    for step in path:
        ax.scatter(step[1], step[0], color='orange', s=50, alpha=0.6)  # Path steps
    ax.scatter(closestObjCol, closestObjRow, color='green', s=200, edgecolor='yellow')  # Closest object


def main():
    world = [[0 for _ in range(7)] for _ in range(5)]
    testTime = int(input("Enter the testing time: "))
    
    # Create subplots for each test instance
    fig, axes = plt.subplots(1, testTime, figsize=(5 * testTime, 5))
    axes = np.array(axes).reshape(-1)
    
    for test in range(testTime):
        world = environmenCreate(world)
        row, column = randomInitPosition(world)
        objPosRow, objPosCol = detectingObjPos(world)
        
        if not objPosRow:
            print("No objects to collect.")
            continue
        
        closestObjRow, closestObjCol = closestObjPos(objPosRow, objPosCol, row, column)
        path, hurdleAvoided = pathSelection(world, column, row, closestObjRow, closestObjCol)
        
        print(f"Test {test + 1}: Closest Obj Position: ({closestObjRow},{closestObjCol}), Hurdles avoided: {hurdleAvoided}")
        for step in path:
            print(f"{step}", end=" -> ")
        
        # Plot each test case's movement on its dedicated subplot
        plot_test_instance(axes[test], world, path, row, column, closestObjRow, closestObjCol)
        axes[test].set_title(f"Test {test + 1}")
        axes[test].grid(True)

    plt.show()


if __name__ == "__main__":
    main()
