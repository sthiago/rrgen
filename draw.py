import turtle

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

    # reposition turtle
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

def draw_bounding_box(t, cell_size, map_height, map_width, padding=2):
    """Draw the box that bounds tha map.
    padding -- spacing between the bbox and the actual map"""
    t.pu()
    t.setposition(-padding, -padding)
    t.setheading(0)
    t.pencolor('red')

    t.pd()
    t.fd(padding*2 + map_width*cell_size)
    t.lt(90)
    t.fd(padding*2 + map_height*cell_size)
    t.lt(90)
    t.fd(padding*2 + map_width*cell_size)
    t.lt(90)
    t.fd(padding*2 + map_height*cell_size)
    t.lt(90)
    t.pu()

    t.setposition(0, 0)
    t.pencolor('black')

def create_turle(cell_size, wall_thickness, map_width, map_height):
    t = turtle.Turtle()
    s = t.getscreen()
    s.setup(width=int(500 * map_height / map_width), height=500)
    s.setworldcoordinates(-2, -2, map_width * cell_size + 4, map_height * cell_size + 4)
    turtle.tracer(0, 0)
    t.speed('fastest')
    t.pensize(wall_thickness)
    t.penup()
    reset_turtle(t, wall_thickness)
    return t

def reset_turtle(t, wall_thickness):
    t.reset()
    t.speed('fastest')
    t.pensize(wall_thickness)
    t.penup()
    t.setposition(0, 0)
    turtle.update()
    return t
