class Sink:
    def __init__(self, node_id):
        self.node_id = node_id
        self.arrived_vehicles = []
        
    def absorb(self, vehicle, current_epoch):
        vehicle.end_epoch = current_epoch
        vehicle.current_location = self.node_id
        self.arrived_vehicles.append(vehicle)
