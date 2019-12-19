from Direction import Direction
from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Intersection import Intersection
from Lane import Lane


def main():
    d = CarDespawner()
    s = CarSpawner(0.5, [d])
    inter = Intersection()
    lane1 = Lane(5, s, None, inter, Direction.SOUTH)
    lane2 = Lane(5, inter, Direction.NORTH, d, None)

    for i in range(100):
        d.update()
        lane1.update()
        lane2.update()
        inter.update()
        s.update()
        print(lane2, end=" ||| ")
        print(inter, end=" ||| ")
        print(lane1)
        print("-" * 100)


if __name__ == '__main__':
    main()