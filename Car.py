import heapq
import math


"""A car"""
class Car:

    num_cars = 0

    def __init__(self, origin, destination):
        self.car_id = Car.num_cars
        Car.num_cars += 1
        self.destination = destination
        self._next_node = self._dijkstra(origin, destination)

    def _dijkstra(self, origin, destination):
        """Find the shortest path from origin to destination"""
        dist = {origin: 0}
        prev = {}
        # queue store triplet of distance, id, node
        # id is needed for tie-break
        q = [(0, id(origin), origin)]
        while q:
            d, _, node = heapq.heappop(q)
            if node == destination:
                break
            if d > dist.get(node, math.inf):
                continue
            for next_node, lane in node.out_lanes.items():
                d2 = d + lane.length
                if d2 < dist.get(next_node, math.inf):
                    dist[next_node] = d2
                    prev[next_node] = node
                    heapq.heappush(q, (d2, id(next_node), next_node))
        next_node = {}
        node = destination
        while node in prev:
            prev_node = prev[node]
            next_node[prev_node] = node
            node = prev_node
        return next_node

    def select_next_node(self, cur_node):
        """Select which of the next traffic node to travel to"""
        return self._next_node[cur_node]

