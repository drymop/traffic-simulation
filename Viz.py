from tkinter import Tk, Canvas, Label
import time

from CarSpawner import CarSpawner
from CarDespawner import CarDespawner
from Direction import Direction
from Intersection import Intersection
from Roundabout import Roundabout
from Lane import Lane

"""Visualization of traffic network"""
class Viz():
    def __init__(self, matrix, lanes, baseLaneLength, master):
        # intersection that will be at center of canvas
        self.interCenter = (len(matrix[0]) // 2, len(matrix) // 2)
        self.lanes = lanes

        self.matrix = matrix
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

        self.labels = []

    def __initIntersections(self):
        """Initialize intersections"""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j]:
                    self.__drawInter(i, j)


    def __drawUsingPrev(self, lane, label, toDespawner):
        prev_out_dir = lane.prev_out_dir
        if isinstance(lane.prev_node, Intersection):
            coordsPrev = self.canvas.coords(lane.prev_node.vizSquare)
        elif isinstance(lane.prev_node, Roundabout):
            coordsPrev = self.canvas.coords(lane.prev_node.vizCircle)
        length = lane.length * self.laneUnit
        if prev_out_dir == Direction.NORTH:
            coords = (
                    coordsPrev[2] - self.laneWidth,
                    coordsPrev[1] - length,  # y increases downward
                    coordsPrev[2],
                    coordsPrev[1]
            )
            labCoords = (coords[2] + 0.75 * self.laneUnit,
                    (coords[1] + coords[3]) / 2)
        elif prev_out_dir == Direction.SOUTH:
            coords = (
                    coordsPrev[0],
                    coordsPrev[3],
                    coordsPrev[0] + self.laneWidth,
                    coordsPrev[3] + length
            )
            labCoords = (coords[0] - self.laneUnit, (coords[1] + coords[3]) / 2)
        elif prev_out_dir == Direction.EAST:
            coords = (
                    coordsPrev[2],
                    coordsPrev[3] - self.laneWidth,
                    coordsPrev[2] + length,
                    coordsPrev[3]
            )
            labCoords = ((coords[0] + coords[2]) / 2,
                    coords[3] + 0.75 * self.laneUnit)
        elif prev_out_dir == Direction.WEST:
            coords = (
                    coordsPrev[0] - length,
                    coordsPrev[1],
                    coordsPrev[0],
                    coordsPrev[1] + self.laneWidth
            )
            labCoords = ((coords[0] + coords[2]) / 2, coords[1] - 1.5 *
                    self.laneUnit)
        color = "purple" if toDespawner else None
        self.__drawLane(lane, *coords, color)
        self.__placeLabel(label, *labCoords)


    def __drawUsingNext(self, lane, label, fromSpawner):
        next_in_dir = lane.next_in_dir
        if isinstance(lane.next_node, Intersection):
            coordsNext = self.canvas.coords(lane.next_node.vizSquare)
        elif isinstance(lane.next_node, Roundabout):
            coordsNext = self.canvas.coords(lane.next_node.vizCircle)
        length = lane.length * self.laneUnit
        if next_in_dir == Direction.NORTH:
            coords = (
                    coordsNext[0],
                    coordsNext[1] - length,
                    coordsNext[0] + self.laneWidth,
                    coordsNext[1]
            )
            labCoords = (coords[0] - self.laneUnit, (coords[1] + coords[3]) / 2)
        elif next_in_dir == Direction.SOUTH:
            coords = (
                    coordsNext[2] - self.laneWidth,
                    coordsNext[3],
                    coordsNext[2],
                    coordsNext[3] + length
            )
            labCoords = (coords[2] + 0.75 * self.laneUnit,
                    (coords[1] + coords[3]) / 2)
        elif next_in_dir == Direction.EAST:
            coords = (
                    coordsNext[2],
                    coordsNext[1],
                    coordsNext[2] + length,
                    coordsNext[1] + self.laneWidth
            )
            labCoords = ((coords[0] + coords[2]) / 2, coords[1] - self.laneUnit)
        elif next_in_dir == Direction.WEST:
            coords = (
                    coordsNext[0] - length,
                    coordsNext[3] - self.laneWidth,
                    coordsNext[0],
                    coordsNext[3]
            )
            labCoords = ((coords[0] + coords[2]) / 2, coords[3] + 0.75 *
                    self.laneUnit)
        color = "pink" if fromSpawner else None
        self.__drawLane(lane, *coords, color)
        self.__placeLabel(label, *labCoords)


    def __labelText(self, label, text):
        label.configure(text=text)

    def __placeLabel(self, label, x, y):
        label.place(x=x, y=y)


    def __initLanes(self):
        """Initialize lanes"""
        i = 0
        for lane in self.lanes:
            # Label corresponding to lanes[i]
            self.labels.append(Label(self.master, text="0"))
            if lane.prev_out_dir:  # Can use prev as basis for lane dim calc
                self.__drawUsingPrev(lane, self.labels[i],
                        isinstance(lane.next_node, CarDespawner))
            elif lane.next_in_dir:  # Can use next as basis for lane dim calc
                self.__drawUsingNext(lane, self.labels[i],
                        isinstance(lane.prev_node, CarSpawner))

            i += 1


    def initTrafficNetwork(self):
        self.__initIntersections()
        self.__initLanes()


    def update(self):
        self.__updateInterColors()
        self.__updateLaneText()
        self.master.update()

    def __updateLaneText(self):
        for i in range(len(self.lanes)):
            self.__labelText(self.labels[i], str(self.lanes[i].n_cars))

    def __updateInterColors(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j]:
                    if isinstance(self.matrix[i][j], Intersection):
                        if self.matrix[i][j].car:
                            self.__updateInter(i, j, True)
                        else:
                            self.__updateInter(i, j, False)
                    elif isinstance(self.matrix[i][j], Roundabout):
                        if self.matrix[i][j].n_cars > 0:
                            self.__updateInter(i, j, True)
                        else:
                            self.__updateInter(i, j, False)



    def __drawInter(self, i, j):
        """Draw square for intersection matrix[i][j].
        Squares are defined by top left coordinate.
        Draw circle for roundabout matrix[i][j]"""
        if isinstance(self.matrix[i][j], Intersection):
            self.__drawSquare(i, j)
        elif isinstance(self.matrix[i][j], Roundabout):
            self.__drawCircle(i, j)

    def __drawCircle(self, i, j):
        x = (j - self.interCenter[0]) \
            * (2 * self.laneUnit + self.laneUnit * self.baseLaneLength) \
            + self.canvasCenter[0]
        y = (i - self.interCenter[1]) \
            * (2 * self.laneUnit + self.laneUnit * self.baseLaneLength) \
            + self.canvasCenter[1]
        self.matrix[i][j].vizCircle = self.canvas.create_oval(x, y,
                x + 2 * self.laneUnit, y + 2 * self.laneUnit,
                fill="black")

    def __drawSquare(self, i, j):
        x = (j - self.interCenter[0]) \
            * (2 * self.laneUnit + self.laneUnit * self.baseLaneLength) \
            + self.canvasCenter[0]
        y = (i - self.interCenter[1]) \
            * (2 * self.laneUnit + self.laneUnit * self.baseLaneLength) \
            + self.canvasCenter[1]
        self.matrix[i][j].vizSquare = self.canvas.create_rectangle(x, y,
                x + 2 * self.laneUnit, y + 2 * self.laneUnit,
                fill="black")

    def __drawLane(self, lane, x0, y0, x1, y1, color=None):
        """Draw rectangle for lane with given coordinates"""
        lane.vizRect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)


    def __updateInter(self, i, j, occupied):
        """Update intersection color to red if occupied"""
        if occupied:
            if isinstance(self.matrix[i][j], Intersection):
                self.canvas.itemconfig(self.matrix[i][j].vizSquare,
                    fill="red")
            elif isinstance(self.matrix[i][j], Roundabout):
                print("HOLA")
                self.canvas.itemconfig(self.matrix[i][j].vizCircle,
                    fill="red")
        else:
            if isinstance(self.matrix[i][j], Intersection):
                self.canvas.itemconfig(self.matrix[i][j].vizSquare,
                    fill="black")
            elif isinstance(self.matrix[i][j], Roundabout):
                self.canvas.itemconfig(self.matrix[i][j].vizCircle,
                    fill="black")


def connect(lanes, matrix, length, i0, j0, i1, j1):
    if i0 == i1:  # horizontal
        lanes.append(Lane(length, matrix[i0][j0], Direction.EAST,
            matrix[i1][j1], Direction.WEST))
        lanes.append(Lane(length, matrix[i1][j1], Direction.WEST,
            matrix[i0][j0], Direction.EAST))
    else:  # vertical
        lanes.append(Lane(length, matrix[i0][j0], Direction.SOUTH,
            matrix[i1][j1], Direction.NORTH))
        lanes.append(Lane(length, matrix[i1][j1], Direction.NORTH,
            matrix[i0][j0], Direction.SOUTH))

if __name__ == "__main__":
    row, col = 3, 3
    #matrix = [[Intersection() for j in range(col)] for i in range(row)]
    matrix = [[Roundabout(1) for j in range(col)] for i in range(row)]
    # make a few of them None
    matrix[0][2] = None
    matrix[2][1] = None

    d = CarDespawner()
    spawns = [CarSpawner(0.5, [d]), CarSpawner(0.5, [d])]

    # connect lanes
    baseLaneLen = 3
    lanes = []

    # spawn/despawn lanes first
    lanes.append(Lane(baseLaneLen, spawns[0], None, matrix[0][0],
        Direction.WEST))
    lanes.append(Lane(baseLaneLen, spawns[1], None, matrix[2][2],
        Direction.SOUTH))
    lanes.append(Lane(baseLaneLen, matrix[2][0], Direction.SOUTH, d, None))

    # always order endpoints as northern node, southern node OR
    #                           western node, eastern node
    connect(lanes, matrix, baseLaneLen, 0, 0, 0, 1)
    connect(lanes, matrix, baseLaneLen, 0, 0, 1, 0)
    connect(lanes, matrix, baseLaneLen, 1, 0, 1, 1)
    connect(lanes, matrix, baseLaneLen, 0, 1, 1, 1)
    connect(lanes, matrix, baseLaneLen, 1, 0, 2, 0)
    connect(lanes, matrix, baseLaneLen, 1, 1, 1, 2)
    connect(lanes, matrix, baseLaneLen, 1, 2, 2, 2)

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

        d.update()

        for spawn in spawns:
            spawn.update()

        # Then update viz
        viz.update()

        time.sleep(pause)

    # Close window to terminate
    root.mainloop()
