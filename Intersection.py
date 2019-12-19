from collections import deque
import math


"""Traffic node: a small, standard 4-way intersection"""
class Intersection:
    N_BRANCHES = 4
    # time to clear intersection, from the distance of in and out lane
    CLEAR_TIMES = [2, 3, 2, 1]

    def __init__(self):
        # store the in and out connections
        self.in_directions = {}   # map inlet node to its direction
        self.out_directions = {}  # map outlet node to its direction
        self.out_lanes = {}       # map outlet node to the corresponding lane

        # keep track of the car within this intersection
        self.car = None
        self.clear_time = math.inf
        self.cur_out_lane = None

        # queue of car waiting to enter
        self.wait_queue = deque()
        self.waiting_cars = set()


    def set_in_lane(self, direction, lane):
        self.in_directions[lane.prev_node] = direction

    def set_out_lane(self, direction, lane):
        self.out_directions[lane.next_node] = direction
        self.out_lanes[lane.next_node] = lane

    def enter(self, prev_node, car):
        if self.car is not None:
            # the car has to wait because intersection is occupied
            # add the car to the wait queue, if it's not already in the queue
            if car not in self.waiting_cars:
                self.waiting_cars.add(car)
                self.wait_queue.append(car)
            return False
        if self.wait_queue and self.wait_queue[0] != car:
            return False
        if self.wait_queue:
            self.wait_queue.popleft()
            self.waiting_cars.remove(car)
        self.car = car
        next_node = car.select_next_node(self)
        dir_diff = self.out_directions[next_node].value - self.in_directions[prev_node].value
        self.clear_time = Intersection.CLEAR_TIMES[dir_diff % Intersection.N_BRANCHES]
        self.cur_out_lane = self.out_lanes[next_node]
        return True

    def update(self):
        if self.clear_time <= 0 and self.cur_out_lane.enter(self.car):
            # if car has been in intersection for long enough,
            # forward it to the next node 
            self.car = None
            self.clear_time = math.inf
        else:
            self.clear_time -= 1

    def __str__(self):
        if self.car:
            return "%3d (%3d)" % (self.car.car_id, self.clear_time)
        else:
            return " (empty) "