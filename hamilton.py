import sys
import turtle
import random

from draw import draw_path, create_turle, reset_turtle, draw_bounding_box

class Node:
    """Represents a node in 2-D Grid. """

    def __init__(self, x, y):
        assert type(x) == int
        assert type(y) == int

        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        assert type(other) == Node
        return Node(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert type(other) == Node
        return Node(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        assert type(other) == Node
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def is_out_of_bounds(self, grid):
        assert type(grid) == Grid
        return not ((0 <= self.x < grid.width) and (0 <= self.y < grid.height))

    def get_neighbors(self, grid):
        assert type(grid) == Grid
        neighbors = []
        for direction in [Node(1, 0), Node(0, 1), Node(-1, 0), Node(0, -1)]:
            neighbor = self + direction
            if not neighbor.is_out_of_bounds(grid):
                neighbors.append(neighbor)
        return neighbors

    def get_edges_to_neighbors(self, grid):
        assert type(grid) == Grid
        neighbors = self.get_neighbors(grid)
        edges = []
        for n in neighbors:
            edges.append(Edge(self, n))
            edges.append(Edge(n, self))
        return edges


class Edge:
    """Represents an edge in a 2-D grid graph."""

    def __init__(self, src, dst):
        assert type(src) == Node
        assert type(dst) == Node
        assert src != dst

        self.src = src
        self.dst = dst

    def __str__(self):
        return f'{self.src} -> {self.dst}'

    def __eq__(self, other):
        return (self.src, self.dst) == (other.src, other.dst)

    def __hash__(self):
        return hash((self.src, self.dst))

    def get_letter_repr(self):
        direction = self.dst - self.src
        translation = {
            Node(1, 0)  : 'r',
            Node(0, 1)  : 'u',
            Node(-1, 0) : 'l',
            Node(0, -1) : 'd',
        }
        return translation.get(direction, '?')


    def reverse(self):
        self.src, self.dst = self.dst, self.src

class Grid:
    """A graph that represents a 2-D grid."""

    def __init__(self, width, height):
        assert type(width) == int
        assert type(height) == int

        self.width = width
        self.height = height
        # self.nodes = set()
        self.edges = set()

    def __str__(self):
        # nodes = ', '.join([ str(n) for n in self.nodes ])
        edges = ', '.join([ str(e) for e in self.edges ])
        return f'Grid({self.width}x{self.height})[{edges}]'

    # def add_node(self, node):
    #     assert type(node) == Node
    #     self.nodes.add(node)

    def get_size(self):
        return self.height * self.width

    def add_edge(self, edge):
        assert type(edge) == Edge
        assert not edge.src.is_out_of_bounds(self)
        assert not edge.dst.is_out_of_bounds(self)

        self.edges.add(edge)

    def remove_edge(self, edge):
        assert type(edge) == Edge
        self.edges.remove(edge)

    def populate_edges(self):
        for i in range(self.width):
            for j in range(self.height):
                node = Node(i, j)
                for edge in node.get_edges_to_neighbors(grid):
                    self.add_edge(edge)


class Path:
    """Represents a path in a 2-D Grid."""

    def __init__(self, grid, start=Node(0, 0), tolerance=0):
        assert type(grid) == Grid
        assert type(start) == Node

        self.grid = grid
        self.start = start
        self.tolerance = tolerance
        self.edges = []
        self.visited = [start]

    def get_extended_str(self):
        edges = ', '.join([ str(e) for e in self.edges ])
        return f'Path[{edges}]'

    def __str__(self):
        edges = ''.join([ e.get_letter_repr() for e in self.edges ])
        return f'{edges}'

    def add_edge(self, edge):
        assert type(edge) == Edge
        assert edge in self.grid.edges

        if len(self.edges) == 0:
            assert edge.src == self.start
        else:
            assert edge.src == self.edges[-1].dst

        self.visited.append(edge.dst)
        self.edges.append(edge)

    def get_last_node(self):
        if len(self.edges) == 0:
            return self.start
        return self.edges[-1].dst

    def pick_next_node(self):
        current_node = self.get_last_node()
        candidates = current_node.get_neighbors(self.grid)
        candidates = [c for c in candidates if c not in self.visited]
        if len(candidates) == 0:
            return None
        return random.choice(candidates)

    def backbite(self):
        # Pick a neighbor that is not the src of the last edge as pivot
        last_edge = self.edges[-1]
        last_node = last_edge.dst
        neighbors = last_node.get_neighbors(self.grid)
        neighbors.remove(last_edge.src)

        # I don't think this is necessary -- have to confirm, tho
        # if self.start in neighbors:
        #     neighbors.remove(self.start)

        assert len(neighbors) > 0
        pivot = random.choice(neighbors)

        # Create an edge from the pivot to the last node
        new_edge = Edge(pivot, last_node)

        # Find the edge of the path that starts at the pivot
        for i in range(len(self.edges)):
            if self.edges[i].src == pivot:
                pivot_index = i
                break

        # Split the path into two. The second part starts after the pivot
        first_part = self.edges[:pivot_index]
        second_part = self.edges[pivot_index+1:]

        # Replace the edge that starts at the pivot with the new edge
        first_part.append(new_edge)

        # Invert the order and direction of the second part
        for edge in second_part:
            edge.reverse()
        second_part.reverse()

        # Finally, put it all as the path
        self.edges = first_part + second_part

    def build_path_method1(self):
        while len(self.visited) < self.grid.get_size():
            candidate = self.pick_next_node()
            if candidate:
                last_node = self.get_last_node()
                self.add_edge(Edge(last_node, candidate))
            elif len(self.visited) < (1-self.tolerance) * self.grid.get_size():
                self.backbite()
            else:
                break



            # global t
            # global cell_size
            # t.reset()
            # t.speed('fastest')
            # t.penup()
            # t.setposition(0, 0)
            # draw_bounding_box(t, cell_size, self.grid.height, self.grid.width)
            # draw_path(t, str(self), cell_size)
            # turtle.update()
        print(len(self.visited), self.grid.get_size())


if __name__ == "__main__":
    # node1 = Node(3, 4)
    # node2 = Node(3, 4)
    # node3 = Node(5, 5)

    # print(node1)
    # print(node2)
    # print(node3)
    # print(node1 == node2)
    # print(node1 == node3)
    # print(node2 == node3)
    # print(node2 + node3)
    # print(node2 - node3)
    # print(node2)
    # print(node3)

    # grid = Grid(6, 6)
    # print(grid)

    # edge = Edge(node1, node3)

    # grid.add_edge(edge)
    # print(grid)
    # grid.remove_edge(edge)
    # print(grid)

    # grid = Grid(3, 3)
    # grid.populate_edges()
    # print(grid)
    # print(len(grid.edges))

    # path = Path(grid, Node(0, 0))
    # path.add_edge(Edge(Node(0, 0), Node(1, 0)))
    # path.add_edge(Edge(Node(1, 0), Node(2, 0)))
    # path.add_edge(Edge(Node(2, 0), Node(2, 1)))
    # print(path)
    # print(path.get_extended_str())

    cell_size = 25 # Cell size in pixels
    wall_thickness = 1 # Wall thickness in pixels. ?? fixme
    map_width = 40 # Map width in cells
    map_height = 20 # Map height in cells
    # num_holes = int(0.2 * map_height * map_width) # Maximum number of holes allowed

    grid = Grid(map_width, map_height)
    grid.populate_edges()

    t = create_turle(cell_size, wall_thickness, map_width, map_height)
    while True:
        seed = random.randrange(sys.maxsize)
        # seed = 2361718422405573934
        random.seed(seed)
        print("Seed:", seed)

        # length = map_height * map_width
        path = Path(grid)
        path.build_path_method1()
        path_str = str(path)
        print("Path:", path_str)

        reset_turtle(t, wall_thickness)
        draw_bounding_box(t, cell_size, map_height, map_width)
        draw_path(t, path_str, cell_size)

        turtle.update()

        # break

    t.hideturtle()
    turtle.exitonclick()
