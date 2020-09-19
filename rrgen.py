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

# Start generation
grid = Grid(args.width, args.height)
drawer = Drawer(grid, args.cell_size, args.wall_thickness, args.padding,
    args.hide_arrows, args.hide_start, args.hide_finish, args.hide_github)

# Check image dimensions
if drawer.img_width > 32512 or drawer.img_height > 32600:
    parser.error(
        'The generated map would exceed the maximum dimensions: 32512x32600')

# Warning on big maps
if not args.ignore_warning and args.width > 45 and args.height > 45:
    print('WARNING: A huge map is about to be generated! Because of the way '
        'generation is implemented at the moment, the time to create the path '
        'skyrockets really fast. A 50x50 map takes about 3 minutes to generate '
        'on a 2010-ish i3 M350. And I gave up when I tried to generate an '
        '80x80 map. Also, take into account that a 50x50 map could take around '
        '30 minutes to finish playing alone.')
    answer = query_yes_no('Continue anyway?')
    if answer == False:
        exit()

drawer.init_image_array()
path = Path(grid, start=start_position)
path.build_path_method1()

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
