import random
from Car import Car

class CarSpawner:
    def __init__(self, stat, spawn_prob, destinations, dest_weights=None):
        self.stat = stat
        self.spawn_prob = spawn_prob
        self.destinations = destinations
        self.dest_weights = dest_weights

    def set_out_lane(self, direction, lane):
        self.out_lane = lane

    def update(self):
        # spawn car with probability self.spawn_prob
        r = random.random()
        if r > self.spawn_prob:
            return
        destination = random.choices(self.destinations, weights=self.dest_weights)[0]
        car = Car(self.out_lane.next_node, destination, self.stat.cur_time)
        if not self.out_lane.enter(car):
            self.stat.n_rejected += 1