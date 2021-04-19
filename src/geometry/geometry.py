import math
import itertools


def distance(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in [0, 1]))


def add(a, b):
    return tuple(a[i] + b[i] for i in [0, 1])


def sub(a, b):
    return tuple(a[i] - b[i] for i in [0, 1])


def manhattan(a, b):
    return sum(abs(a[i] - b[i]) for i in [0, 1])


def in_square(test_position, center_position, radius):
    return all(abs(center_position[i] - test_position[i]) <= radius for i in [0, 1])


def square(position, radius):
    return [add((i, j), position) for i in range(-radius, radius + 1) for j in range(-radius, radius + 1)]


def circle(position, radius):
    return set(filter(lambda x: distance(x, position) <= radius, square(position, radius)))


def ring(position, inner, outer):
    return set(filter(lambda x: inner <= distance(x, position) <= outer, square(position, outer)))


def merge(shapes):
    return set(itertools.chain.from_iterable(shapes))
