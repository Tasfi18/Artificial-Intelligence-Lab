import pygame
import random
from collections import deque

ROWS = 9
COLS = 9
CELL_SIZE = 70
WIN_WIDTH = COLS * CELL_SIZE
WIN_HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AGENT_COLOR = (255, 0, 0)
HURDLE_COLOR = (0, 0, 255)                                  
OBJECT_COLOR = (0, 255, 0)
CROSS_COLOR = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 200, 0)

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.2:
                    self.grid[i][j] = 1 
                elif random.random() < 0.4:
                    self.grid[i][j] = 2  

    def draw(self, win, target):
        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(win, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                if self.grid[i][j] == 1:
                    points = [
                        (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + 5), 
                        (j * CELL_SIZE + 5, i * CELL_SIZE + CELL_SIZE - 5),  
                        (j * CELL_SIZE + CELL_SIZE - 5, i * CELL_SIZE + CELL_SIZE - 5) 
                    ]
                    pygame.draw.polygon(win, HURDLE_COLOR, points)
                elif self.grid[i][j] == 2:
                    pygame.draw.line(win, CROSS_COLOR, (j * CELL_SIZE + 5, i * CELL_SIZE + 5), 
                                     (j * CELL_SIZE + CELL_SIZE - 5, i * CELL_SIZE + CELL_SIZE - 5), 5)
                    pygame.draw.line(win, CROSS_COLOR, (j * CELL_SIZE + 5, i * CELL_SIZE + CELL_SIZE - 5), 
                                     (j * CELL_SIZE + CELL_SIZE - 5, i * CELL_SIZE + 5), 5)

        if target is not None:
            pygame.draw.circle(win, (255, 0, 0), (target[1] * CELL_SIZE + CELL_SIZE // 2, target[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

class Robot:
    def __init__(self, grid):
        self.grid = grid
        self.row = random.randint(1, grid.rows - 2)
        self.col = random.randint(1, grid.cols - 2)
        while self.grid.grid[self.row][self.col] == 1:
            self.row = random.randint(1, grid.rows - 2)
            self.col = random.randint(1, grid.cols - 2)
        self.path = [(self.row, self.col)]

    def move(self, direction):
        new_row = self.row + direction[0]
        new_col = self.col + direction[1]
        if 0 <= new_row < self.grid.rows and 0 <= new_col < self.grid.cols and self.grid.grid[new_row][new_col] != 1:
            self.row = new_row
            self.col = new_col
            self.path.append((self.row, self.col))

    def draw(self, win):
        pygame.draw.circle(win, AGENT_COLOR, (self.col * CELL_SIZE + CELL_SIZE // 2, self.row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        for i, j in self.path:
            pygame.draw.circle(win, YELLOW, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 8)

def find_nearest_object(grid, robot):
    min_distance = float('inf')
    nearest_object = None

    for i in range(grid.rows):
        for j in range(grid.cols):
            if grid.grid[i][j] == 2:
                distance = abs(i - robot.row) + abs(j - robot.col)

                clear_path = True

                if robot.row != i:
                    row_step = 1 if i > robot.row else -1
                    for r in range(robot.row, i, row_step):
                        if grid.grid[r][robot.col] == 1:
                            clear_path = False
                            break

                if clear_path and robot.col != j:
                    col_step = 1 if j > robot.col else -1
                    for c in range(robot.col, j, col_step):
                        if grid.grid[robot.row][c] == 1:
                            clear_path = False
                            break

                if clear_path and distance < min_distance:
                    min_distance = distance
                    nearest_object = (i, j)

    return nearest_object

def collect_object(grid, robot):
    if grid.grid[robot.row][robot.col] == 2:
        grid.grid[robot.row][robot.col] = 0
        return True
    return False

def has_valid_move(grid, robot):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        new_row = robot.row + direction[0]
        new_col = robot.col + direction[1]
        if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols and grid.grid[new_row][new_col] != 1:
            return True
    return False

def bfs_shortest_path(grid, start, target):
    rows, cols = grid.rows, grid.cols
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        current = queue.popleft()
        if current == target:
            break
        for direction in directions:
            new_row = current[0] + direction[0]
            new_col = current[1] + direction[1]
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                grid.grid[new_row][new_col] != 1 and 
                (new_row, new_col) not in visited):
                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
                parent[(new_row, new_col)] = current

    path = []
    while target in parent:
        path.append(target)
        target = parent[target]
        if target is None:
            break
    path.reverse()
    return path

def main():
    for _ in range(5):
        pygame.init()
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Robot Navigation")

        grid = Grid(ROWS, COLS)
        grid.randomize()
        robot = Robot(grid)

        target = (random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
        while grid.grid[target[0]][target[1]] == 1 or (target[0] == robot.row and target[1] == robot.col):
            target = (random.randint(1, ROWS - 2), random.randint(1, COLS - 2))

        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            path = bfs_shortest_path(grid, (robot.row, robot.col), target)

            if path:
                next_step = path[1] if len(path) > 1 else path[0]
                robot.move((next_step[0] - robot.row, next_step[1] - robot.col))

            win.fill(WHITE)
            grid.draw(win, target) 
            robot.draw(win)
            pygame.display.update()
            clock.tick(1)
            if (robot.row, robot.col) == target:
                print("Robot has reached the target!")
                running = False

        pygame.quit()


if __name__ == "__main__":
    main()
