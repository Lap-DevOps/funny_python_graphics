from random import choice
import pygame

# set the size of the screen and the size of each cell
RES = WIDTH, HEIGHT = 1202, 702
TILE = 50

# calculate the number of rows and columns
cols, rows = WIDTH // TILE, HEIGHT // TILE

# create empty lists for colors and stack
colors, color = [], 40
stack = []

# initialize pygame
pygame.init()

# create the screen and clock objects
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

# create a Cell class to represent each cell in the grid
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    # draw the cell with a brown color
    def draw_cuttenr_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(screen, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    # draw the walls of the cell with an orange color if they exist
    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)

    # check if the cell at the given position is valid and return it
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    # check the neighbors of the current cell and return a random unvisited neighbor
    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

def remove_walls(current, next):
    # Determine the direction of the movement by checking the difference in x and y coordinates
    dx = current.x - next.x
    if dx == 1:
        # If the current cell is to the right of the next cell, remove the left wall of the current cell and the right wall of the next cell
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        # If the current cell is to the left of the next cell, remove the right wall of the current cell and the left wall of the next cell
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        # If the current cell is below the next cell, remove the top wall of the current cell and the bottom wall of the next cell
        current.walls['top'] = False
        next.walls['bottom'] = False
    if dy == -1:
        # If the current cell is above the next cell, remove the bottom wall of the current cell and the top wall of the next cell
        current.walls['bottom'] = False
        next.walls['top'] = False

# Create a list of all the cells in the grid
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

# Set the current cell to the first cell in the list
current_cell = grid_cells[0]

# Create an empty stack to keep track of visited cells
stack = []

# Main game loop
while True:
    # Clear the screen with a darkslategrey color
    screen.fill(pygame.Color('darkslategrey'))

    # Check for events (e.g. QUIT event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Draw all the cells in the grid
    [cell.draw() for cell in grid_cells]

    # Mark the current cell as visited and draw it with a different color
    current_cell.visited = True
    current_cell.draw_cuttenr_cell()

    # Draw a colored circle around each cell in the stack (i.e. the path taken so far)
    [pygame.draw.rect(screen, colors[i], (cell.x*TILE+5, cell.y*TILE+5, TILE-10, TILE-10), border_radius=12) for i, cell in enumerate(stack)]

    # Check for unvisited neighbors of the current cell
    next_cell = current_cell.check_neighbors()
    if next_cell:
        # If there are unvisited neighbors, mark the current cell as visited, add it to the stack, remove the wall between the current and next cell, and set the next cell as the current cell
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 10, 100)) # Add a new color to the colors list
        color += 1 # Increment the color counter
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        # If there are no unvisited neighbors, pop the top cell from the stack and set it as the current cell
        current_cell = stack.pop()

    # Update the display and limit the frame rate to 30 FPS
    pygame.display.flip()
    clock.tick(10)
    pygame.display.set_caption(f'FPS: {clock.get_fps():.2f}')

