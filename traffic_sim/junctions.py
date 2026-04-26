class RoundRobinStrategy:
    def __init__(self):
        self.current_idx = 0
        
    def schedule(self, junction, routing_table, sinks):
        # We can pull from both incoming roads and local traffic sources
        queues = []
        for r in junction.incoming_roads:
            if len(r.end_queue) > 0:
                queues.append(r.end_queue)
                
        for s in junction.local_sources:
            if len(s.queue) > 0:
                queues.append(s.queue)
                
        if not queues:
            return
            
        # Process up to junction.capacity vehicles per epoch
        # For simplicity, let's say capacity is 1 vehicle per epoch
        # Or capacity = number of outgoing roads? Let's process 1 vehicle per incoming queue max
        
        # We will iterate through queues starting from current_idx
        processed_any = False
        num_queues = len(queues)
        start_idx = self.current_idx % num_queues
        
        for i in range(num_queues):
            idx = (start_idx + i) % num_queues
            q = queues[idx]
            
            if len(q) == 0:
                continue
                
            vehicle = q[0]
            
            # Check if it has arrived at its destination sink
            if vehicle.destination == junction.id and junction.id in sinks:
                q.popleft()
                sinks[junction.id].absorb(vehicle, junction.simulator.current_epoch)
                self.current_idx = (idx + 1) % num_queues
                processed_any = True
                continue
            
            # Look up next road
            if vehicle.destination in routing_table:
                next_road_id = routing_table[vehicle.destination]
                next_road = junction.outgoing_roads_map.get(next_road_id)
                
                if next_road and next_road.can_enter():
                    q.popleft()
                    next_road.enter(vehicle)
                    self.current_idx = (idx + 1) % num_queues
                    processed_any = True
                else:
                    # Next road is full, vehicle must wait
                    pass
            else:
                # No route found? Drop the vehicle or keep waiting
                pass

class Junction:
    def __init__(self, node_id, strategy=None):
        self.id = node_id
        self.incoming_roads = []
        self.outgoing_roads = []
        self.outgoing_roads_map = {}
        self.local_sources = []
        
        self.strategy = strategy if strategy else RoundRobinStrategy()
        
        # Will be set by simulator
        self.simulator = None 

    def add_incoming_road(self, road):
        self.incoming_roads.append(road)

    def add_outgoing_road(self, road):
        self.outgoing_roads.append(road)
        self.outgoing_roads_map[road.id] = road
        
    def add_local_source(self, source):
        self.local_sources.append(source)
        
    def step(self, routing_table, sinks):
        self.strategy.schedule(self, routing_table, sinks)
