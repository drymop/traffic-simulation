class CarDespawner:
    def __init__(self, stats):
        self.out_lanes = {}
        self.stats = stats
        pass

    def set_in_lane(self, direction, lane):
        # don't care
        pass

    def enter(self, prev_node, car):
        # simply despawn the car
        car_time = self.stats.cur_time - car.start_time
        self.stats.car_times.append(car_time)
        return True

    def update(self):
        # do nothing
        pass