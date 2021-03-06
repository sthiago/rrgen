#!/usr/bin/env python3

import os
import sys
import png
import random

from cli import parser, query_yes_no
from colors import Colors
from core import Grid, Path, Node
from draw import Drawer

args = parser.parse_args()

# Show available colors
if args.colors:
    longest = max(list(Colors), key=lambda c: len(c.name))
    padding = len(longest.name) + 1
    print('Available colors:')
    for color in list(Colors):
        print(color.name.rjust(padding), color.value)
    exit(0)

# Configure map color
if args.color:
    try:
        color = Colors[args.color]
    except KeyError:
        parser.error(f'Color \'{args.color}\' doesn\'t exist. '
            'Try --colors to see all the available colors.')
else:
    color = random.choice(list(Colors))

# Prevent method 2 with start_at
if args.method == 2 and args.start_at is not None:
    parser.error('Method 2 can\'t be used with --start-at')

# Prevents too high of a tolerance (that would result in an empty map)
if args.method == 1 and (1.0-args.tolerance) * args.width * args.height < 1:
    parser.error('Tolerance is too high. An empty map would be generated.')

# Configure start position
if args.start_at is None:
    start_options = {
        'bottom_left' : Node(0, 0),
        'bottom_right' : Node(args.width-1, 0),
        'top_left' : Node(0, args.height-1),
        'top_right' : Node(args.width-1, args.height-1),
    }
    start_position = start_options[args.start]
else:
    x, y = args.start_at[0], args.start_at[1]
    if not 0 <= x < args.width or not 0 <= y < args.height:
        parser.error('Start position values for X and Y must be within '
        'boundaries: 0 <= X < WIDTH and 0 <= Y < HEIGHT')
    start_position = Node(x, y)

# Configure random seed
if args.seed is None:
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
else:
    seed = args.seed
    random.seed(seed)

if args.show_seed:
    print("Seed:", seed)

# Start of path generation and drawing
if args.path:
    path = Path.from_string(args.path)
    grid = path.grid
else:
    grid = Grid(args.width, args.height)

drawer = Drawer(grid, args.cell_size, args.wall_thickness, args.padding,
    args.hide_arrows, args.hide_start, args.hide_finish, args.hide_github)

# Check image dimensions
if drawer.img_width > 32512 or drawer.img_height > 32600:
    parser.error(
        'The generated map would exceed the maximum dimensions: 32512x32600')

# Warning on big maps
if not args.path and not args.ignore_warning \
    and args.width > 40 and args.height > 40:
    print('WARNING: A huge map is about to be generated! Because of the way '
        'map generation is implemented, the time to create the path grows '
        'really fast. Maps bigger than 40x40 can take several minutes to '
        'generate. Also, take into account that a 50x50 map could take '
        '30 minutes to finish playing with 1 player. You can suppress this '
        'warning with --ignore-warning.')
    answer = query_yes_no('Continue anyway?')
    if answer == False:
        exit()

drawer.init_image_array()

if not args.path:
    path = Path(grid, start=start_position)
    if args.method == 1:
        path.build_path_method1(args.tolerance)
    elif args.method == 2:
        path.build_path_method2()

if args.show_path:
    path_str = str(path)
    print("Path:", path_str)

# Draw image to file
drawer.draw_path(path, 1)
img = drawer.img
img.reverse()
palette = [ (0, 0, 0, 255), color.value ]
w = png.Writer(len(img[0]), len(img), palette=palette, bitdepth=8)

filename = os.path.expanduser(args.output)
if os.path.isdir(filename):
    filename += 'rrgen.png'
if not filename.endswith('.png'):
    filename += '.png'

f = open(filename, 'wb')
w.write(f, img)
print(f'Created file {filename}')
