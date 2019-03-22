class Direction:
    def __init__(self, delta):
        self.delta = delta

    def __cmp__(self, other):
        return self.delta == other.delta

    def go(self, point, multiply=1):
        return tuple(p + d * multiply for p, d in zip(point, self.delta))



UP    = Direction((-1,  0))
DOWN  = Direction(( 1,  0))
LEFT  = Direction(( 0, -1))
RIGHT = Direction(( 0,  1))

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

DIRS = {
    'up'   : UP,
    'down' : DOWN,
    'left' : LEFT,
    'right': RIGHT,
}
