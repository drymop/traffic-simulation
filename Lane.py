"""Directional edge connecting 2 nodes in traffic network"""
class Lane:
    def __init__(self, length, prev_node, out_direction, next_node, in_direction):
        self.length = length
        self.prev_node = prev_node
        self.next_node = next_node
        # connect the 2 nodes
        prev_node.set_out_lane(out_direction, self)
        next_node.set_in_lane(in_direction, self)
        # keep track of cars on the lane
        self.cars = [None] * length
        self.n_cars = 0

    def enter(self, car):
        if not self.cars[-1] is None:
            return False
        self.cars[-1] = car
        self.n_cars += 1
        return True

    def update(self):
        # if there is a car at the "end" of the lane,
        # forward to the next traffic node if possible
        if self.cars[0] and self.next_node.enter(self.prev_node, self.cars[0]):
            self.cars[0] = None
            self.n_cars -= 1
        # move each car forward if possible
        for i in range(1, len(self.cars)):
            if not self.cars[i-1]:
                self.cars[i-1], self.cars[i] = self.cars[i], None

    def __str__(self):
        cells = []
        for car in self.cars:
            if car:
                s = "%4d" % car.car_id
            else:
                s = "    "
            cells.append(s)
        return " | ".join(cells)