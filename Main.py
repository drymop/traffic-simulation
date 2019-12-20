from tkinter import Tk, Canvas, Label
import time
import random

from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Direction import Direction
from Intersection import Intersection
from Roundabout import Roundabout
from Lane import Lane
from Viz import Viz, connect
from Stats import Stats


def main():
    #CHANGE THESE FLAGS TO CONTROL THE EXPERIMENT

    VIZ = False  # Set to True for visualization
    USE_ROUNDABOUT = True # Set to True to use roundabout
    PAUSE = 0.1 # time (in sec) between each update, if VIZ is True
    MAX_TIME = 1000000
    SEED = 0
    SPAWN_PROB = 0.1

    row, col = 2, 2
    stat = Stats()

    # grid of intersection/roundabout
    if USE_ROUNDABOUT:
        matrix = [[Roundabout(1) for j in range(col)] for i in range(row)]
    else:
        matrix = [[Intersection() for j in range(col)] for i in range(row)]

    despawns = [CarDespawner(stat) for i in range(row * 4)]
    spawns = [CarSpawner(stat, SPAWN_PROB, despawns) for i in range(col * 4)]

    # connect lanes
    baseLaneLen = 10
    lanes = []

    # spawn/despawn lanes first
    lanes.append(Lane(baseLaneLen, spawns[0], None, matrix[0][0],
        Direction.NORTH))
    lanes.append(Lane(baseLaneLen, spawns[1], None, matrix[0][1],
        Direction.NORTH))
    lanes.append(Lane(baseLaneLen, spawns[2], None, matrix[0][1],
        Direction.EAST))
    lanes.append(Lane(baseLaneLen, spawns[3], None, matrix[1][1],
        Direction.EAST))
    lanes.append(Lane(baseLaneLen, spawns[4], None, matrix[1][1],
        Direction.SOUTH))
    lanes.append(Lane(baseLaneLen, spawns[5], None, matrix[1][0],
        Direction.SOUTH))
    lanes.append(Lane(baseLaneLen, spawns[6], None, matrix[1][0],
        Direction.WEST))
    lanes.append(Lane(baseLaneLen, spawns[7], None, matrix[0][0],
        Direction.WEST))

    lanes.append(Lane(baseLaneLen, matrix[0][0], Direction.NORTH, despawns[0],
        None))
    lanes.append(Lane(baseLaneLen, matrix[0][1], Direction.NORTH, despawns[1],
        None))
    lanes.append(Lane(baseLaneLen, matrix[0][1], Direction.EAST, despawns[2],
        None))
    lanes.append(Lane(baseLaneLen, matrix[1][1], Direction.EAST, despawns[3],
        None))
    lanes.append(Lane(baseLaneLen, matrix[1][1], Direction.SOUTH, despawns[4],
        None))
    lanes.append(Lane(baseLaneLen, matrix[1][0], Direction.SOUTH, despawns[5],
        None))
    lanes.append(Lane(baseLaneLen, matrix[1][0], Direction.WEST, despawns[6],
        None))
    lanes.append(Lane(baseLaneLen, matrix[0][0], Direction.WEST, despawns[7],
        None))

    # always order endpoints as northern node, southern node OR
    #                           western node, eastern node
    connect(lanes, matrix, baseLaneLen, 0, 0, 0, 1)
    connect(lanes, matrix, baseLaneLen, 0, 0, 1, 0)
    connect(lanes, matrix, baseLaneLen, 0, 1, 1, 1)
    connect(lanes, matrix, baseLaneLen, 1, 0, 1, 1)

    if VIZ:
        root = Tk()
        viz = Viz(matrix, lanes, baseLaneLen, root)

    random.seed(SEED)
    for x in range(MAX_TIME):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j]:
                    matrix[i][j].update()

        for lane in lanes:
            lane.update()

        for spawn in spawns:
            spawn.update()

        stat.cur_time += 1

        # Then update viz
        if VIZ:
            viz.update()
            time.sleep(PAUSE)

    print(len(stat.car_times))
    print(sum(stat.car_times)/len(stat.car_times))
    print(stat.n_rejected)

    # Close window to terminate
    if VIZ:
        root.mainloop()

main()
