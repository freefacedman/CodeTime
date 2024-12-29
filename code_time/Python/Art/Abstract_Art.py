#NATIVE TO PY NO PIP
import turtle
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Randomized Art Maker Animation")

colors = ["red", "blue", "green", "yellow", "purple", "orange", "white", "cyan", "magenta", "lime"]

artist = turtle.Turtle()
artist.speed(0)
artist.width(2)
artist.penup()
artist.goto(0, 0)
artist.pendown()

def random_move():
    angle = random.randint(0, 360)
    distance = random.randint(10, 30)
    artist.color(random.choice(colors))
    artist.setheading(angle)
    artist.forward(distance)

while True:
    random_move()

turtle.done()
