class CarDespawner:
    def __init__(self):
        pass

    def set_in_lane(self, direction, lane):
        # don't care
        pass

    def can_enter(self):
        # car can always enter
        return True

    def enter(self, prev_node, car):
        # simply despawn the car
        # TODO maybe report on stats later
        return True