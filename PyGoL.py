#!/usr/bin/env python3

# File:    PyGoL.py
# Author:  Martin Ochs
# License: MIT
# Brief:   A very basic python implementation for Conway's "Game of Life"
#          using Tkinter for the GUI. The simulation can be controlled by
#          the speed slider and the buttons for different initial states.



import tkinter as tk
import random



# Define SW name and Version
SW_NAME = "PyGoL"
SW_VERS = "v0.5"

# Define the size of the grid
GRID_WIDTH    =  128
GRID_HEIGHT   =   64

# Define the size of the window
CELL_SIZE     = 10
CANVAS_WIDTH  = GRID_WIDTH  * CELL_SIZE
CANVAS_HEIGHT = GRID_HEIGHT * CELL_SIZE
CANVAS_OFFSET = 10  # GUI Pixel offset for Canvas to get some errormargin, since Linux and Mac handle window sizes differently and cells might geht cut off


# Create the grid to represent the cells
grid = [[0] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
cycle_counter = 0
cells_alive = 0
END_DET_CNT = 60
end_det = [0] * END_DET_CNT
end_det_pos = 0



# Function to initialize the grid
def init_grid(mode):
  global grid
  global cycle_counter
  cycle_counter = 0
  for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
      grid[x][y] = 0
  if  (mode == 1): # Random
    for x in range(GRID_WIDTH):
      for y in range(GRID_HEIGHT):
        grid[x][y] = random.choice([0, 1])
    for i in range(10):
      grid = update_grid() # Update several times to reduce huge grid changes after start
  elif(mode == 2): # Blinker
    grid[1][0] = 1
    grid[1][1] = 1
    grid[1][2] = 1
  elif(mode == 3): # Glider
    grid[0][2] = 1
    grid[1][0] = 1
    grid[1][2] = 1
    grid[2][1] = 1
    grid[2][2] = 1
  elif(mode == 4): # Glider gun
    grid[ 1][5] = 1; grid[ 1][6] = 1
    grid[ 2][5] = 1; grid[ 2][6] = 1
    grid[11][5] = 1; grid[11][6] = 1; grid[11][7] = 1
    grid[12][4] = 1; grid[12][8] = 1
    grid[13][3] = 1; grid[13][9] = 1
    grid[14][3] = 1; grid[14][9] = 1
    grid[15][6] = 1
    grid[16][4] = 1; grid[16][8] = 1
    grid[17][5] = 1; grid[17][6] = 1; grid[17][7] = 1
    grid[18][6] = 1
    grid[21][3] = 1; grid[21][4] = 1; grid[21][5] = 1
    grid[22][3] = 1; grid[22][4] = 1; grid[22][5] = 1
    grid[23][2] = 1; grid[23][6] = 1
    grid[25][1] = 1; grid[25][2] = 1; grid[25][6] = 1; grid[25][7] = 1
    grid[35][3] = 1; grid[35][4] = 1
    grid[36][3] = 1; grid[36][4] = 1
  elif(mode == 5): # Pentomino
    grid[0+int(GRID_WIDTH/2)][1+int(GRID_HEIGHT/2)] = 1
    grid[1+int(GRID_WIDTH/2)][0+int(GRID_HEIGHT/2)] = 1
    grid[1+int(GRID_WIDTH/2)][1+int(GRID_HEIGHT/2)] = 1
    grid[1+int(GRID_WIDTH/2)][2+int(GRID_HEIGHT/2)] = 1
    grid[2+int(GRID_WIDTH/2)][0+int(GRID_HEIGHT/2)] = 1
  elif(mode == 6): # Diehard
    grid[0+int(GRID_WIDTH/2)][4+int(GRID_HEIGHT/2)] = 1
    grid[1+int(GRID_WIDTH/2)][4+int(GRID_HEIGHT/2)] = 1
    grid[1+int(GRID_WIDTH/2)][5+int(GRID_HEIGHT/2)] = 1
    grid[5+int(GRID_WIDTH/2)][5+int(GRID_HEIGHT/2)] = 1
    grid[6+int(GRID_WIDTH/2)][3+int(GRID_HEIGHT/2)] = 1
    grid[6+int(GRID_WIDTH/2)][5+int(GRID_HEIGHT/2)] = 1
    grid[7+int(GRID_WIDTH/2)][5+int(GRID_HEIGHT/2)] = 1
  elif(mode == 7): # Acorn
    grid[0+int(GRID_WIDTH/2)][4+int(GRID_HEIGHT/2)] = 1
    grid[1+int(GRID_WIDTH/2)][2+int(GRID_HEIGHT/2)] = 1
    grid[1+int(GRID_WIDTH/2)][4+int(GRID_HEIGHT/2)] = 1
    grid[3+int(GRID_WIDTH/2)][3+int(GRID_HEIGHT/2)] = 1
    grid[4+int(GRID_WIDTH/2)][4+int(GRID_HEIGHT/2)] = 1
    grid[5+int(GRID_WIDTH/2)][4+int(GRID_HEIGHT/2)] = 1
    grid[6+int(GRID_WIDTH/2)][4+int(GRID_HEIGHT/2)] = 1
  draw_grid()



# Function to update the grid based on the game of life rules
def update_grid():
  new_grid = [[0] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
  for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
      neighbors = 0
      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          if dx == 0 and dy == 0:
            continue
          nx = (x + dx) % GRID_WIDTH
          ny = (y + dy) % GRID_HEIGHT
          neighbors += grid[nx][ny]
      if   grid[x][y] == 1 and neighbors  < 2: # Underpopulation
        new_grid[x][y] = 0
      elif grid[x][y] == 1 and neighbors  > 3: # Overpopulation
        new_grid[x][y] = 0
      elif grid[x][y] == 0 and neighbors == 3: # Reproduction
        new_grid[x][y] = 1
      else:                                    # Stasis
        new_grid[x][y] = grid[x][y]
  return new_grid



# Function to draw the grid on the canvas
def draw_grid():
  global cells_alive
  cells_alive = 0
  canvas.delete("all")
  for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
      x1 = x * CELL_SIZE + (CANVAS_OFFSET/2)
      y1 = y * CELL_SIZE + (CANVAS_OFFSET/2)
      x2 = x1 + CELL_SIZE
      y2 = y1 + CELL_SIZE
      if grid[x][y] == 1:
        #canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred")
        canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="darkred")
        cells_alive += 1
  label_cycle.config(text=f"Cycle: {cycle_counter}")
  label_cells.config(text=f"Cells: {cells_alive}")



# Function to detect the end of the simulation
def end_detection():
  global end_det
  global end_det_pos
  global cells_alive
  end_det_pos = (end_det_pos + 1) % END_DET_CNT
  end_det[end_det_pos] = cells_alive
  if cells_alive == 0:
    return True
  if cycle_counter > END_DET_CNT:                          # At least END_DET_CNT cycles needed for detection
    for pattern in range (1, int(END_DET_CNT/2)):          # Test pattern in the length of 1 to half of the buffer
      for testpos in range (pattern, END_DET_CNT):
        if end_det[testpos] != end_det[testpos % pattern]: # Pattern not found? -> End loop and test next pattern
          break
        if testpos == END_DET_CNT - 1:                     # End of loop reached? -> Pattern found!
          return True
  return False



# Function to handle one life cycle of the simulation
def life():
  global grid
  global cycle_counter

  if not end_detection():
    cycle_counter += 1

  grid = update_grid()
  draw_grid()
  window.update()

  if   speed_slider.get() == 5: # Set timeout depending on speed_slider value
    timeout = 0
  elif speed_slider.get() == 4:
    timeout = 1
  elif speed_slider.get() == 3:
    timeout = 10
  elif speed_slider.get() == 2:
    timeout = 100
  else:
    timeout = 1000
  window.after(timeout, life)



# Create a Tkinter window
window = tk.Tk()
window.title("Game of Life")
window.resizable(False, False)
window.geometry(f"{CANVAS_WIDTH+CANVAS_OFFSET+120}x{CANVAS_HEIGHT+CANVAS_OFFSET}")

# Create a canvas to draw the grid
canvas = tk.Canvas(window, width=CANVAS_WIDTH+CANVAS_OFFSET, height=CANVAS_HEIGHT+CANVAS_OFFSET) #, background="black")
canvas.pack()
canvas.place(x=0, y=0)

# Setup the slider for the speed of the simulation
speed_slider = tk.Scale(window, from_=1, to=5, orient="horizontal", label="Speed [1-5]", variable=tk.IntVar(value=5))
speed_slider.pack()
speed_slider.place(x=CANVAS_WIDTH+20, y=10, width=100)
window.bind("1", lambda e: speed_slider.set(1))
window.bind("2", lambda e: speed_slider.set(2))
window.bind("3", lambda e: speed_slider.set(3))
window.bind("4", lambda e: speed_slider.set(4))
window.bind("5", lambda e: speed_slider.set(5))

# Setup the random button which resets the grid
random_button = tk.Button(window, text="[R]andom", command=lambda: init_grid(1))
random_button.pack()
random_button.place(x=CANVAS_WIDTH+20, y=90, width=100)
window.bind("r", lambda e: init_grid(1))
window.bind("R", lambda e: init_grid(1))

# Setup the blinker button which resets the grid
blinker_button = tk.Button(window, text="[B]linker", command=lambda: init_grid(2))
blinker_button.pack()
blinker_button.place(x=CANVAS_WIDTH+20, y=120, width=100)
window.bind("b", lambda e: init_grid(2))
window.bind("B", lambda e: init_grid(2))

# Setup the glider button which resets the grid
glider_button = tk.Button(window, text="[G]lider", command=lambda: init_grid(3))
glider_button.pack()
glider_button.place(x=CANVAS_WIDTH+20, y=150, width=100)
window.bind("g", lambda e: init_grid(3))
window.bind("G", lambda e: init_grid(3))

# Setup the glider gun button which resets the grid
glider_gun_button = tk.Button(window, text="G[l]ider gun", command=lambda: init_grid(4))
glider_gun_button.pack()
glider_gun_button.place(x=CANVAS_WIDTH+20, y=180, width=100)
window.bind("l", lambda e: init_grid(4))
window.bind("L", lambda e: init_grid(4))

# Setup the pentomino button which resets the grid
pentomino_button = tk.Button(window, text="[P]entomino", command=lambda: init_grid(5))
pentomino_button.pack()
pentomino_button.place(x=CANVAS_WIDTH+20, y=210, width=100)
window.bind("p", lambda e: init_grid(5))
window.bind("P", lambda e: init_grid(5))

# Setup the diehard button which resets the grid
diehard_button = tk.Button(window, text="[D]iehard", command=lambda: init_grid(6))
diehard_button.pack()
diehard_button.place(x=CANVAS_WIDTH+20, y=240, width=100)
window.bind("d", lambda e: init_grid(6))
window.bind("D", lambda e: init_grid(6))

# Setup the acorn button which resets the grid
acorn_button = tk.Button(window, text="[A]corn", command=lambda: init_grid(7))
acorn_button.pack()
acorn_button.place(x=CANVAS_WIDTH+20, y=270, width=100)
window.bind("a", lambda e: init_grid(7))
window.bind("A", lambda e: init_grid(7))

# Setup the cycle counter label
label_cycle = tk.Label(window, text="Cycle:", anchor="w")
label_cycle.pack()
label_cycle.place(x=CANVAS_WIDTH+20, y=310, width=100)

# Setup the cells alive label
label_cells = tk.Label(window, text="Cells:", anchor="w")
label_cells.pack()
label_cells.place(x=CANVAS_WIDTH+20, y=330, width=100)

# Setup the quit button which ends the simulation
quit_button = tk.Button(window, text="[Q]uit", command=quit)
quit_button.pack()
quit_button.place(x=CANVAS_WIDTH+20, y=430, width=100)
window.bind("q", lambda e: quit())
window.bind("Q", lambda e: quit())
window.bind("<Escape>", lambda e: quit())
window.protocol("WM_DELETE_WINDOW", quit) # Clean quit on window close button

# Print SW name and version to window
label_sw = tk.Label(window, text=f"{SW_NAME} {SW_VERS}", anchor="e")
label_sw.pack()
label_sw.place(x=CANVAS_WIDTH+20, y=470, width=100, )

# Initialize the simulation
init_grid(1)
window.after(1, life)

# Run the Tkinter event loop
window.mainloop()

