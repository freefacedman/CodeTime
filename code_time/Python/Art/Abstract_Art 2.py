#NATIVE TO PY NO PIP
import turtle
import random
import math

screen = turtle.Screen()
screen.title("Wild Randomized Art Maker with Enhanced Shapes and Dull Colors")
screen.tracer(0)

turtle.colormode(255)

artist = turtle.Turtle()
artist.speed(0)
artist.width(2)
artist.penup()
artist.goto(0, 0)
artist.pendown()
artist.hideturtle()

colors = [
    (105, 105, 105), (112, 128, 144), (119, 136, 153), (47, 79, 79),
    (169, 169, 169), (128, 128, 128), (192, 192, 192), (211, 211, 211),
    (245, 245, 245), (220, 220, 220), (128, 128, 0), (189, 183, 107),
    (128, 0, 0), (139, 69, 19), (160, 82, 45), (210, 180, 140),
    (184, 134, 11), (218, 165, 32), (205, 133, 63), (222, 184, 135),
    (244, 164, 96), (210, 105, 30), (255, 140, 0), (255, 165, 0),
    (255, 215, 0), (218, 112, 214), (186, 85, 211), (148, 0, 211),
    (153, 50, 204), (138, 43, 226), (75, 0, 130), (72, 61, 139),
    (60, 179, 113), (46, 139, 87), (34, 139, 34), (85, 107, 47),
    (107, 142, 35), (154, 205, 50), (124, 252, 0), (127, 255, 0),
    (173, 255, 47), (0, 128, 0), (0, 100, 0), (0, 139, 139),
    (32, 178, 170), (0, 128, 128), (0, 255, 127)
]

def get_random_color():
    return random.choice(colors)

def draw_circle():
    artist.pencolor(get_random_color())
    radius = random.randint(10, 100)
    artist.circle(radius)

def draw_square():
    artist.pencolor(get_random_color())
    side = random.randint(20, 150)
    for _ in range(4):
        artist.forward(side)
        artist.left(90)

def draw_triangle():
    artist.pencolor(get_random_color())
    side = random.randint(20, 150)
    for _ in range(3):
        artist.forward(side)
        artist.left(120)

def draw_pentagon():
    artist.pencolor(get_random_color())
    side = random.randint(20, 150)
    for _ in range(5):
        artist.forward(side)
        artist.left(72)

def draw_hexagon():
    artist.pencolor(get_random_color())
    side = random.randint(20, 150)
    for _ in range(6):
        artist.forward(side)
        artist.left(60)

def draw_octagon():
    artist.pencolor(get_random_color())
    side = random.randint(20, 150)
    for _ in range(8):
        artist.forward(side)
        artist.left(45)

def draw_star():
    artist.pencolor(get_random_color())
    side = random.randint(20, 150)
    for _ in range(5):
        artist.forward(side)
        artist.right(144)

def draw_spiral():
    artist.pencolor(get_random_color())
    for _ in range(random.randint(50, 100)):
        artist.forward(random.uniform(1, 5))
        artist.left(random.uniform(-30, 30))

def draw_wave():
    artist.pencolor(get_random_color())
    for _ in range(random.randint(20, 50)):
        artist.forward(random.uniform(1, 3))
        artist.left(random.uniform(-10, 10))

def draw_curve():
    artist.pencolor(get_random_color())
    for _ in range(random.randint(10, 50)):
        artist.forward(random.uniform(1, 5))
        artist.left(random.uniform(-45, 45))

def draw_shape():
    shape = random.choice(['circle', 'square', 'triangle', 'pentagon', 'hexagon', 'octagon', 'star', 'spiral', 'wave', 'curve'])
    if shape == 'circle':
        draw_circle()
    elif shape == 'square':
        draw_square()
    elif shape == 'triangle':
        draw_triangle()
    elif shape == 'pentagon':
        draw_pentagon()
    elif shape == 'hexagon':
        draw_hexagon()
    elif shape == 'octagon':
        draw_octagon()
    elif shape == 'star':
        draw_star()
    elif shape == 'spiral':
        draw_spiral()
    elif shape == 'wave':
        draw_wave()
    elif shape == 'curve':
        draw_curve()

total_steps = 360
current_step = 0
radius = 600
num_layers = 35
running = True

def stop_animation():
    global running
    running = False

def change_background():
    screen.bgcolor(get_random_color())

def randomize_movement():
    global colors, num_layers, radius
    random.shuffle(colors)
    num_layers = random.randint(10, 35)
    radius = random.randint(200, 800)

def draw_step():
    global current_step
    if not running:
        return
    for layer in range(num_layers):
        angle = current_step + (layer * (360 / num_layers))
        rad = math.radians(angle)
        x = radius * math.cos(rad) + random.uniform(-300, 300)
        y = radius * math.sin(rad) + random.uniform(-300, 300)
        artist.goto(x, y)
        draw_shape()
    current_step = (current_step + 1) % total_steps
    screen.update()
    screen.ontimer(draw_step, 500)

def draw_specific_circle():
    draw_circle()

def draw_specific_square():
    draw_square()

def draw_specific_triangle():
    draw_triangle()

screen.listen()
screen.onkey(stop_animation, "i")
screen.onkey(randomize_movement, "r")
screen.onkey(change_background, "b")
screen.onkey(draw_specific_circle, "c")
screen.onkey(draw_specific_square, "s")
screen.onkey(draw_specific_triangle, "t")

change_background()
draw_step()

turtle.done()
#I = STOP
#R = RANDOMIZE
#C = CIRCLE
#S = SQUARE
#B = BACKGROUND
#T = TRIANGLE