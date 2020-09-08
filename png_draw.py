import sys
import png
import random

from hamilton import Grid, Edge, Node, Path

class Drawer:
    def __init__(self, grid, cell_size, wall_thickness, padding):
        assert type(grid) == Grid
        assert type(cell_size) == int
        assert type(wall_thickness) == int
        assert type(padding) == int
        assert wall_thickness >= 1

        self.grid = grid
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        self.padding = padding

        self.img_width, self.img_height = self.get_image_dimensions()
        assert self.img_width >= 640
        assert self.img_height >= 32
        self.img = [[0] * self.img_width for _ in range(self.img_height)]

    def get_image_dimensions(self):
        # Find the minimum required width and height
        needed_width = self.cell_size * self.grid.width + self.wall_thickness + 2 * self.padding
        needed_height = self.cell_size * self.grid.height + self.wall_thickness + 2 * self.padding

        # They need to be multiples of 8
        width = 8 * ((needed_width + 8 - 1) // 8)
        height = 8 * ((needed_height + 8 - 1) // 8)

        return (width, height)

    def draw_line(self, start, length, direction, color):
        assert type(start) == tuple
        assert type(length) == int
        assert type(color) == int
        assert direction in ['horizontal', 'vertical']
        assert 0 <= color < 64

        x, y = start
        if direction == 'horizontal':
            for i in range(x, x + length):
                for j in range(y, y + self.wall_thickness):
                    self.img[j][i] = color
        elif direction == 'vertical':
            for i in range(x, x + self.wall_thickness):
                for j in range(y, y + length):
                    self.img[j][i] = color

    def draw_left_wall(self, node, color):
        assert type(node) == Node
        assert type(color) == int
        assert 0 <= color < 64

        start = (
            self.padding + node.x * self.cell_size,
            self.padding + node.y * self.cell_size,
        )
        self.draw_line(start, self.cell_size, 'vertical', color)

    def draw_right_wall(self, node, color):
        assert type(node) == Node
        assert type(color) == int
        assert 0 <= color < 64

        start = (
            self.padding + (node.x + 1) * self.cell_size,
            self.padding + node.y * self.cell_size,
        )
        self.draw_line(start, self.cell_size, 'vertical', color)

    def draw_bottom_wall(self, node, color):
        assert type(node) == Node
        assert type(color) == int
        assert 0 <= color < 64

        start = (
            self.padding + node.x * self.cell_size,
            self.padding + node.y * self.cell_size,
        )
        self.draw_line(start, self.cell_size, 'horizontal', color)

    def draw_top_wall(self, node, color):
        assert type(node) == Node
        assert type(color) == int
        assert 0 <= color < 64

        start = (
            self.padding + node.x * self.cell_size,
            self.padding + (node.y + 1) * self.cell_size,
        )
        self.draw_line(start, self.cell_size + self.wall_thickness, 'horizontal', color)

    def draw_start_cell(self, start_node, move, color):
        assert type(start_node) == Node
        assert type(move) == str
        assert move in list('lrud')

        if move == 'r':
            self.draw_left_wall(start_node, color)
            self.draw_top_wall(start_node, color)
            self.draw_bottom_wall(start_node, color)
        elif move == 'l':
            self.draw_right_wall(start_node, color)
            self.draw_top_wall(start_node, color)
            self.draw_bottom_wall(start_node, color)
        elif move == 'u':
            self.draw_left_wall(start_node, color)
            self.draw_right_wall(start_node, color)
            self.draw_bottom_wall(start_node, color)
        elif move == 'd':
            self.draw_left_wall(start_node, color)
            self.draw_right_wall(start_node, color)
            self.draw_top_wall(start_node, color)

    def draw_end_cell(self, end_node, move, color):
        assert type(end_node) == Node
        assert type(move) == str
        assert move in list('lrud')

        if move == 'r':
            self.draw_right_wall(end_node, color)
            self.draw_top_wall(end_node, color)
            self.draw_bottom_wall(end_node, color)
        elif move == 'l':
            self.draw_left_wall(end_node, color)
            self.draw_top_wall(end_node, color)
            self.draw_bottom_wall(end_node, color)
        elif move == 'u':
            self.draw_left_wall(end_node, color)
            self.draw_right_wall(end_node, color)
            self.draw_top_wall(end_node, color)
        elif move == 'd':
            self.draw_left_wall(end_node, color)
            self.draw_right_wall(end_node, color)
            self.draw_bottom_wall(end_node, color)

    def draw_cell(self, node, move, color):
        assert type(node) == Node
        assert type(move) == str

        if move == 'rr' or move == 'll':
            self.draw_top_wall(node, color)
            self.draw_bottom_wall(node, color)
        elif move in ['rl', 'lr', 'ud', 'du']:
            pass
        elif move == 'rd':
            self.draw_top_wall(node, color)
            self.draw_right_wall(node, color)
        elif move == 'ru':
            self.draw_bottom_wall(node, color)
            self.draw_right_wall(node, color)
        elif move == 'ld':
            self.draw_top_wall(node, color)
            self.draw_left_wall(node, color)
        elif move == 'lu':
            self.draw_bottom_wall(node, color)
            self.draw_left_wall(node, color)
        elif move == 'dr':
            self.draw_bottom_wall(node, color)
            self.draw_left_wall(node, color)
        elif move == 'dl':
            self.draw_right_wall(node, color)
            self.draw_bottom_wall(node, color)
        elif move == 'dd' or move == 'uu':
            self.draw_right_wall(node, color)
            self.draw_left_wall(node, color)
        elif move == 'ur':
            self.draw_top_wall(node, color)
            self.draw_left_wall(node, color)
        elif move == 'ul':
            self.draw_top_wall(node, color)
            self.draw_right_wall(node, color)

    def draw_path(self, path, color):
        assert type(path) == Path

        path_str = str(path)
        start_node = path.edges[0].src
        self.draw_start_cell(start_node, path_str[0], color)
        for i in range(len(path_str)-1):
            node = path.edges[i].dst
            self.draw_cell(node, path_str[i:i+2], color)
        node = path.edges[i+1].dst
        self.draw_end_cell(node, path_str[-1], color)

    def draw_all_walls(self, node, color):
        self.draw_left_wall(node, color)
        self.draw_right_wall(node, color)
        self.draw_top_wall(node, color)
        self.draw_bottom_wall(node, color)




# w, h = calculate_image_dimensions(Grid(33, 17), 50, 5)
# img = [[0] * w for _ in range(h)]

# for j in range(len(img)):
#     for i in range(len(img[j])):
#         if 100 <= i <= 500 and 100 <= j <= 150:
#             img[j][i] = 4

# draw_edge(Edge(Node(1, 1), Node(10, 1)))

cell_size = 19
wall_thickness = 1
map_width = 40
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


# drawer.draw_all_walls(Node(0, 0), 1)
# drawer.draw_all_walls(Node(1, 0), 1)
# drawer.draw_all_walls(Node(2, 0), 1)
# drawer.draw_all_walls(Node(0, 1), 1)
# drawer.draw_all_walls(Node(1, 1), 1)
# drawer.draw_all_walls(Node(2, 1), 1)
# drawer.draw_all_walls(Node(0, 2), 1)
# drawer.draw_all_walls(Node(1, 2), 1)
# drawer.draw_all_walls(Node(2, 2), 1)


img = drawer.img
img.reverse()

palette = [
    (0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
]
w = png.Writer(len(img[0]), len(img), palette=palette, bitdepth=8)
f1 = open('png.png', 'wb')
f2 = open('/home/sthiago/SteamWA/User/SavedLevels/png.png', 'wb')
w.write(f1, img)
w.write(f2, img)
