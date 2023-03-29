from clingo import *
import random
import time
from tkinter import *
import timeit

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

def myfunc(model):

    global lastmdl # quick and dirty approach using globals, proper implementation would include objects of classes

    lastmdl = model.symbols(atoms=True)

snake_solution = []
apple_solution = []
path_solution = []
step_length = []
snake = [[1, 1, 1]]
snake_solution.append(snake)
old_model = 0
time_end = time.time()
total_time += time_end - time_start

time_start = time.time()
ctl = Control("0")

ctl.load("path/to/multishot/snake_apple_multishot.lp")

ctl.add("base", [], r"#const m = " + str(M) + ".")
ctl.add("base", [], r"#const n = " + str(N) + ".")


ctl.ground([("base", [])])
time_end = time.time()
grounding_time += time_end - time_start
total_time += time_end - time_start

shortest_paths = []

for i in range(2, L + 1):
    iteration = i - 1
    time_start = time.time()
    x_head, y_head, z_head = snake[0]
    print("Iteration: ", i-1)

    apple_x, apple_y = random_apple(snake)
    apple_solution.append([apple_x, apple_y])
    print("Apple position: ", apple_x, apple_y)
    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), True)
    time_end = time.time()
    total_time += time_end - time_start

    time_start = time.time()
    ctl.ground([("add_snake", [Number(i)])])
    time_end = time.time()
    grounding_time += time_end - time_start
    total_time += time_end - time_start

    time_start = time.time()
    assumptions = [(Function("snake", [Number(x), Number(y), Number(z)]), True) for x, y, z in snake]
    time_end = time.time()
    total_time += time_end - time_start

    time_start = time.time()
    tic = timeit.default_timer()

    with ctl.solve(async_=True, assumptions=assumptions, on_model=myfunc) as handle:
        while not handle.wait(16):
            if timeit.default_timer() - tic > 60:
                handle.cancel()
                break
        model = lastmdl   
        if model == old_model:
            print("No solution")
            break 
    old_model = model
    time_end = time.time()
    solving_time += time_end - time_start
    total_time += time_end - time_start

    time_start = time.time()
    cycle = []
    new_snake = []
    for j in model:
        if j.name == "new_snake":
            new_snake.append([j.arguments[0].number, j.arguments[1].number, j.arguments[2].number])
        elif j.name == "cycle":
            cycle.append([j.arguments[0].number, j.arguments[1].number, j.arguments[2].number])

    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), False)
    time_end = time.time()
    total_time += time_end - time_start

    ctl_naive = Control("0")
    ctl_naive.load("path/to/naive/snake_apple_naive_shortest_path.lp")
    ctl_naive.add("base", [], r"#const m = " + str(M) + ".")
    ctl_naive.add("base", [], r"#const n = " + str(N) + ".")
    ctl_naive.ground([("base", []), ("add_snake", [Number(i)])])
    ctl_naive.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), True)
    result_naive = ctl_naive.solve(assumptions=assumptions, yield_=True)
    results_naive = []
    path = []
    for model in result_naive:
        results_naive.append(model.symbols(atoms=True))
    if len(results_naive) == 0:
        print("No solution")
    for j in results_naive[-1]:
        if j.name == "path":
            path.append([j.arguments[0].number, j.arguments[1].number])
    shortest_path = len(path) - 1
    shortest_paths.append(shortest_path)
    
    snake = sorted(new_snake, key=lambda x: x[2])
    new_snake_head = new_snake[0]
    snake_solution.append(snake)
    path_solution.append(cycle)

    print("cycle :", cycle)

    for j in cycle:
        if j[0] == x_head and j[1] == y_head:
            step_length.append(j[2] - 1)
            break    


    # with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_surplus_8.txt", "a") as f:
    #     f.write(str(step_length[-1] - shortest_path) + ", ")
    # with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_snake_8.txt", "a") as f:
    #     f.write(str(snake) + ", ")
    # with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_solving_time_8.txt", "a") as f:
    #     f.write(str(solving_time) + ", ")
    # with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_grounding_time_8.txt", "a") as f:
    #     f.write(str(grounding_time) + ", ")
    # with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_total_time_8.txt", "a") as f:
    #     f.write(str(total_time) + ", ")

surplus = [step_length[i] - shortest_paths[i] for i in range(len(step_length))]

print("Iteration " + str(iteration))
print("surplus steps taken " + str(surplus_step))
print("total computing time " + str(total_time))
print("ASP grounding time " + str(grounding_time))
print("ASP solving time " + str(solving_time))


# with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_surplus_8.txt", "a") as f:
#     f.write(str(surplus) + ", ")
# with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_total_time_8.txt", "a") as f:
#     f.write(str(total_time) + ", ")
# with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_grounding_time_8.txt", "a") as f:
#     f.write(str(grounding_time) + ", ")
# with open(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_multishot_solving_time_8.txt", "a") as f:
#     f.write(str(solving_time) + ", ")
################################################################
# # uncomment the following code to visualize the solution
# # now visualize the solution

# window = Tk()
# GAME_WIDTH = M*50
# GAME_HEIGHT = N*50


# canvas = Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg='white')
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
#     if [x, y] == snake_head:
#         snake_body_visualizes.append(canvas.create_rectangle((x-1)*50, (y-1)*50, x*50, y*50, fill='blue'))
#     else:
#         snake_body_visualizes.append(canvas.create_rectangle((x-1)*50, (y-1)*50, x*50, y*50, fill='green'))

# # now draw snake with iteration
# for i in range(len(path_solution)):
    
#     # first draw the apple
#     apple = apple_solution[i]
#     apple_visualize = canvas.create_oval((apple[0]-1)*50, (apple[1]-1)*50, apple[0]*50, apple[1]*50, fill='red')
#     window.update()
#     time.sleep(0.2)

#     # delete the old snake body
#     for snake_body_visualize in snake_body_visualizes:
#         canvas.delete(snake_body_visualize)
#     snake_body_visualizes = []
#     # draw the movement of the snake
#     path = sorted(path_solution[i], key=lambda x: x[2], reverse=True)
#     l = step_length[i]
    
#     for x, y, z in path:
#         if z > l:
#             continue
#         elif z <= l: 
#             # update the snake body
#             snake_head = [x, y]
#             snake_body.insert(0, snake_head)
#             if z != 1:
#                 snake_body.pop()
#             else:
#                 canvas.delete(apple_visualize)
#             for snake_body_visualize in snake_body_visualizes:
#                 canvas.delete(snake_body_visualize)
#             # draw the new snake body
#             for x, y in snake_body:
#                 if [x, y] == snake_head:
#                     snake_body_visualizes.append(canvas.create_rectangle((x-1)*50, (y-1)*50, x*50, y*50, fill='blue'))
#                 else: 
#                     snake_body_visualizes.append(canvas.create_rectangle((x-1)*50, (y-1)*50, x*50, y*50, fill='green'))
#             window.update()
#             time.sleep(0.2)


# window.mainloop()


# window.mainloop()

                



