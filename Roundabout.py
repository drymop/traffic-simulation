from collections import deque
import math


"""Traffic node: a small, standard 4-way intersection"""
class Roundabout:
    N_BRANCHES = 4

    def __init__(self, quarter_arc_len):
        # store the in and out connections
        self.in_directions = {}   # map inlet node to its direction
        self.out_directions = {}  # map outlet node to its direction
        self.out_lanes = {}       # map outlet node to the corresponding lane

        # keep track of the car within this roundabout
        # cars travel in counter clock-wise direction
        # (increasing index in array)
        # and wrap around at max index -> 0
        self.cars = [None] * (quarter_arc_len+2) * Roundabout.N_BRANCHES
        self.n_cars = 0

        # map direction to index of inlet/outlets
        self.out_positions = [(quarter_arc_len+2) * i for i in range(Roundabout.N_BRANCHES)]
        self.in_positions  = [p+1 for p in self.out_positions]

        # viz stuff
        self.vizCircle = None


    def set_in_lane(self, direction, lane):
        self.in_directions[lane.prev_node] = direction

    def set_out_lane(self, direction, lane):
        self.out_directions[lane.next_node] = direction
        self.out_lanes[lane.next_node] = lane

    def enter(self, prev_node, car):
        in_dir = self.in_directions[prev_node]
        pos = self.in_positions[in_dir.value]
        if self.cars[pos] is not None:
            return False
        self.cars[pos] = car
        self.n_cars += 1
        return True

    def update(self):
        # first, check if any car can leave
        # if so, forward them to their next nodes
        for out_node, out_dir in self.out_directions.items():
            lane = self.out_lanes[out_node]
            pos = self.out_positions[out_dir.value]
            car = self.cars[pos]
            if car is None:
                continue
            if car.select_next_node(self) == out_node and lane.enter(car):
                self.cars[pos] = None
                self.n_cars -= 1
        # move every car forward
        last_car = self.cars[-1]
        for i in range(len(self.cars)-1, 0, -1):
            self.cars[i] = self.cars[i-1]
        self.cars[0] = last_car

    def __str__(self):
        cells = []
        for i, car in enumerate(self.cars):
            if i in self.in_positions:
                c = "^"
            elif i in self.out_positions:
                c = "v"
            else:
                c = " "
            if car:
                s = "%s %3d " % (c, car.car_id)
            else:
                s = "%s     " % c
            cells.append(s)
        cells.reverse()
        return "|".join(cells)
