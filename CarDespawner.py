class CarDespawner:
    def __init__(self):
        pass

    def set_in_lane(self, direction, lane):
        # don't care
        pass

    def enter(self, prev_node, car):
        # simply despawn the car
        # TODO maybe report on stats later
        return True

    def update(self):
        # do nothing
        pass