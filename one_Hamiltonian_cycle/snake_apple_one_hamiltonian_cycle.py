from clingo import *
import random
import tkinter
import time

total_time = 0
grounding_time = 0
solving_time = 0

time_start = time.time()
M = 8
N = 8
L = M*N

time_end = time.time()
total_time += time_end - time_start

time_start = time.time()
ctl = Control("1")
ctl.load("path\to\one_Hamiltonian_cycle\snake_apple_one_hamiltonian_cycle_create_cycle.lp")
ctl.add("base", [], r"#const m = " + str(M) + ".")
ctl.add("base", [], r"#const n = " + str(N) + ".")
ctl.ground([("base", [])])
time_end = time.time()
grounding_time += time_end - time_start
total_time += time_end - time_start

time_start = time.time()
result = ctl.solve(yield_=True)
time_end = time.time()
solving_time += time_end - time_start
total_time += time_end - time_start

time_start = time.time()
old_model = 0
for model in result:
    cycle_result = model.symbols(shown=True)

cycle = sorted([[i.arguments[0].number, i.arguments[1].number, i.arguments[2].number] for i in cycle_result if i.name == "cycle"], key=lambda x: x[2])

def myfunc(model):

    global lastmdl # quick and dirty approach using globals, proper implementation would include objects of classes

    lastmdl = model.symbols(atoms=True)

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

snake_solution = []

snake = [[1, 1, 1]]
snake_solution.append(snake)
apple_solution = []

time_end = time.time()
total_time += time_end - time_start

time_start = time.time()
ctl = Control("1")
ctl.load("path\to\one_Hamiltonian_cycle\snake_apple_one_hamiltonian_cycle_snake.lp")
ctl.add("base", [], r"#const m = " + str(M) + ".")
ctl.add("base", [], r"#const n = " + str(N) + ".")
for i in cycle:
    ctl.add("base", [], "cycle(" + str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + ").")
ctl.ground([("base", [])])
end_time = time.time()
grounding_time += end_time - time_start
total_time += end_time - time_start

for i in range(2, L+1):
    # the following part is to measure the surplus step taken 
    ctl_naive = Control("0")
    ctl_naive.load("path/to/naive/snake_apple_naive_shortest_path.lp")
    ctl_naive.add("base", [], r"#const m = " + str(M) + ".")
    ctl_naive.add("base", [], r"#const n = " + str(N) + ".")
    ctl_naive.ground([("base", []), ("add_snake", [Number(i)])])
    apple_x, apple_y = random_apple(snake)
    print("apple: ", apple_x, apple_y)
    apple_solution.append([apple_x, apple_y])
    ctl_naive.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), True)
    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), True)
    assumptions = [(Function("snake", [Number(x), Number(y), Number(z)]), True) for x, y, z in snake]
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
        
    time_start = time.time()
    apple_x, apple_y = random_apple(snake)
    apple_solution.append([apple_x, apple_y])
    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), True)
    time_end = time.time()
    total_time += time_end - time_start

    time_start = time.time()
    ctl.ground([("add_snake", [Number(i)])])
    time_end = time.time()
    grounding_time += time_end - time_start
    total_time += time_end - time_start

    time_start = time.time()
    tic = timeit.default_timer()

    with ctl.solve(async_=True,on_model=myfunc) as handle:
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
    new_snake = []
    for j in model:
        if j.name == "new_snake":
            new_snake.append([j.arguments[0].number, j.arguments[1].number, j.arguments[2].number])

    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), False)
    
    time_end = time.time()
    total_time += time_end - time_start
    for j in snake_result:
        if j.name == "new_snake":
            new_snake.append([j.arguments[0].number, j.arguments[1].number, j.arguments[2].number])
    snake.sort(key=lambda x: x[2])
    old_snake_head = snake[0]
    new_snake.sort(key=lambda x: x[2])
    new_snake_head = new_snake[0]
    for j in cycle:
        if j[0] == old_snake_head[0] and j[1] == old_snake_head[1]:
            old_snake_head_index = j[2]
        if j[0] == new_snake_head[0] and j[1] == new_snake_head[1]:
            new_snake_head_index = j[2]
    if new_snake_head_index < old_snake_head_index:
        actual_path = old_snake_head_index - new_snake_head_index
    else:
        actual_path = old_snake_head_index + L - new_snake_head_index
    actual_paths.append(actual_path)
    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), False)

    snake = new_snake
    snake_solution.append(snake)

surplus_step = [actual_paths[i] - shortest_paths[i] for i in range(len(actual_paths))]
print("surplus steps taken " + str(surplus_step))
print("total computing time " + str(total_time))
print("ASP grounding time " + str(grounding_time))
print("ASP solving time " + str(solving_time))

# # now visualize the solution
# window = tkinter.Tk()

# GAME_WIDTH = N*50
# GAME_HEIGHT = M*50

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

# head_pos = 1
# def next(l):
#     if l == 1:
#         return 16
#     else:
#         return l - 1

# for i in range(L - 1):
    
#     # first draw the apple
#     apple = apple_solution[i]
#     apple_visualize = canvas.create_oval((apple[0]-1)*50, (apple[1]-1)*50, apple[0]*50, apple[1]*50, fill='red')
#     window.update()
#     time.sleep(0.25)
    
#     # draw the movement of the snake
#     while snake_head != apple:
#         for snake_body_visualize in snake_body_visualizes:
#             canvas.delete(snake_body_visualize)
#         snake_body_visualizes = []
#         # move the snake head
#         for x, y, z in cycle:
#             if z == head_pos:
#                 snake_head = [x, y]
#                 break
            
#         snake_body.insert(0, snake_head)
#         if snake_head != apple:
#             snake_body.pop()
#         else: 
#             canvas.delete(apple_visualize)
#             print(snake_body)

#         for x, y in snake_body:
#             snake_body_visualizes.append(canvas.create_rectangle((x-1)*50, (y-1)*50, x*50, y*50, fill='green'))

#         window.update()
#         time.sleep(0.25)

#         head_pos = next(head_pos)




# window.mainloop()
