from Direction import Direction
from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Roundabout import Roundabout
from Lane import Lane


def main():
    d = CarDespawner()
    s1 = CarSpawner(0.5, [d])
    s2 = CarSpawner(0.5, [d])
    r = Roundabout(1)
    lane1 = Lane(5, s1, None, r, Direction.SOUTH)
    lane2 = Lane(5, s2, None, r, Direction.WEST)
    lane3 = Lane(5, r, Direction.NORTH, d, None)

    for i in range(20):
        d.update()
        r.update()
        lane1.update()
        lane2.update()
        lane3.update()
        s1.update()
        s2.update()
        print(lane1)
        print(lane2)
        print()
        print(r)
        print()
        print(lane3)
        print("-" * 100)


if __name__ == '__main__':
    main()
