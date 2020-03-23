from data.res import information, list_of_under_mobs_objects


class Square:
    def __init__(self, kind):
        self.points_to_go, self.look = information[kind]
        self.kind = kind

    def __str__(self):
        return self.kind

    def __eq__(self, other):
        return self.kind == other.kind

    def can_place_npc_here(self):
        return self.kind in list_of_under_mobs_objects
