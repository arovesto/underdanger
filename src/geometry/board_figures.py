import random

from src.geometry.direction import DIRS


def make_random_blub_(material, blub_square):
    p = (0, 0)
    construction = []
    for i in range(blub_square):
        construction.append((material, p))
        p = random.choice(list(DIRS.values())).go(p)
    return construction


starting_area = [
    ",,,,,,,,,,,",
    ",*********,",
    ",*,,,,,,,*,",
    ",*,$$$$$,*,",
    ",*,$,,,$,*,",
    ",*,$,,,+,,,",
    ",*,$,,,$,*,",
    ",*,$$$$$,*,",
    ",*,,,,,,,*,",
    ",*********,",
    ",,,,,,,,,,,",
]

exit_area = [
    "     ",
    " $$$ ",
    " $e$ ",
    " $,$ ",
    "  ,  "
]

village = []
