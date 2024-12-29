import turtle, random, math

screen = turtle.Screen()
screen.title("Interactive Random Art Maker")
screen.bgcolor(random.choice([
    "dimgray", "slategray", "darkslategray", "gray", "darkolivegreen",
    "sienna", "chocolate", "peru", "saddlebrown", "olive", "darkgreen",
    "rosybrown", "khaki", "burlywood", "tan", "darkgoldenrod",
    "darkseagreen", "mediumseagreen", "seagreen", "forestgreen",
    "darkorchid", "mediumpurple", "darkviolet", "indigo"
]))
screen.setup(width=1000, height=800)
screen.tracer(1)
turtle.colormode(255)

artist = turtle.Turtle()
artist.speed(0)
artist.width(2)
artist.penup()
artist.goto(0,0)
artist.pendown()
artist.hideturtle()

colors = [
    (105,105,105),(112,128,144),(119,136,153),(47,79,79),(169,169,169),
    (128,128,128),(192,192,192),(211,211,211),(245,245,245),(220,220,220),
    (128,128,0),(189,183,107),(128,0,0),(139,69,19),(160,82,45),
    (210,180,140),(184,134,11),(218,165,32),(205,133,63),(222,184,135),
    (244,164,96),(210,105,30),(255,140,0),(255,165,0),(255,215,0),
    (218,112,214),(186,85,211),(148,0,211),(153,50,204),(138,43,226),
    (75,0,130),(72,61,139),(60,179,113),(46,139,87),(34,139,34),
    (85,107,47),(107,142,35),(154,205,50),(124,252,0),(127,255,0),
    (173,255,47),(0,128,0),(0,100,0),(0,139,139),(32,178,170),
    (0,128,128),(0,255,127)
]

def get_random_color():
    return random.choice(colors)

def draw_circle():
    artist.pencolor(get_random_color())
    radius = random.randint(10,200)
    artist.circle(radius)

def draw_square():
    artist.pencolor(get_random_color())
    side = random.randint(20,200)
    for _ in range(4):
        artist.forward(side)
        artist.left(90)

def draw_triangle():
    artist.pencolor(get_random_color())
    side = random.randint(20,200)
    for _ in range(3):
        artist.forward(side)
        artist.left(120)

def draw_pentagon():
    artist.pencolor(get_random_color())
    side = random.randint(20,200)
    for _ in range(5):
        artist.forward(side)
        artist.left(72)

def draw_hexagon():
    artist.pencolor(get_random_color())
    side = random.randint(20,200)
    for _ in range(6):
        artist.forward(side)
        artist.left(60)

def draw_octagon():
    artist.pencolor(get_random_color())
    side = random.randint(20,200)
    for _ in range(8):
        artist.forward(side)
        artist.left(45)

def draw_star():
    artist.pencolor(get_random_color())
    side = random.randint(20,200)
    for _ in range(5):
        artist.forward(side)
        artist.right(144)

def draw_spiral():
    artist.pencolor(get_random_color())
    for _ in range(random.randint(50,150)):
        artist.forward(random.uniform(1,5))
        artist.left(random.uniform(-30,30))

def draw_wave():
    artist.pencolor(get_random_color())
    for _ in range(random.randint(20,100)):
        artist.forward(random.uniform(1,3))
        artist.left(random.uniform(-10,10))

def draw_curve():
    artist.pencolor(get_random_color())
    for _ in range(random.randint(10,100)):
        artist.forward(random.uniform(1,5))
        artist.left(random.uniform(-45,45))

def draw_diamond():
    artist.pencolor(get_random_color())
    side = random.randint(20,200)
    for _ in range(2):
        artist.forward(side)
        artist.left(60)
        artist.forward(side)
        artist.left(120)

def draw_ellipse():
    artist.pencolor(get_random_color())
    artist.speed(1)
    for i in range(360):
        angle = math.radians(i)
        x = random.randint(50,200) * math.cos(angle)
        y = random.randint(25,100) * math.sin(angle)
        artist.goto(x, y)
    artist.speed(0)

def draw_heart():
    artist.pencolor(get_random_color())
    artist.fillcolor(get_random_color())
    artist.begin_fill()
    artist.left(140)
    artist.forward(random.randint(50,200))
    for _ in range(200):
        angle = math.radians(1)
        artist.right(angle)
        artist.forward(random.uniform(1,3))
    artist.left(120)
    for _ in range(200):
        angle = math.radians(1)
        artist.right(angle)
        artist.forward(random.uniform(1,3))
    artist.forward(random.randint(50,200))
    artist.end_fill()
    artist.setheading(0)

def change_background():
    screen.bgcolor(get_random_color())

def clear_screen():
    artist.clear()

def increase_pen_size():
    current_width = artist.width()
    if current_width <10:
        artist.width(current_width+1)

def decrease_pen_size():
    current_width = artist.width()
    if current_width >1:
        artist.width(current_width-1)

def change_pen_color():
    artist.pencolor(get_random_color())

def undo_action():
    artist.undo()

def show_legend():
    print("""
Legend of Keyboard Controls:
---------------------------
c - Draw Circle
s - Draw Square
t - Draw Triangle
p - Draw Pentagon
h - Draw Hexagon
o - Draw Octagon
k - Draw Star
l - Draw Spiral
w - Draw Wave
u - Draw Curve
d - Draw Diamond
e - Draw Ellipse
a - Draw Heart
b - Change Background Color
x - Clear Screen
+ - Increase Pen Size
- - Decrease Pen Size
q - Change Pen Color
z - Undo Last Action
n - Show Legend
""")

screen.listen()
screen.onkey(draw_circle, "c")
screen.onkey(draw_square, "s")
screen.onkey(draw_triangle, "t")
screen.onkey(draw_pentagon, "p")
screen.onkey(draw_hexagon, "h")
screen.onkey(draw_octagon, "o")
screen.onkey(draw_star, "k")
screen.onkey(draw_spiral, "l")
screen.onkey(draw_wave, "w")
screen.onkey(draw_curve, "u")
screen.onkey(draw_diamond, "d")
screen.onkey(draw_ellipse, "e")
screen.onkey(draw_heart, "a")
screen.onkey(change_background, "b")
screen.onkey(clear_screen, "x")
screen.onkey(increase_pen_size, "+")
screen.onkey(decrease_pen_size, "-")
screen.onkey(change_pen_color, "q")
screen.onkey(undo_action, "z")
screen.onkey(show_legend, "n")
show_legend()
screen.update()
turtle.done()
