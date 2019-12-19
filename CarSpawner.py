import random
from Car import Car

class CarSpawner:
    def __init__(self, spawn_prob, destinations, dest_weights=None):
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
        destination = random.choices(destinations, weights=self.dest_weights)
        car = Car(self.out_lane.next_node, destination)
        self.out_lane.enter(car)