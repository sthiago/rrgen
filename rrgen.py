import sys
import png
import random

from colors import Colors
from core import Grid, Path
from draw import Drawer

cell_size = 200
wall_thickness = 5
map_width = 30
map_height = 20

grid = Grid(map_width, map_height)
drawer = Drawer(grid, cell_size, wall_thickness, 32)

seed = random.randrange(sys.maxsize)
random.seed(seed)
print("Seed:", seed)

path = Path(grid)
path.build_path_method1()
path_str = str(path)
print("Path:", path_str)

drawer.draw_path(path, 1)

img = drawer.img
img.reverse()

palette = [ (0, 0, 0, 255), Colors.blue.value, Colors.red.value ]
w = png.Writer(len(img[0]), len(img), palette=palette, bitdepth=8)
f1 = open('png.png', 'wb')
f2 = open('/home/sthiago/SteamWA/User/SavedLevels/png.png', 'wb')
w.write(f1, img)
w.write(f2, img)
