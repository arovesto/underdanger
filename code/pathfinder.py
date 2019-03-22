from geometry import distance
from direction import DIRS

class Node:
    def __init__(self, position, cost):
        self.position = position
        self.cost = cost
        self.previous = None
        self.value = 1000

class StartNode:
    def __init__(self, position, cost):
        self.position = position
        self.cost = cost
        self.previous = None
        self.value = 0
        
        
def path(entity, positions, max_deph = 15):
    start_position = entity.position
    possible = [StartNode(start_position, entity.world.board.squares[start_position].points_to_go)]
    explored = []
    for _ in range(max_deph):
        square = best_point(possible, positions)
        if len(possible) == 0: break
        if square == 0: break
        if any(distance(square.position, p) == 0 for p in positions):
            return build_path(entity, square)
        else:
            explored.append(square.position)
            possible = update_possible(square, possible, explored, entity)
    return []
    
def build_path(entity, square):
    path = []
    while square.previous is not None:
        path.append(square.position)
        square = square.previous
    return list(reversed(path))

def best_point(possible, positions):
    return min(possible, key = lambda x: min(x.cost + distance(p, x.position) for p in positions), default = 0)

def update_possible(square, possible, explored, entity):
    possible.remove(square)
    for direction in DIRS.values():
        if (entity.world.can_move(entity, direction.go(square.position))
            and direction.go(square.position) not in explored
            and distance(entity.position, direction.go(square.position)) <= entity.see):
                s = Node(direction.go(square.position), entity.world.board.squares[square.position].points_to_go)
                if square.value + s.cost < s.value:
                    s.value = square.value + s.cost
                    s.previous = square
                possible.append(s)
    return possible            
        