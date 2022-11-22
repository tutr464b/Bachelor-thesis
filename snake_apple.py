from tkinter import *
import time

window = Tk()

snake = [[2,4], [1,4], [1,3], [1,2], [1,1] ]

def draw_snake(snake):

    snake_draw = []
    if snake != NONE:
        for i in range(len(snake)):
            x = (snake[i][0] - 1) * SPACE_SIZE
            y = (snake[i][1] - 1) * SPACE_SIZE
            if (i >= 1):
                x1 = (snake[i-1][0] - 1) * SPACE_SIZE
                y1 = (snake[i-1][1] - 1) * SPACE_SIZE
                snake_part = canvas.create_line(x + SPACE_SIZE/2, y + SPACE_SIZE/2, x1 + SPACE_SIZE/2, y1 + SPACE_SIZE/2, fill="#0000FF", width=SPACE_SIZE/10) 
                
                if (i == len(snake) - 1):
                    snake_tail = snake_part
                else:
                    snake_draw.append(snake_part)
            if(i == 0):
                head = canvas.create_rectangle(x + 1/3*SPACE_SIZE, y + 1/3*SPACE_SIZE, x + 2/3*SPACE_SIZE, y + 2/3*SPACE_SIZE, fill="#00FF00", outline="#FFFFFF")

        window.update()
    return snake_draw, head, snake_tail


def draw_apple(apple):
    x = (apple[0] - 1) * SPACE_SIZE
    y = (apple[1] - 1) * SPACE_SIZE
    apple_draw = canvas.create_oval(x + 1/4*SPACE_SIZE, y + 1/4*SPACE_SIZE, x + 3/4*SPACE_SIZE, y + 3/4*SPACE_SIZE, fill="#FF0000", outline="#FFFFFF")
    window.update()
    return apple_draw

with open(r'C:\Users\tuang\Desktop\asp\snake_apple.txt', 'r') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    lines = [line for line in lines if line[0] != '%']

cycle = lines[-9]

cycle = cycle.split()
list = []
for i in cycle:
    (L, M, N) = i[6:-1].split(',')
    L, M, N = int(L), int(M), int(N)
    list.append([L, M, N])

m, n = 5, 5

apple = [3, 4]

SPACE_SIZE = 50
GAME_WIDTH = m * SPACE_SIZE
GAME_HEIGHT = n * SPACE_SIZE


window.title("snake eating apple")
window.resizable(False, False)

canvas = Canvas(window, bg="#FFFFFF", height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


for i in range(m):
    for j in range(n):
        x = i * SPACE_SIZE
        y = j * SPACE_SIZE
        canvas.create_rectangle(x + 2/5*SPACE_SIZE, y + 2/5*SPACE_SIZE, x + 3/5*SPACE_SIZE, y + 3/5*SPACE_SIZE, fill="#FF0000", outline="#FFFFFF")

apple_draw = draw_apple(apple)

# create node that the snake can go over


snake_draw, snake_head, snake_tail = draw_snake(snake)
window.update()
time.sleep(1)

update_position = len(list)
while(snake[0] != apple):
 
    canvas.delete(snake_head)
    for snake_body in snake_draw:
        canvas.delete(snake_body)
    
    snake.pop()
    snake.insert(0, [list[update_position - 1][1], list[update_position - 1][2]])
    if (snake[0] != apple):
        canvas.delete(snake_tail)
    else:
        canvas.delete(apple_draw)
    snake_draw, snake_head, snake_tail = draw_snake(snake)
    update_position -= 1
    time.sleep(1)
    window.update()

window.mainloop()
