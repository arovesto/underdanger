import random

from data.res import list_of_under_mobs_objects, bioms, bioms_choice
from src.geometry.square import Square
from src.geometry.geometry import add, distance
from src.geometry.direction import DIRS
from src.geometry.board_figures import starting_area, exit_area


def make_random_figure(biom):
    p = (0, 0)
    construction = {}
    for _ in range(biom[0]):
        construction[p] = Square(random.choice(biom[1]))
        p = random.choice(list(DIRS.values())).go(p)
    return construction


def create_board(lines):
    shape = (len(lines), len(lines[0]))
    g = BoardGenerator(shape)
    g.add_figure((0, 0), create_figure(lines))
    return g.create_board()


def create_figure(lines):
    codes = {'.': 'floor', '#': 'wall', '$': 'brick', '*': 'fence',
             '+': 'door', '&': 'grass', '~': 'water', 'e': 'exit', ',': 'slab'}
    skip = ' '
    squares = {(x, y): Square(codes[c])
               for x, line in enumerate(lines)
               for y, c in enumerate(line) if c != skip}
    return squares


def reflect_y(figure):
    dx = max(x for (x, _) in figure)
    return {(x - dx, y): square for (x, y), square in figure.items()}


def rotate(figure):
    return {(y, -x): square for (x, y), square in reflect_y(figure).items()}


def random_orientation(figure):
    fig = figure
    for _ in range(random.randrange(0, 4)): fig = rotate(fig)
    return fig


def generate_game_board(shape):
    start_position = (random.randrange(5, shape[0] - 5), random.randrange(5, shape[1] - 5))
    exit_position = (random.randrange(3, shape[0] - 3), random.randrange(3, shape[1] - 3))
    if distance(start_position, exit_position) < shape[0] / 3:
        return generate_game_board(shape)
    g = BoardGenerator(shape)
    g.add_figure(add((-5, -5), start_position), random_orientation(create_figure(starting_area)))
    g.add_figure(add((-1, -1), exit_position), random_orientation(create_figure(exit_area)))
    return g.generate(), start_position, [exit_position]


def generate_game_board_improved(shape, start_position, exit_position, altitude_overfall=10, water_level=1):
    g = BoardGenerator(shape)
    g.add_surface()  # Все клетки заполняются чем-либо
    g.add_altitude(altitude_overfall)  # Создаются холмы и ямы, в пределах перепада высот
    g.add_water(water_level)  # Все точки с заданной высотой заполняются водой + с холм текут реки
    g.add_figure(add((-5, -5), start_position), create_figure(starting_area))
    g.add_figure(add((-1, -1), exit_position), create_figure(exit_area))
    g.add_village()  # На ровных местах создаются деревни
    return g.generate()  # Простая функция, почти без ничего


class Rectangle:
    def __init__(self, shape):
        self.shape = shape
        self.area = shape[0] * shape[1]

    def is_inside(self, position):
        return all(x in range(self.shape[i]) for i, x in enumerate(position))

    def random_position(self):
        return tuple(random.randrange(x) for x in self.shape)

    def neighbours(self, position):
        x, y = position
        return [(i, j) for i in range(x - 1, x + 2)
                for j in range(y - 1, y + 2)
                if [i, j] != [x, y] and self.is_inside((i, j))]


class Board(Rectangle):
    def __init__(self, shape, squares):
        super().__init__(shape)
        self.squares = squares


    def square(self, position):
        return self.squares[position]


class BoardGenerator(Rectangle):
    def __init__(self, shape):
        super().__init__(shape)
        self.squares = {}

    def create_board(self):
        return Board(self.shape, self.squares)

    def generate(self, bioms_dencity=0.5, bioms_size=20):
        bioms_count = int(bioms_dencity * self.area / bioms_size)
        for _ in range(bioms_count):
            biom = make_random_figure(bioms[random.choice(bioms_choice)])
            self.add_figure(self.random_position(), biom)

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if not (i, j) in self.squares:
                    self.squares[(i, j)] = Square(random.choice(list_of_under_mobs_objects))
        return self.create_board()

    def add_figure(self, origin, figure, override=False):
        for position, square in figure.items():
            p = add(position, origin)
            if self.is_inside(p) and (not p in self.squares or override):
                self.squares[p] = square
