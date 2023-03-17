import turtle
from random import randint

# screen settings
WIDTH, HEIGHT = 1200, 800
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.screensize(3 * WIDTH, 3 * HEIGHT)
screen.bgcolor('black')
screen.delay(0)

# turtle settings

leo = turtle.Turtle()
leo.pensize(3)
leo.speed(0)
leo.setpos(0, -HEIGHT // 2)
leo.color('green')

# 1 - system settings

gens = 8
axiom = 'XY'
chr_1, rule_1 = 'X', 'F[@[-X]+X]'

step = 80
angle = lambda: randint(0, 45)
stak = []
color = [0.35, 0.2, 0.0]
thinkness = 20


def apply_ryles(axiom):
    # res = ''
    # for char in axiom:
    #     if char == chr_1:
    #         res += rule_1
    #     else:
    #         res += rule_2
    # return res
    return "".join([rule_1 if char == chr_1 else char for char in axiom])


def get_result(gens, axiom):
    for gen in range(gens):
        axiom = apply_ryles(axiom)
    return axiom


turtle.pencolor('white')
turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 - 100)
turtle.clear()
turtle.write(f"generation: {gens}", font=('Arial', 60, 'normal'))

axiom = get_result(gens, axiom)
leo.left(180)
leo.pensize(thinkness)

leo.setheading(0)
leo.goto(0, 0)
leo.clear()

for char in axiom:
    leo.color(color)
    if char == "F" or char == 'X':
        leo.forward(step)
    elif char == '@':
        step -= 6
        color[1] += 0.04
        thinkness -= 2
        thinkness = max(1, thinkness)
        leo.pensize(thinkness)
    elif char == '+':
        leo.right(angle())
    elif char == '-':
        leo.left(angle())
    elif char == '[':
        angle_, pos_ = leo.heading(), leo.pos()
        stak.append((angle_, pos_, thinkness, step, color[1]))
    elif char == ']':
        angle_, pos_, thinkness, step, color[1] = stak.pop()
        leo.pensize(thinkness)
        leo.setheading(angle_)
        leo.penup()
        leo.goto(pos_)
        leo.pendown()
screen.exitonclick()
