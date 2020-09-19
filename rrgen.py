import os
import sys
import png
import random

from cli import parser
from colors import Colors
from core import Grid, Path
from draw import Drawer

args = parser.parse_args()
print(args)

if args.colors:
    longest = max(list(Colors), key=lambda c: len(c.name))
    padding = len(longest.name) + 1
    print('Available colors:')
    for color in list(Colors):
        print(color.name.rjust(padding), color.value)
    exit(0)

if args.color:
    try:
        color = Colors[args.color]
    except KeyError:
        print(f'Error: color \'{args.color}\' doesn\'t exist. '
            'Try --colors to see all the available colors.')
        exit(1)
else:
    color = random.choice(list(Colors))

if args.seed is None:
    seed = random.randrange(sys.maxsize)
    random.seed(seed)
else:
    seed = args.seed
    random.seed(seed)

if args.show_seed:
    print("Seed:", seed)

grid = Grid(args.width, args.height)
drawer = Drawer(grid, args.cell_size, args.wall_thickness, args.padding,
    args.hide_arrows, args.hide_start, args.hide_finish, args.hide_github)

path = Path(grid)
path.build_path_method1()

if args.show_path:
    path_str = str(path)
    print("Path:", path_str)

drawer.draw_path(path, 1)
img = drawer.img
img.reverse()

palette = [ (0, 0, 0, 255), color.value ]
w = png.Writer(len(img[0]), len(img), palette=palette, bitdepth=8)
f = open(os.path.expanduser(args.output), 'wb')
w.write(f, img)
print(f'Created file {args.output}')
