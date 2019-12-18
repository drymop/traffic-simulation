"""Directional edge in traffic network"""
class Lane:
    def __init__(self, length, prev_node=None, next_node=None):
        self.next_node = next_node
        self.cars = [None] * length
        self.n_cars = 0

    def can_enter(self):
        return self.cars[-1] is None

    def enter(self, prev_node, car):
        if not self.cars[-1] is None:
            return False
        self.cars[-1] = car
        self.n_cars += 1
        return True

    def update(self):
        # if there is a car at the "end" of the lane,
        # forward to the next traffic node if possible
        if self.cars[0] and self.next_node.enter(self, self.cars[0]):
            self.cars[0] = None
            self.n_cars -= 1
        # move each car forward if possible
        for i in range(1, length(self.cars)):
            if not self.cars[i-1]:
                self.cars[i-1], self.cars[i] = self.cars[i], None