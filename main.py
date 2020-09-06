import sys
import turtle
import random
import copy

from draw import draw_path, draw_bounding_box

def get_new_position(position, move):
    assert move in list('rldu')
    assert len(position) == 2

    moves = { 'r': (1, 0), 'l': (-1, 0), 'u': (0, 1), 'd': (0, -1) }
    move = moves[move]
    new_position = tuple(sum(x) for x in zip(position, move))
    return new_position

def is_out_of_bounds(position, map_height, map_width):
    w, h = map_width, map_height
    x, y = position[0], position[1]


    if 0 <= x < w and 0 <= y < h:
        return False

    # print (x, y)
    return True

def build_visited_list(path, start=(0,0)):
    visited = [start]
    current_position = start
    for move in path:
        current_position = get_new_position(current_position, move)
        visited.append(current_position)
    return visited


def gen_path_backtrack(length, path='r', visited=None, where_im_at=None):
    if gen_path_backtrack.best_len == None:
        gen_path_backtrack.best_len = len(path)
    elif len(path) > gen_path_backtrack.best_len:
        gen_path_backtrack.best_len = len(path)
        gen_path_backtrack.moves_without_improvement = 0
        print(
            str(gen_path_backtrack.best_len).zfill(3),
            str(len(path)).zfill(3),
            path,
        )

    gen_path_backtrack.moves_without_improvement += 0

    global t
    global cell_size
    t.reset()
    t.speed('fastest')
    t.penup()
    t.setposition(0, 0)
    draw_path(t, path, cell_size)
    turtle.update()


    # List with position in the grid that i've already passed by.
    if visited == None:
        visited = [(0, 0)]

    # TODO: This will change depending on the starting move
    if where_im_at == None:
        where_im_at = (1, 0)

    # Keep track of where I've been so as to not allow overlap
    visited.append(where_im_at)

    # I think I need a stop condition here.
    # For now, the condition will just be a length
    if len(path) >= length-1:
        return path

    # Try and generate the next move recursively
    possible_moves = list('rldu')
    random.shuffle(possible_moves)
    extended_path = None
    while len(possible_moves) > 0:
        candidate_move = possible_moves.pop()
        where_id_be = get_new_position(where_im_at, candidate_move)

        # print(path + candidate_move)

        # it'll overlap, skip it
        if where_id_be in visited:
            continue

        # it's out of bounds, skip it
        # but there's no need to test this if it is the very last move
        if len(path) < length and is_out_of_bounds(where_id_be, map_height, map_width):
            continue

        extended_path = gen_path_backtrack(length, path + candidate_move, copy.copy(visited), where_id_be)

        # if nothing went wrong furthen along, then we don't have to try anymore
        if extended_path != None:
            break

    return extended_path
gen_path_backtrack.best_len = None
gen_path_backtrack.moves_without_improvement = 0

# These parameters that should come from the command line

# Cell size in pixels
cell_size = 25

# Map width in cells
map_width = 30

# Map height in cells
map_height = 30

# Number of holes
num_holes = 167

# Wall thickness in pixels.
wall_thickness = 1

# screen = turtle.getscreen()

t = turtle.Turtle()
s = t.getscreen()
s.setup(width=500, height=500)
s.setworldcoordinates(-2, -2, map_width * cell_size + 4, map_height * cell_size + 4)
turtle.tracer(0, 0)

while True:
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print("Seed:", seed)

    t.reset()
    t.speed('fastest')
    t.pensize(wall_thickness)
    t.penup()

    draw_bounding_box(t, cell_size, map_height, map_width)
    length = map_height * map_width
    path = gen_path_backtrack(length - num_holes)

    # if path == None:
    #     continue

    print("Path:", path)
    draw_path(t, path, cell_size)

    t.penup()
    t.setposition(0, 0)
    turtle.update()

    # break

t.hideturtle()
turtle.exitonclick()
