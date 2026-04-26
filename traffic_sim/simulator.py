import heapq

class Simulator:
    def __init__(self):
        self.roads = {}
        self.junctions = {}
        self.sources = []
        self.sinks = {}
        
        self.current_epoch = 0
        self.routing_tables = {} # junction_id -> {destination_id: next_road_id}
        
        # For visualization
        self.history = []
        
    def add_road(self, road):
        self.roads[road.id] = road
        if road.source_node in self.junctions:
            self.junctions[road.source_node].add_outgoing_road(road)
        if road.dest_node in self.junctions:
            self.junctions[road.dest_node].add_incoming_road(road)

    def add_junction(self, junction):
        junction.simulator = self
        self.junctions[junction.id] = junction

    def add_source(self, source):
        self.sources.append(source)
        if source.source_node in self.junctions:
            self.junctions[source.source_node].add_local_source(source)

    def add_sink(self, sink):
        self.sinks[sink.node_id] = sink

    def compute_routing_tables(self):
        # Using Dijkstra's algorithm to compute shortest path from all junctions to all destinations
        nodes = list(self.junctions.keys())
        
        for source_node in nodes:
            self.routing_tables[source_node] = {}
            
            # Run Dijkstra from source_node
            distances = {n: float('infinity') for n in nodes}
            previous_road = {n: None for n in nodes}
            distances[source_node] = 0
            
            pq = [(0, source_node)]
            
            while pq:
                current_dist, current_node = heapq.heappop(pq)
                
                if current_dist > distances[current_node]:
                    continue
                    
                if current_node in self.junctions:
                    for road in self.junctions[current_node].outgoing_roads:
                        neighbor = road.dest_node
                        # weight = road.travel_time (or length)
                        weight = road.travel_time
                        
                        distance = current_dist + weight
                        
                        if neighbor in distances and distance < distances[neighbor]:
                            distances[neighbor] = distance
                            previous_road[neighbor] = road.id
                            heapq.heappush(pq, (distance, neighbor))
            
            # Reconstruct first hop for all destinations
            for dest_node in nodes:
                if dest_node != source_node and distances[dest_node] != float('infinity'):
                    # Trace back from dest_node to source_node to find the first hop
                    curr = dest_node
                    first_hop_road = None
                    while curr != source_node:
                        road_id = previous_road[curr]
                        if road_id is None:
                            break
                        first_hop_road = road_id
                        road = self.roads[road_id]
                        curr = road.source_node
                        
                    if first_hop_road:
                        self.routing_tables[source_node][dest_node] = first_hop_road

    def step(self):
        # 1. Sources generate vehicles
        for source in self.sources:
            source.generate(self.current_epoch)
            
        # 2. Roads move vehicles along
        for road in self.roads.values():
            road.step()
            
        # 3. Junctions route vehicles
        for junction in self.junctions.values():
            junction.step(self.routing_tables.get(junction.id, {}), self.sinks)
            
        # 4. Record state for visualization
        self._record_state()
        
        self.current_epoch += 1
        
    def _record_state(self):
        state = {
            'epoch': self.current_epoch,
            'vehicles': []
        }
        
        # Record vehicles on roads
        for road in self.roads.values():
            for item in road.vehicles_traveling:
                state['vehicles'].append({
                    'id': item['vehicle'].id,
                    'source': item['vehicle'].source,
                    'destination': item['vehicle'].destination,
                    'road_id': road.id,
                    'progress': item['vehicle'].progress,
                    'status': 'moving'
                })
            for v in road.end_queue:
                state['vehicles'].append({
                    'id': v.id,
                    'source': v.source,
                    'destination': v.destination,
                    'road_id': road.id,
                    'progress': 1.0,
                    'status': 'waiting'
                })
                
        # Record vehicles in source queues
        for source in self.sources:
            for v in source.queue:
                state['vehicles'].append({
                    'id': v.id,
                    'source': v.source,
                    'destination': v.destination,
                    'node_id': source.source_node,
                    'progress': 0.0,
                    'status': 'source_queue'
                })
                
        self.history.append(state)
