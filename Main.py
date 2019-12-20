from tkinter import Tk, Canvas, Label
import time

from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Direction import Direction
from Intersection import Intersection
from Roundabout import Roundabout
from Lane import Lane
from Viz import Viz, connect

def main():
    row, col = 2, 2

    # TODO: This is the line to replace for intersection type
    matrix = [[Intersection() for j in range(col)] for i in range(row)]
    #matrix = [[Roundabout(1) for j in range(col)] for i in range(row)]

    despawns = [CarDespawner(), CarDespawner()]
    spawns = [CarSpawner(0.5, [despawns[0]]), CarSpawner(0.5, [despawns[1]])]

    # connect lanes
    baseLaneLen = 5  # TODO: Change this for roundabout to 3
    lanes = []

    # spawn/despawn lanes first
    lanes.append(Lane(baseLaneLen, spawns[0], None, matrix[0][0],
        Direction.NORTH))
    lanes.append(Lane(baseLaneLen, spawns[1], None, matrix[0][1],
        Direction.NORTH))
    lanes.append(Lane(baseLaneLen, matrix[1][0], Direction.SOUTH, despawns[0],
        None))
    lanes.append(Lane(baseLaneLen, matrix[1][1], Direction.SOUTH, despawns[1],
        None))

    # always order endpoints as northern node, southern node OR
    #                           western node, eastern node
    connect(lanes, matrix, baseLaneLen, 0, 0, 0, 1)
    connect(lanes, matrix, baseLaneLen, 0, 0, 1, 0)
    connect(lanes, matrix, baseLaneLen, 0, 1, 1, 1)
    connect(lanes, matrix, baseLaneLen, 1, 0, 1, 1)

    root = Tk()
    viz = Viz(matrix, lanes, baseLaneLen, root)

    pause = 1
    for x in range(100):
        print("Iter", x)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j]:
                    matrix[i][j].update()

        for lane in lanes:
            lane.update()

        for despawn in despawns:
            despawn.update()

        for spawn in spawns:
            spawn.update()

        # Then update viz
        viz.update()

        time.sleep(pause)

    # Close window to terminate
    root.mainloop()

main()
