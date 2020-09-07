import random

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
        if direction == Node(1, 0):
            return 'r'
        elif direction == Node(0, 1):
            return 'u'
        elif direction == Node(-1, 0):
            return 'l'
        elif direction == Node(0, -1):
            return 'd'
        return '?'


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

    def __init__(self, grid, start):
        assert type(grid) == Grid
        assert type(start) == Node

        self.grid = grid
        self.start = start
        self.edges = []

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

        self.edges.append(edge)


if __name__ == "__main__":
    node1 = Node(3, 4)
    node2 = Node(3, 4)
    node3 = Node(5, 5)

    print(node1)
    print(node2)
    print(node3)
    print(node1 == node2)
    print(node1 == node3)
    print(node2 == node3)
    print(node2 + node3)
    print(node2 - node3)
    print(node2)
    print(node3)

    grid = Grid(6, 6)
    print(grid)

    edge = Edge(node1, node3)

    grid.add_edge(edge)
    print(grid)
    grid.remove_edge(edge)
    print(grid)

    grid = Grid(3, 3)
    grid.populate_edges()
    print(grid)
    print(len(grid.edges))

    path = Path(grid, Node(0, 0))
    path.add_edge(Edge(Node(0, 0), Node(1, 0)))
    path.add_edge(Edge(Node(1, 0), Node(2, 0)))
    path.add_edge(Edge(Node(2, 0), Node(2, 1)))
    print(path)
    print(path.get_extended_str())
