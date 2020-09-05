import sys
import turtle
import random

from draw import draw_path, draw_bounding_box

def choose_next_move(last_move):
    moves = list('rlud')
    assert last_move in moves

    if last_move == 'r':
        return random.choice(list('rud'))
    if last_move == 'l':
        return random.choice(list('lud'))
    if last_move == 'u':
        return random.choice(list('rul'))
    if last_move == 'd':
        return random.choice(list('rld'))

    raise ValueError('Pretty sure I asserted that it shouldn\'t reach this')

def generate_path():
    path = 'r'
    for i in range(23):
        last_move = path[-1]
        path += choose_next_move(last_move)
    return path

def where_would_i_be(where_im_at, move):
    assert move in list('rldu')
    assert len(where_im_at) == 2

    if move == 'r':
        return (where_im_at[0]+1, where_im_at[1])
    if move == 'l':
        return (where_im_at[0]-1, where_im_at[1])
    if move == 'u':
        return (where_im_at[0], where_im_at[1]+1)
    if move == 'd':
        return (where_im_at[0], where_im_at[1]-1)

def generate_path_recursive(path='r', where_ive_been=None, where_im_at=None):
    # if path == 'ruruurdrrdlldldrdruru':
    print(path)

    # List with position in the grid that i've already passed by.
    if where_ive_been == None:
        where_ive_been = [(0, 0)]

    # TODO: This will change depending on the starting move
    if where_im_at == None:
        where_im_at = (1, 0)

    # Keep track of where I've been so as to not allow overlap
    where_ive_been.append(where_im_at)

    # I think I need a stop condition here.
    # For now, the condition will just be a length
    if len(path) >= 25:
        return path

    # Try and generate the next move recursively
    possible_moves = list('rldu')
    random.shuffle(possible_moves)
    extended_path = None
    while len(possible_moves) > 0:
        candidate_move = possible_moves.pop()
        where_id_be = where_would_i_be(where_im_at, candidate_move)

        # it'll overlap, skip it
        if where_id_be in where_ive_been:
            continue

        extended_path = generate_path_recursive(path + candidate_move, where_ive_been, where_id_be)

        # if nothing went wrong furthen along, then we don't have to try anymore
        if extended_path != None:
            break

    return extended_path



# These parameters that should come from the command line

# Cell size in pixels
cell_size = 25

# Map width in cells
map_width = 5

# Map height in cells
map_height = 5

# Wall thickness in pixels.
wall_thickness = 1

# screen = turtle.getscreen()
# screen.setworldcoordinates(0, 0, map_width * cell_size, map_height * cell_size)

t = turtle.Turtle()
# t.setposition(0, (map_height-1) * cell_size)


# path = 'rdldddrruluruurrdldrdldr'
# path = 'rrullddrrddlulldlulldrdr'

while True:
    # seed = random.randrange(sys.maxsize)
    seed = 7905049820465421464
    random.seed(seed)
    print("Seed:", seed)

    t.reset()
    t.speed('fastest')
    t.pensize(wall_thickness)
    t.penup()

    path = generate_path_recursive()
    print("Path:", path)
    draw_path(t, path, cell_size)

    break
    t.penup()
    t.setposition(0, 0)


# t.hideturtle()
turtle.exitonclick()
# turtle.mainloop()
