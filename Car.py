import heapq
import math


"""A car"""
class Car:

    num_cars = 0

    def __init__(self, origin, destination):
        self.car_id = Car.num_cars
        Car.num_cars += 1
        self.destination = destination
        self._rev_path = self._dijkstra(origin, destination)

    def _dijkstra(self, origin, destination):
        """Find the (reversed) shortest path from origin to destination"""
        dist = {origin: 0}
        prev = {}
        q = [(0, origin)]
        while q:
            d, node = heapq.heappop(q)
            if node == destination:
                break
            if d >= dist.get(node, math.inf):
                continue
            for next_node, lane in node.out_lanes:
                d2 = d + lane.length
                if d2 < dist.get(next_node, math.inf):
                    dist[next_node] = d2
                    prev[next_node] = node
                    heapq.heappush(q, (d2, next_node))
        rev_path = [destination]
        while node in prev:
            prev_node = prev[node]
            path.append(prev_node)
            node = prev_node
        return rev_path

    def select_next_node(self):
        """Select which of the next traffic node to travel to"""
        return self._rev_path.pop()

