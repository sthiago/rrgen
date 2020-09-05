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

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def is_out_of_bounds(self, grid):
        assert type(grid) == Grid
        return not ((0 <= self.x < grid.width) and (0 <= self.y < grid.height))

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

class Path:
    """Represents a path in a 2-D grid."""
    
    def __init__(self, grid):
        assert type(grid) == Grid
        self.grid = grid
        self.edges = []

    def get_extended_str(self):
        edges = ', '.join([ str(e) for e in self.edges ])
        return f'Path[{edges}]'

    def __str__(self):
        return f'Path[]'

    def add_edge(self, edge):
        assert type(edge) == Edge'
        assert edge in self.grid.edges
        

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

    grid = Grid(3, 4)
    print(grid)

    edge = Edge(node1, node3)

    grid.add_edge(edge)
    print(grid)
    grid.remove_edge(edge)
    print(grid)
