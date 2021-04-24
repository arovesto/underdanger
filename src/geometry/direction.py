class Direction:
    def __init__(self, delta):
        self.delta = delta

    def __cmp__(self, other):
        return self.delta == other.delta

    def go(self, point, multiply=1):
        return tuple(p + d * multiply for p, d in zip(point, self.delta))


UP = Direction((-1, 0))
DOWN = Direction((1, 0))
LEFT = Direction((0, -1))
RIGHT = Direction((0, 1))


def anti_dir(direction):
    if direction == UP:
        return DOWN
    if direction == LEFT:
        return RIGHT
    if direction == RIGHT:
        return LEFT
    if direction == DOWN:
        return UP


def perpendicular(direction):
    if direction == UP or direction == DOWN:
        return LEFT, RIGHT
    return UP, DOWN


def where_to_go(delta):
    result = []
    if delta[0] > 0:
        result.append('юг')
    elif delta[0] < 0:
        result.append('север')

    if delta[1] > 0:
        result.append('восток')
    elif delta[1] < 0:
        result.append('запад')
    if len(result) == 2:
        result[0] += 'о'
    return "-".join(result)


def directions_on(fr, to):
    dt = (to[0] - fr[0], to[1] - fr[1])
    dirs = []
    if dt[0] > 0:
        dirs.append("down")
    elif dt[0] < 0:
        dirs.append("up")

    if dt[1] > 0:
        dirs.append("right")
    elif dt[1] < 0:
        dirs.append("left")

    return list(reversed(sorted(dirs, key=lambda x: abs(dt[dirs.index(x)]))))


DIRS = {
    'up': UP,
    'down': DOWN,
    'left': LEFT,
    'right': RIGHT,
}
