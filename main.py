# the import for the graphical user interface
import tkinter
# use random import to place food in different locations
import random

# constants
ROWS = 25  # the width of the game-board
COLS = 25  # the length of the game-board
TILE_SIZE = 25  # each tile is 25 pixels
WINDOW_WIDTH = TILE_SIZE * COLS  # the total width of the game board is tile_size x cols
WINDOW_HEIGHT = TILE_SIZE * ROWS  # the total length of the game board is tile_size x rows


# create a class for the Tiles
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# game window
window = tkinter.Tk()  # this will open up a window
window.title("Snake")  # the title of the window will be snake
window.resizable(False, False)  # window will be 625x625 pixels and the user can't change the size by expanding window

# this creates the canvas (interface of the window)
canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
# format = (w) * (h) + (x) + (y)
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# initialize the game
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)  # single tile is snake's head
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)  # this is the food
snake_body = []  # multiple snake tiles
velocity_x = 0
velocity_y = 0
game_over = False
score = 0

# a function to change direction
def change_direction(e):  # e = event
    global velocity_x, velocity_y, game_over  # global lets you get variables from outside function
    if game_over:
        return

    if (e.keysym == "Up" and velocity_y != 1):
        velocity_x = 0
        velocity_y = -1
    elif e.keysym == "Down" and velocity_y != -1:
        velocity_x = 0
        velocity_y = 1
    elif (e.keysym == "Left" and velocity_x != 1):
        velocity_x = -1
        velocity_y = 0
    elif (e.keysym == "Right" and velocity_x != -1):
        velocity_x = 1
        velocity_y = 0

# function to move the snake
def move():
    global snake, food, snake_body, game_over, score  # import snake from outside function
    if (game_over):
        return
    if (snake.x <0 or snake.x >= WINDOW_WIDTH or snake.y <0 or snake.y >=WINDOW_HEIGHT):
        game_over = True
        return

    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    # check for collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    # update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i==0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y


    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE

# function to draw everything
def draw():
    global snake, food, snake_body, score, game_over   # global let's it pull a variable defined outside the function
    move()

    canvas.delete("all")  # every time you draw the new frame delete the previous one

    # draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    # draw the snake
    canvas.create_rectangle(snake.x,snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2,WINDOW_HEIGHT/2, font="Arial 20", text=f"Game over: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    window.after(100, draw)  # 100ms = 1/10 second, 10 frames/second draw da snake
draw()

# will listen for a key release and when it does hear that it calls change_direction
window.bind("<KeyRelease>", change_direction)
# lets the window run and stay open
window.mainloop()
