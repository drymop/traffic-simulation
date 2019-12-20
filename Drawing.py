from tkinter import Tk, Canvas
import time

from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Direction import Direction
from Intersection import Intersection
from Lane import Lane

"""Visualization of traffic network"""
class Viz():
    def __init__(self, interMatrix, lanes, baseLaneLength, master):
        # intersection that will be at center of canvas
        self.interCenter = (len(interMatrix[0]) // 2, len(interMatrix) // 2)
        self.lanes = lanes

        self.interMatrix = interMatrix
        self.baseLaneLength = baseLaneLength

        self.master = master

        self.initUI()
        self.initTrafficNetwork()


    def initUI(self):
        """Initialize canvas and drawing items"""
        self.master.title("Intersection Network")

        self.canvasWidth = 1000
        self.canvasHeight = 1000
        self.master.geometry("{0}x{1}+0+0".format(self.canvasWidth,
            self.canvasHeight))

        print("CanvasDim:", (self.canvasWidth, self.canvasHeight))

        self.canvasCenter = (self.canvasWidth // 2, self.canvasHeight // 2)
        print("CanvasCenter:", self.canvasCenter)

        self.laneUnit = 15
        self.laneGap = 4
        self.laneWidth = self.laneUnit - self.laneGap / 2

        self.canvas = Canvas(self.master)
        self.canvas.pack(fill="both", expand=True)

    def __initIntersections(self):
        """Initialize intersections"""
        for i in range(len(self.interMatrix)):
            for j in range(len(self.interMatrix[0])):
                if self.interMatrix[i][j]:
                    self.__drawInter(i, j)


    def __drawUsingPrev(self, lane, toDespawner):
        prev_out_dir = lane.prev_out_dir
        coordsPrev = self.canvas.coords(lane.prev_node.vizSquare)
        length = lane.length * self.laneUnit
        if prev_out_dir == Direction.NORTH:
            coords = (
                    coordsPrev[2] - self.laneWidth,
                    coordsPrev[1] - length,  # y increases downward
                    coordsPrev[2],
                    coordsPrev[1]
            )
        elif prev_out_dir == Direction.SOUTH:
            coords = (
                    coordsPrev[0],
                    coordsPrev[3],
                    coordsPrev[0] + self.laneWidth,
                    coordsPrev[3] + length
            )
        elif prev_out_dir == Direction.EAST:
            coords = (
                    coordsPrev[2],
                    coordsPrev[3] - self.laneWidth,
                    coordsPrev[2] + length,
                    coordsPrev[3]
            )
        elif prev_out_dir == Direction.WEST:
            coords = (
                    coordsPrev[0] - length,
                    coordsPrev[1],
                    coordsPrev[0],
                    coordsPrev[1] + self.laneWidth
            )
        color = "purple" if toDespawner else None
        self.__drawLane(lane, *coords, color)


    def __drawUsingNext(self, lane, fromSpawner):
        next_in_dir = lane.next_in_dir
        coordsNext = self.canvas.coords(lane.next_node.vizSquare)
        length = lane.length * self.laneUnit
        if next_in_dir == Direction.NORTH:
            coords = (
                    coordsNext[0],
                    coordsNext[1] - length,
                    coordsNext[0] + self.laneWidth,
                    coordsNext[1]
            )
        elif next_in_dir == Direction.SOUTH:
            coords = (
                    coordsNext[2] - self.laneWidth,
                    coordsNext[3],
                    coordsNext[2],
                    coordsNext[3] + length
            )
        elif next_in_dir == Direction.EAST:
            coords = (
                    coordsNext[2],
                    coordsNext[1],
                    coordsNext[2] + length,
                    coordsNext[1] + self.laneWidth
            )
        elif next_in_dir == Direction.WEST:
            coords = (
                    coordsNext[0] - length,
                    coordsNext[3] - self.laneWidth,
                    coordsNext[0],
                    coordsNext[3]
            )
        color = "pink" if fromSpawner else None
        self.__drawLane(lane, *coords, color)


    def __initLanes(self):
        """Initialize lanes"""
        for lane in self.lanes:
            if lane.prev_out_dir:  # Can use prev as basis for lane dim calc
                self.__drawUsingPrev(lane, isinstance(lane.next_node,
                    CarDespawner))
            elif lane.next_in_dir:  # Can use next as basis for lane dim calc
                self.__drawUsingNext(lane, isinstance(lane.prev_node,
                    CarSpawner))


    def initTrafficNetwork(self):
        self.__initIntersections()
        self.__initLanes()


    def update(self):
        self.__updateInterColors()
        self.master.update()

    def __updateInterColors(self):
        for i in range(len(self.interMatrix)):
            for j in range(len(self.interMatrix[0])):
                if self.interMatrix[i][j]:
                    if self.interMatrix[i][j].car:
                        self.__updateInter(i, j, True)
                    else:
                        self.__updateInter(i, j, False)


    def __drawInter(self, i, j):
        """Draw square for intersection interMatrix[i][j].
        Squares are defined by top left coordinate."""
        x = (j - self.interCenter[0]) \
            * (2 * self.laneUnit + self.laneUnit * self.baseLaneLength) \
            + self.canvasCenter[0]
        y = (i - self.interCenter[1]) \
            * (2 * self.laneUnit + self.laneUnit * self.baseLaneLength) \
            + self.canvasCenter[1]
        print("Drawing inter[{}][{}] at canvas ({},{})".format(i, j, x, y))
        self.interMatrix[i][j].vizSquare = self.canvas.create_rectangle(x, y,
                x + 2 * self.laneUnit, y + 2 * self.laneUnit,
                fill="black")

    def __drawLane(self, lane, x0, y0, x1, y1, color=None):
        """Draw rectangle for lane with given coordinates"""
        lane.vizRect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)


    def __updateInter(self, i, j, occupied):
        """Update intersection color to red if occupied"""
        if occupied:
            self.canvas.itemconfig(self.interMatrix[i][j].vizSquare,
                fill="red")
        else:
            self.canvas.itemconfig(self.interMatrix[i][j].vizSquare,
                fill="black")


def connect(lanes, length, i0, j0, i1, j1):
    if i0 == i1:  # horizontal
        lanes.append(Lane(length, interMatrix[i0][j0], Direction.EAST,
            interMatrix[i1][j1], Direction.WEST))
        lanes.append(Lane(length, interMatrix[i1][j1], Direction.WEST,
            interMatrix[i0][j0], Direction.EAST))
    else:  # vertical
        lanes.append(Lane(length, interMatrix[i0][j0], Direction.SOUTH,
            interMatrix[i1][j1], Direction.NORTH))
        lanes.append(Lane(length, interMatrix[i1][j1], Direction.NORTH,
            interMatrix[i0][j0], Direction.SOUTH))

if __name__ == "__main__":
    row, col = 3, 3
    interMatrix = [[Intersection() for j in range(col)] for i in range(row)]
    # make a few of them None
    interMatrix[0][2] = None
    interMatrix[2][1] = None

    d = CarDespawner()
    spawns = [CarSpawner(0.5, [d]), CarSpawner(0.5, [d])]

    # connect lanes
    baseLaneLen = 5
    lanes = []

    # spawn/despawn lanes first
    lanes.append(Lane(baseLaneLen, spawns[0], None, interMatrix[0][0],
        Direction.WEST))
    lanes.append(Lane(baseLaneLen, spawns[1], None, interMatrix[2][2],
        Direction.SOUTH))
    lanes.append(Lane(baseLaneLen, interMatrix[2][0], Direction.SOUTH, d, None))

    # always order endpoints as northern point, southern point OR
    #                           western point, eastern point
    connect(lanes, baseLaneLen, 0, 0, 0, 1)
    connect(lanes, baseLaneLen, 0, 0, 1, 0)
    connect(lanes, baseLaneLen, 1, 0, 1, 1)
    connect(lanes, baseLaneLen, 0, 1, 1, 1)
    connect(lanes, baseLaneLen, 1, 0, 2, 0)
    connect(lanes, baseLaneLen, 1, 1, 1, 2)
    connect(lanes, baseLaneLen, 1, 2, 2, 2)

    root = Tk()
    viz = Viz(interMatrix, lanes, baseLaneLen, root)

    pause = 3
    for i in range(100):
        for i in range(len(interMatrix)):
            for j in range(len(interMatrix[0])):
                if interMatrix[i][j]:
                    interMatrix[i][j].update()

        d.update()

        for lane in lanes:
            lane.update()

        for spawn in spawns:
            spawn.update()

        # Then update viz
        viz.update()

        time.sleep(pause)

    # Close window to terminate
    root.mainloop()
