from clingo import *
import random
import tkinter
import time

M = 4
N = 4
L = M*N
ctl = Control("1")

ctl.load(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_one_hamiltonian_cycle_create_cycle.lp")
ctl.add("base", [], r"#const m = " + str(M) + ".")
ctl.add("base", [], r"#const n = " + str(N) + ".")
start_time = time.time()
ctl.ground([("base", [])])
result = ctl.solve(yield_=True)
end_time = time.time()
creating_cycle_time = end_time - start_time

for model in result:
    cycle_result = model.symbols(shown=True)
 
cycle = sorted([[i.arguments[0].number, i.arguments[1].number, i.arguments[2].number] for i in cycle_result if i.name == "cycle"], key=lambda x: x[2])
print("cycle: ", cycle)

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

ctl = Control("1")
ctl.load(r"C:\Users\tuang\Desktop\thesis_asp\snake_apple_one_hamiltonian_cycle_snake.lp")
ctl.add("base", [], r"#const m = " + str(M) + ".")
ctl.add("base", [], r"#const n = " + str(N) + ".")
for i in cycle:
    ctl.add("base", [], "cycle(" + str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + ").")
start_time = time.time()
ctl.ground([("base", [])])
end_time = time.time()
grounding_base_time = end_time - start_time
prepare_time = float(creating_cycle_time) + float(grounding_base_time)

run_time = []

for i in range(2, L+1):
    print("Step: ", i-1)

    apple_x, apple_y = random_apple(snake)
    apple_solution.append([apple_x, apple_y])
    print("Apple position: ", apple_x, apple_y)
    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), True)
    start_time = time.time()
    ctl.ground([("add_snake", [Number(i)])])
    result = ctl.solve(yield_=True)
    end_time = time.time()
    run_time.append(end_time - start_time)
    results = []
    for model in result:
        snake_result = model.symbols(atoms=True)
    
    new_snake = []
    for i in snake_result:
        if i.name == "new_snake":
            new_snake.append([i.arguments[0].number, i.arguments[1].number, i.arguments[2].number])

    ctl.assign_external(Function("apple", [Number(apple_x), Number(apple_y)]), False)

    snake = new_snake
    snake_solution.append(snake)

    print("snake :", snake)

print("prepare time: " + str(prepare_time))
print(run_time)



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
