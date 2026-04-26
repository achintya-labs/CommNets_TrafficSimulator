from collections import deque
from .vehicle import Vehicle

class TrafficSource:
    def __init__(self, source_node, destination_node, generator):
        self.source_node = source_node
        self.destination_node = destination_node
        self.generator = generator
        self.queue = deque() # Vehicles waiting to enter the network
        
    def generate(self, epoch):
        num_vehicles = self.generator.generate(epoch)
        for _ in range(num_vehicles):
            v = Vehicle(self.source_node, self.destination_node, epoch)
            self.queue.append(v)
        return num_vehicles > 0
