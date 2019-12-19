"""Traffic node: a small, standard 4-way intersection"""
class Intersection:
    N_BRANCHES = 4
    # time to clear intersection, from the distance of in and out lane
    CLEAR_TIMES = [1, 2, 1, 0]

    def __init__(self):
        # store the in and out connections
        self.in_directions = {}   # map inlet node to its direction
        self.out_directions = {}  # map outlet node to its direction
        self.out_lanes = {}       # map outlet node to the corresponding lane

        self.car = None
        self.clear_time = -1
        self.cur_out_lane = None

    def set_in_lane(self, direction, lane):
        self.in_directions[lane.prev_node] = direction

    def set_out_lane(self, direction, lane):
        self.out_directions[lane.next_node] = direction
        self.out_lanes[lane.next_node] = lane

    def can_enter(self):
        return self.car is None

    def enter(self, prev_node, car):
        if self.car is not None:
            return False
        self.car = car
        next_node = car.select_next_node()
        dir_diff = self.out_directions[next_node].value - self.in_directions[prev_node].value
        self.clear_time = Intersection.CLEAR_TIMES[dir_diff % Intersection.N_BRANCHES]
        self.cur_out_lane = self.out_lanes[next_node]
        return True

    def update(self):
        if self.clear_time <= 0 and self.cur_out_lane.enter(self.car):
            # if car has been in intersection for long enough,
            # forward it to the next node 
            self.car = None
        else:
            self.clear_time -= 1