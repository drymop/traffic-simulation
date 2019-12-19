from Direction import Direction
from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Intersection import Intersection
from Lane import Lane


def main():
    d = CarDespawner()
    s = CarSpawner(0.5, [d])
    lane = Lane(10, s, None, d, None)

    for i in range(100):
        d.update()
        lane.update()
        s.update()
        print(lane)
        print("-" * 100)


if __name__ == '__main__':
    main()