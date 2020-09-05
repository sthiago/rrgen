import sys
import turtle
import random

def validate_start_cell(cell):
    """start can't be 'd', worms would fall"""
    valid_path_chars = 'rlu'
    if len(cell) != 1:
        raise ValueError('start cell must be a single character')
    for ch in cell:
        if ch not in valid_path_chars:
            raise ValueError('start cell can only be r, l, or u')

def validate_cell(cell):
    valid_path_chars = 'rldu'
    if len(cell) != 2:
        raise ValueError('cell must be a str with length of 2')
    for ch in cell:
        if ch not in valid_path_chars:
            raise ValueError('cell letters can only be r, l, d, or u')

# All draw_x_wall functions presume the turtle at bottom-left facing right

def draw_left_wall(t, size):
    t.pd()
    t.lt(90)
    t.fd(size)
    t.pu()
    t.bk(size)
    t.rt(90)

def draw_right_wall(t, size):
    pos = t.pos()
    t.pu()
    t.fd(size)
    t.lt(90)
    t.pd()
    t.fd(size)
    t.pu()
    t.setpos(pos)
    t.rt(90)

def draw_top_wall(t, size):
    pos = t.pos()
    t.pu()
    t.lt(90)
    t.fd(size)
    t.rt(90)
    t.pd()
    t.fd(size)
    t.pu()
    t.setpos(pos)

def draw_down_wall(t, size):
    t.pd()
    t.fd(size)
    t.pu()
    t.bk(size)

def box(t):
    draw_left_wall(t, 50)
    draw_right_wall(t, 50)
    draw_top_wall(t, 50)
    draw_down_wall(t, 50)

def draw_start_cell(t, cell, size):
    validate_start_cell(cell)
    x, y = t.pos()
    if cell == 'r':
        draw_left_wall(t, size)
        draw_top_wall(t, size)
        draw_down_wall(t, size)
        t.setpos(x + size, y)
    elif cell == 'l':
        draw_right_wall(t, size)
        draw_top_wall(t, size)
        draw_down_wall(t, size)
        t.setpos(x - size, y)
    elif cell == 'u':
        draw_left_wall(t, size)
        draw_right_wall(t, size)
        draw_down_wall(t, size)
        t.setpos(x, y - size)

def draw_end_cell(t, last_cell, size):
    # todo: adicionar validate
    if last_cell == 'r':
        draw_top_wall(t, size)
        draw_down_wall(t, size)
        draw_right_wall(t, size)
    elif last_cell == 'l':
        draw_top_wall(t, size)
        draw_down_wall(t, size)
        draw_left_wall(t, size)
    elif last_cell == 'u':
        draw_top_wall(t, size)
        draw_right_wall(t, size)
        draw_left_wall(t, size)
    elif last_cell == 'd':
        draw_down_wall(t, size)
        draw_right_wall(t, size)
        draw_left_wall(t, size)


def draw_cell(t, cell, size):
    """draw_cell presumes t is in lower left corner of cell[1] pointing right."""
    validate_cell(cell)
    x, y = t.pos()

    if cell == 'rr' or cell == 'll':
        draw_top_wall(t, size)
        draw_down_wall(t, size)
    elif cell in ['rl', 'lr', 'ud', 'du']:
        pass
    elif cell == 'rd':
        draw_top_wall(t, size)
        draw_right_wall(t, size)
    elif cell == 'ru':
        draw_down_wall(t, size)
        draw_right_wall(t, size)
    elif cell == 'ld':
        draw_top_wall(t, size)
        draw_left_wall(t, size)
    elif cell == 'lu':
        draw_down_wall(t, size)
        draw_left_wall(t, size)
    elif cell == 'dr':
        draw_down_wall(t, size)
        draw_left_wall(t, size)
    elif cell == 'dl':
        draw_right_wall(t, size)
        draw_down_wall(t, size)
    elif cell == 'dd' or cell == 'uu':
        draw_right_wall(t, size)
        draw_left_wall(t, size)
    elif cell == 'ur':
        draw_top_wall(t, size)
        draw_left_wall(t, size)
    elif cell == 'ul':
        draw_top_wall(t, size)
        draw_right_wall(t, size)

    # reposiciona seta
    if cell[1] == 'r':
        t.setpos(x + size, y)
    elif cell[1] == 'l':
        t.setpos(x - size, y)
    elif cell[1] == 'u':
        t.setpos(x, y + size)
    elif cell[1] == 'd':
        t.setpos(x, y - size)

def draw_path(t, path, size=25):
    draw_start_cell(t, path[0], size)
    for i in range(len(path)-1):
        draw_cell(t, path[i:i+2], size)
    draw_end_cell(t, path[-1], size)

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
