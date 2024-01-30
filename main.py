import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Rectangle:
    def __init__(self, width, height, x=0, y=0, pos_x = 0):
        self.width = width
        self.height = height
        self.x = x  # X-coordinate of bottom-left corner
        self.y = y  # Y-coordinate of bottom-left corner
        self.pos_x = 0 # plotted y position

    def rotate(self):
        self.width, self.height = self.height, self.width

        
def place_rectangle(board, rectangle):
    for rotate in [False, True]:
        if rotate:
            rectangle.rotate()
        for x in range(len(board) - rectangle.width + 1):
            for y in range(len(board[0]) - rectangle.height + 1):
                if can_place(board, rectangle, x, y):
                    for i in range(rectangle.width):
                        for j in range(rectangle.height):
                            board[x + i][y + j] = 1
                    rectangle.x, rectangle.y = x, y  # Update position
                    return True
        if rotate:
            rectangle.rotate()  # Rotate back for next attempt
    return False

# Control if there is an empty space for rectangle
def can_place(board, rectangle, x, y):
    for i in range(rectangle.width):
        for j in range(rectangle.height):
            if board[x + i][y + j] != 0:
                return False
    return True

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        expected_num_rectangles = int(lines[0].strip())  # Number of rectangles from the first line
        area_size = tuple(map(int, lines[1].split()))
        rectangles = [Rectangle(*map(int, line.split())) for line in lines[2:2 + expected_num_rectangles]]
        return area_size, rectangles
    
# Replace this with the path to your file
filename = "./dataset/C2_3"

# Read data from file
area_size, rectangles = read_file(filename)

# Solve the problem for the given board size
board = [[0 for _ in range(area_size[1])] for _ in range(area_size[0])]
placed_rectangles = []
for rectangle in rectangles:
    if place_rectangle(board, rectangle):
        placed_rectangles.append(rectangle)
    else:
        print(f"Failed to place rectangle of size {rectangle.width}x{rectangle.height}")


def calculate_success_ratio(board, area_size):
    total_area = area_size[0] * area_size[1]
    used_area = sum(row.count(1) for row in board)
    success_ratio = (used_area / total_area) * 100
    empty_area = total_area - used_area
    return success_ratio, empty_area

success_ratio, empty_area = calculate_success_ratio(board, area_size)
print(f"Success Ratio: {success_ratio}%")
print(f"Leftover Empty Space: {empty_area} units")

def add_new_x_position(placed_rectangles):
    for rectangle in placed_rectangles:
        rectangle.pos_x = rectangle.x - rectangle.height
    
# add the new y positions
add_new_x_position(placed_rectangles)
#for i in placed_rectangles:
#   print(i.x, i.y, i.pos_x, i.height, i.width)

def convert_to_gcode(placed_rectangles):
    gcode = ""
    for rectangle in placed_rectangles:
        left_bot_y = rectangle.y
        left_bot_x = rectangle.x 
        height = rectangle.height
        width = rectangle.width

        gcode += f"M3\n"
        gcode+= f"G90\n"
        gcode+= f"G21\n"
        gcode += f"G1 F20\n"  # Drawing speed setting
        gcode += f"G1 X{left_bot_x } Y{left_bot_y}\n"  # Starting Point
        gcode += f"m3 s90\n"  # Acitvate pen
        gcode += f"G4 P0.20000000298023224\n"  # wait 
        gcode += f"G1 F20\n"  # Drawing speed setting
        gcode += f"G1 X{(left_bot_x + width)} Y{left_bot_y}\n"  
        gcode += f"G1 X{(left_bot_x + width)} Y{(left_bot_y + height)}\n"  
        gcode += f"G1 X{left_bot_x} Y{(left_bot_y + height)}\n"  
        gcode += f"G1 X{left_bot_x} Y{left_bot_y}\n" 
        gcode += f"m5\n"  # Close the pen

    gcode += f"G1 X{0} Y{0}\n"  #  Starting Point
    return gcode

# Visualization
fig, ax = plt.subplots()
for rectangle in placed_rectangles:
    ax.add_patch(patches.Rectangle(
        (rectangle.x, rectangle.y), rectangle.width, rectangle.height,
        edgecolor='black', facecolor=random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'cyan']),
        fill=True
    ))
ax.set_xlim(0, area_size[0])
ax.set_ylim(0, area_size[1])
ax.set_title("2D Cutting and Packing Problem Solution")
ax.set_xlabel("Width")
ax.set_ylabel("Height")
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

# Write gcode to a file
gcode_str = convert_to_gcode(placed_rectangles)
file = open('gcode. gcode', 'w+')
file.write(gcode_str)


