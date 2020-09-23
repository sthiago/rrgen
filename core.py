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

    def __str__(self):
        return f'Grid[{self.width}x{self.height}]'

    def get_size(self):
        return self.height * self.width

    def add_edge(self, edge):
        assert type(edge) == Edge
        assert not edge.src.is_out_of_bounds(self)
        assert not edge.dst.is_out_of_bounds(self)

        self.edges.add(edge)


class Path:
    """Represents a path in a 2-D Grid."""

    def __init__(self, grid, start=Node(0, 0)):
        assert type(grid) == Grid
        assert type(start) == Node

        self.grid = grid
        self.start = start
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
        assert not edge.src.is_out_of_bounds(self.grid)
        assert not edge.dst.is_out_of_bounds(self.grid)

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

    def build_path_method1(self, tolerance=0.0):
        """Build path randomly with backbiting

        tolerance = max. percentage of holes accepted"""
        assert type(tolerance) == float
        assert 0.0 <= tolerance <= 1.0

        while len(self.visited) < (1.0-tolerance) * self.grid.get_size():
            candidate = self.pick_next_node()
            if candidate:
                last_node = self.get_last_node()
                self.add_edge(Edge(last_node, candidate))
            else:
                self.backbite()

    def is_along_border(self, node):
        assert type(node) == Node

        last_node = self.get_last_node()
        diff = node - last_node
        assert diff.x != 0 or diff.y != 0

        # Horizontal neighbor: check the upper and lower nodes
        if diff.x != 0:
            upper = Node(node.x, node.y+1)
            lower = Node(node.x, node.y-1)
            return upper.is_out_of_bounds(self.grid) or upper in self.visited \
                or lower.is_out_of_bounds(self.grid) or lower in self.visited

        # Vertical neighbor: check the right and left nodes
        elif diff.y != 0:
            left = Node(node.x-1, node.y)
            right = Node(node.x+1, node.y)
            return left.is_out_of_bounds(self.grid) or left in self.visited \
                or right.is_out_of_bounds(self.grid) or right in self.visited

    def build_path_method2(self):
        last_node = self.start

        while True:
            # If there are no non-visited neighbors, the path is done
            neighbors = last_node.get_neighbors(self.grid)
            non_visited_neighbors = [ n for n in neighbors if n not in self.visited ]
            if len(non_visited_neighbors) == 0:
                break

            # Only consider neighbors that are along an edge
            candidates = []
            for neighbor in non_visited_neighbors:
                if self.is_along_border(neighbor):
                    candidates.append(neighbor)

            choice = random.choice(candidates)
            self.add_edge(Edge(last_node, choice))
            last_node = choice

        # Apply backbite 20 times per cell in the grid to randomize the path
        for i in range(20 * self.grid.get_size()):
            self.backbite()
