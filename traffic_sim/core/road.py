import math
from collections import deque

class Road:
    def __init__(self, road_id, source_node, dest_node, length, max_speed, capacity):
        self.id = road_id
        self.source_node = source_node
        self.dest_node = dest_node
        self.length = length
        self.max_speed = max_speed
        self.capacity = capacity
        
        self.travel_time = math.ceil(length / max_speed)
        
        # Vehicles currently traveling on the road
        # Format: {'vehicle': v, 'time_remaining': t}
        self.vehicles_traveling = []
        
        # Vehicles that have reached the end of the road and are waiting to enter the next junction
        self.end_queue = deque()

    def get_num_vehicles(self):
        return len(self.vehicles_traveling) + len(self.end_queue)

    def can_enter(self):
        return self.get_num_vehicles() < self.capacity

    def enter(self, vehicle):
        if not self.can_enter():
            return False
        
        self.vehicles_traveling.append({
            'vehicle': vehicle,
            'time_remaining': self.travel_time
        })
        vehicle.current_location = self.id
        vehicle.progress = 0.0
        return True

    def step(self):
        # Move vehicles along the road
        arrived_this_step = []
        for item in self.vehicles_traveling:
            item['time_remaining'] -= 1
            # Update visual progress
            item['vehicle'].progress = 1.0 - (item['time_remaining'] / self.travel_time) if self.travel_time > 0 else 1.0
            
            if item['time_remaining'] <= 0:
                arrived_this_step.append(item)
                
        # Move arrived vehicles to the end queue
        for item in arrived_this_step:
            self.vehicles_traveling.remove(item)
            item['vehicle'].progress = 1.0
            self.end_queue.append(item['vehicle'])

        # Increment wait time for vehicles in the queue
        for v in self.end_queue:
            v.waiting_time += 1
