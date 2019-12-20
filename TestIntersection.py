from Direction import Direction
from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Intersection import Intersection
from Lane import Lane


def main():
    d = CarDespawner()
    s1 = CarSpawner(0.5, [d])
    s2 = CarSpawner(0.5, [d])
    inter = Intersection()
    lane1 = Lane(5, s1, None, inter, Direction.SOUTH)
    lane2 = Lane(5, s2, None, inter, Direction.WEST)
    lane3 = Lane(5, inter, Direction.NORTH, d, None)

    for i in range(100):
        d.update()
        lane1.update()
        lane2.update()
        lane3.update()
        inter.update()
        s1.update()
        s2.update()
        print(lane3, end=" ||| ")
        print(inter, end=" ||| ")
        print(lane1)
        print(" " * 51, end="")
        print(lane2)
        print("-" * 100)


if __name__ == '__main__':
    main()
