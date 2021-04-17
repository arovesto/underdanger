from data.res import square_types, list_of_under_mobs_objects


class Square:
    def __init__(self, square_type):
        square_info = square_types[square_type]
        self.kind = square_type
        self.points_to_go = square_info['move_cost']
        self.look = square_info['appearance']
        self.description = square_info['description']
        self.style = square_info['html_style']

    def __str__(self):
        return self.kind

    def __eq__(self, other):
        return self.kind == other.kind

    def can_place_npc_here(self):
        return self.kind in list_of_under_mobs_objects