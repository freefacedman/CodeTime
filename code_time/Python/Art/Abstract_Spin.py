#NATIVE TO PY NO PIP
import turtle
import random
import math

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Complex Randomized Art Maker with More Colors and Randomness")
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
    (255, 0, 0), (255, 127, 0), (255, 255, 0), (127, 255, 0),
    (0, 255, 0), (0, 255, 127), (0, 255, 255), (0, 127, 255),
    (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127),
    (255, 20, 147), (30, 144, 255), (34, 139, 34), (255, 105, 180),
    (75, 0, 130), (255, 215, 0), (173, 216, 230), (128, 0, 0),
    (0, 128, 128), (128, 0, 128), (255, 140, 0), (0, 255, 255),
    (210, 105, 30), (255, 20, 147), (0, 100, 0), (255, 192, 203),
    (144, 238, 144), (255, 182, 193), (255, 250, 205), (138, 43, 226),
    (255, 69, 0), (0, 191, 255), (154, 205, 50), (255, 160, 122),
    (65, 105, 225), (255, 255, 224), (176, 224, 230), (255, 99, 71),
    (154, 50, 205), (255, 165, 0), (0, 206, 209), (218, 112, 214)
]

def get_random_color():
    return random.choice(colors)

total_steps = 360
current_step = 0
radius = 400
num_layers = 15
running = True

def stop_animation():
    global running
    running = False

def draw_step():
    global current_step
    if not running:
        return
    for layer in range(num_layers):
        angle = current_step + (layer * (360 / num_layers))
        rad = math.radians(angle)
        x = radius * math.cos(rad) + random.uniform(-100, 100)
        y = radius * math.sin(rad) + random.uniform(-100, 100)
        artist.goto(x, y)
        artist.pencolor(get_random_color())
        artist.forward(random.uniform(5, 40))
        artist.left(random.uniform(-90, 90))
    current_step = (current_step + 1) % total_steps
    screen.update()
    screen.ontimer(draw_step, 10)

screen.listen()
screen.onkey(stop_animation, "i")

draw_step()

turtle.done()
#I =STOP
#R =RANDOMIZE