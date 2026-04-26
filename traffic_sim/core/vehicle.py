class Vehicle:
    _id_counter = 0
    
    def __init__(self, source, destination, start_epoch):
        self.id = Vehicle._id_counter
        Vehicle._id_counter += 1
        self.source = source
        self.destination = destination
        self.start_epoch = start_epoch
        self.end_epoch = None
        self.waiting_time = 0  # Total time spent waiting in queues
        
        # Tracking for visualization and stats
        self.current_location = source  # Can be a node_id or road_id
        self.progress = 0.0  # 0.0 to 1.0 if on a road
