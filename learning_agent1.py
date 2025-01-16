import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Tk
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
fig_width = screen_width / 120  
fig_height = screen_height / 120
num_grids = 50  
grid_size = 6  
grids = [np.random.choice([0, 1], size=(grid_size, grid_size), p=[0.7, 0.3]) for _ in range(num_grids)]
probability_grid = np.zeros((grid_size, grid_size))
for grid in grids:
    probability_grid += grid
probability_grid /= num_grids
test_grid = np.random.choice([0, 1], size=(grid_size, grid_size), p=[0.7, 0.3])
# Agent highest probability position
max_prob_position = np.unravel_index(np.argmax(probability_grid), probability_grid.shape)
agent_position = max_prob_position
visited = np.zeros((grid_size, grid_size), dtype=bool)
visited[agent_position] = True
# Success and error counters
success_count = 0
error_count = 0
path = [agent_position]
while len(path) < grid_size * grid_size:
    # Get unvisited positions
    unvisited_positions = [(i, j) for i in range(grid_size) for j in range(grid_size) if not visited[i, j]]
    unvisited_positions.sort(key=lambda pos: probability_grid[pos[0], pos[1]], reverse=True)
    # Move to the highest probability
    if unvisited_positions:
        agent_position = unvisited_positions[0]
        visited[agent_position] = True
        path.append(agent_position)
        # Count success or error
        if test_grid[agent_position] == 1:
            success_count += 1
        else:
            error_count += 1
            
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

#success and error percentages
total_cells = grid_size * grid_size
success_percentage = (success_count / total_cells) * 100
error_percentage = (error_count / total_cells) * 100
# Initialize plot function
def initialize():
    ax.clear()
    ax.imshow(probability_grid, cmap='plasma', interpolation='none', alpha=0.9)
    ax.set_xticks(np.arange(0, grid_size, 1))
    ax.set_yticks(np.arange(0, grid_size, 1))
    ax.set_xticklabels(np.arange(1, grid_size + 1))
    ax.set_yticklabels(np.arange(1, grid_size + 1))
    
    #probability value
    for (x, y), value in np.ndenumerate(probability_grid):
        ax.text(y, x - 0.2, f"{value:.2f}", ha='center', va='center', color='white')
        
    #initial success and error counts 
    ax.text(-2, grid_size - 1, f"Success Count: {success_count}", fontsize=10, ha='center', color='green')
    ax.text(-2, grid_size - 0.5, f"Error Count: {error_count}", fontsize=10, ha='center', color='red')
    start_x, start_y = max_prob_position
    ax.plot(start_y, start_x, 'bo', markersize=10, label='Starting Position')
    ax.legend()
    return ax

def animate(i):
    ax.clear()
    ax.imshow(probability_grid, cmap='plasma', interpolation='none', alpha=0.9)
    
    # Display object locations 
    for (x, y), value in np.ndenumerate(test_grid):
        if value == 1:
            ax.plot(y, x, marker='x', color='cyan', markersize=15, mew=2) 
    for (x, y), value in np.ndenumerate(probability_grid):
        ax.text(y, x - 0.2, f"{value:.2f}", ha='center', va='center', color='white')
        
    # Mark visited cells 
    for j, (x, y) in enumerate(path[:i + 1]):
        if test_grid[x, y] == 1:
            ax.plot(y, x, 'ks', markersize=12, fillstyle='none', markeredgewidth=2) 
            ax.add_patch(plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color='green', alpha=0.5))  
        else:
            ax.plot(y, x, 'mo', markersize=6) 
            
    # Agent's current position
    if i < len(path):
        x, y = path[i]
        ax.plot(y, x, 'co', markersize=10)
        
    #position current probability
    current_x, current_y = path[min(i, len(path) - 1)]
    current_probability = probability_grid[current_x, current_y]
    ax.text(grid_size + 1, grid_size // 2, f"Current Probability: {current_probability:.2f}", 
            fontsize=10, ha='left', color='orange')
    
    #success and error counts
    success_so_far = sum(1 for (x, y) in path[:i + 1] if test_grid[x, y] == 1)
    error_so_far = i + 1 - success_so_far
    ax.text(-2, grid_size - 1, f"Success Count: {success_so_far}", fontsize=10, ha='center', color='green')
    ax.text(-2, grid_size - 0.5, f"Error Count: {error_so_far}", fontsize=10, ha='center', color='red')
    
    if i == len(path) - 1:
        ax.text(grid_size / 2, -1, f"Performance: {success_percentage:.2f}%", fontsize=10, ha='center', color='green')
        
    # Grid 
    ax.set_xticks(np.arange(0, grid_size, 1))
    ax.set_yticks(np.arange(0, grid_size, 1))
    ax.set_xticklabels(np.arange(1, grid_size + 1))
    ax.set_yticklabels(np.arange(1, grid_size + 1))

    #borders
    for i in range(grid_size):
        for j in range(grid_size):
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, edgecolor='black', facecolor='none', lw=1)
            ax.add_patch(rect)
ani = animation.FuncAnimation(fig, animate, frames=len(path), init_func=initialize, repeat=False, interval=500)
plt.show()
