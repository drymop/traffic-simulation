"""Traffic node: a small, standard 4-way intersection"""
class Intersection:
    N_BRANCHES = 4
    CLEAR_TIMES = [1, 2, 1, 0]

    def __init__(self):
        # index is clock-wise
        self.in_lanes = [None] * Intersection.N_BRANCHES
        self.out_lanes = [None] * Intersection.N_BRANCHES
        self.car = None
        self.clear_time = -1
        self.next_node_ind = -1

    def can_enter(self):
        return self.car is None

    def enter(self, prev_node, car):
        if self.car is not None:
            return False
        self.car = car
        # find index of previous node
        for prev_node_ind in range(Intersection.N_BRANCHES):
            if prev_node == self.in_lanes[prev_node_ind].prev_node:
                break
        next_nodes = [lane.next_node for lane in self.out_lanes]
        next_node_ind = car.select_next_node(next_nodes)
        self.clear_time = Intersection.CLEAR_TIMES[(next_node_ind - prev_node_ind) % Intersection.N_BRANCHES]
        self.next_node_ind = next_node_ind
        return True

    def update(self):
        if self.clear_time <= 0:
            out_lane = self.out_lanes[next_node_ind]
            if out_lane.enter(self.car):
                self.car = None
        else:
            self.clear_time -= 1