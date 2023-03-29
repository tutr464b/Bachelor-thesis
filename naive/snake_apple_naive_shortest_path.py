import time
from clingo import *
import random

total_time = 0
grounding_time = 0
solving_time = 0

time_start = time.time()

M = 8
N = 8
L = M*N



def random_apple(snake):
    # function to generate random apple position
    exclude = [N*(X-1) + Y for X, Y, _ in snake]
    random_list = [x for x in range(1, L + 1) if x not in exclude]
    ran = random.choice(random_list)
    q = ran%N
    p = ran//N + 1
    if (q == 0):
        q = N
        p = p - 1
    return p, q

snake = [[1, 1, 1]]
snake_solution = []
snake_solution.append(snake)
path_solution = []
apple_solution = []

time_end = time.time()
total_time += time_end - time_start

for i in range(2, L + 1):
    time_start = time.time()
    ctl = Control("0")
    ctl.load(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_naive_shortest_path.lp")
    ctl.add("base", [], r"#const m = " + str(M) + ".")
    ctl.add("base", [], r"#const n = " + str(N) + ".")
    ctl.ground([("base", []), ("add_snake", [Number(i)])])
    time_end = time.time()
    grounding_time += time_end - time_start
    total_time += time_end - time_start
    time_start = time.time()
    apple_x, apple_y = random_apple(snake)
    apple_solution.append([apple_x, apple_y])
    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), True)
    assumptions = [(Function("snake", [Number(x), Number(y), Number(z)]), True) for x, y, z in snake]
    time_end = time.time()
    total_time += time_end - time_start
    time_start = time.time()
    result = ctl.solve(yield_=True, assumptions=assumptions)
    time_end = time.time()
    solving_time += time_end - time_start
    total_time += time_end - time_start
    time_start = time.time()
    results = []
    for model in result:
        results.append(model.symbols(atoms=True))
    if len(results) == 0:
        break
    path = []
    new_snake = []
    for i in results[-1]:
        if i.name == "new_snake":
            new_snake.append([i.arguments[0].number, i.arguments[1].number, i.arguments[2].number])
        elif i.name == "path":
            path.append([i.arguments[0].number, i.arguments[1].number, i.arguments[2].number])

    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), False)
    snake = new_snake
    snake_solution.append(snake)
    path_solution.append(path)
    time_end = time.time()
    total_time += time_end - time_start

# here total computing time, ASP grounding time, ASP solving time, number of steps taken can be stored in files or printed out here
print("total time" + str(total_time))
print("ASP grounding time" + str(grounding_time))
print("ASP solving time" + str(solving_time))
    
## now visualize the solution
## uncomment to visualize
# import tkinter
# window = tkinter.Tk()

# GAME_WIDTH = M*50
# GAME_HEIGHT = N*50


# canvas = tkinter.Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg='white')
# canvas.pack()

# # draw grid 
# for i in range(N):
#     canvas.create_line(0, i*50, GAME_WIDTH, i*50, fill='black')
# for i in range(M):
#     canvas.create_line(i*50, 0, i*50, GAME_HEIGHT, fill='black')

# # draw the initial snake

# snake = snake_solution [0]
# snake_body_unsorted = []
# for x, y, z in snake:
#     if z == 1:
#         snake_head = [x, y]
#     snake_body_unsorted.append([x, y, z])
# snake_body_unsorted = sorted(snake_body_unsorted, key=lambda x: x[2])
# snake_body = [[x, y] for x, y, z in snake_body_unsorted]
# snake_body_visualizes = []
# for x, y in snake_body:
#     snake_body_visualizes.append(canvas.create_rectangle((x-1)*50, (y-1)*50, x*50, y*50, fill='green'))
# print(snake_body)

# # now draw snake with iteration
# for i in range(len(path_solution)):
#     print("next step")
    
#     # first draw the apple
#     apple = apple_solution[i]
#     apple_visualize = canvas.create_oval((apple[0]-1)*50, (apple[1]-1)*50, apple[0]*50, apple[1]*50, fill='red')
#     window.update()
#     time.sleep(1)

#     # delete the old snake body
#     for snake_body_visualize in snake_body_visualizes:
#         canvas.delete(snake_body_visualize)
#     snake_body_visualizes = []
#     # draw the movement of the snake
#     path = sorted(path_solution[i], key=lambda x: x[2], reverse=True)
#     for x, y, z in path:
#         if z != len(path): 
#             # update the snake body
#             snake_head = [x, y]
#             snake_body.insert(0, snake_head)
#             if z != 1:
#                 snake_body.pop()
#             else:
#                 canvas.delete(apple_visualize)
#             print(snake_body)
#             for snake_body_visualize in snake_body_visualizes:
#                 canvas.delete(snake_body_visualize)
#             # draw the new snake body
#             for x, y in snake_body:
#                 snake_body_visualizes.append(canvas.create_rectangle((x-1)*50, (y-1)*50, x*50, y*50, fill='green'))
#             window.update()
#             time.sleep(1)


# last_apple = apple_solution[-1]
# canvas.create_oval((last_apple[0]-1)*50, (last_apple[1]-1)*50, last_apple[0]*50, last_apple[1]*50, fill='red')


# window.mainloop()


# window.mainloop()

                


