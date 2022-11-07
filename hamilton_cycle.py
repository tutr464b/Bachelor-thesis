from tkinter import *

with open(r'C:\Users\tuang\Desktop\asp\output.txt', 'r') as f:  
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

with open(r'C:\Users\tuang\Desktop\asp\snake.lp', 'r') as f:  
    snake = f.readlines()
    snake = [line.strip() for line in snake]
    snake = [line for line in snake if line]
    snake = [line for line in snake if line[0] != '%']

height = snake[0]
height = height.replace('.', ' ')
m = [int(s) for s in height.split() if s.isdigit()][0]

width = snake[1]
width = width.replace('.', ' ')
width.split(' ')	
n = [int(s) for s in width.split() if s.isdigit()][0]


SPACE_SIZE = 50
GAME_WIDTH = m * SPACE_SIZE
GAME_HEIGHT = n * SPACE_SIZE

window = Tk()
window.title("Hamiltonian Cycle")
window.resizable(False, False)

canvas = Canvas(window, bg="#FFFFFF", height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
window.update()

for i in range(len(list)):
    x = (list[i][1] - 1) * SPACE_SIZE
    y = (list[i][2] - 1) * SPACE_SIZE
    if (i >= 1):
        x1 = (list[i-1][1] - 1) * SPACE_SIZE
        y1 = (list[i-1][2] - 1) * SPACE_SIZE
        canvas.create_line(x + SPACE_SIZE/2, y + SPACE_SIZE/2, x1 + SPACE_SIZE/2, y1 + SPACE_SIZE/2, fill="#0000FF", width=SPACE_SIZE/10) 
    canvas.create_rectangle(x + 2/5*SPACE_SIZE, y + 2/5*SPACE_SIZE, x + 3/5*SPACE_SIZE, y + 3/5*SPACE_SIZE, fill="#FF0000", outline="#FFFFFF")
window.mainloop()