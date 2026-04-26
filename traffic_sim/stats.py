import numpy as np

class StatsCollector:
    def __init__(self, simulator):
        self.simulator = simulator
        
    def generate_report(self):
        print("\n--- Simulation Statistics ---")
        
        # 1. Vehicle Statistics
        arrived_vehicles = []
        for sink in self.simulator.sinks.values():
            arrived_vehicles.extend(sink.arrived_vehicles)
            
        from traffic_sim.core import Vehicle
        print(f"Total Vehicles Generated: {Vehicle._id_counter}")
        print(f"Total Vehicles Arrived at Destination: {len(arrived_vehicles)}")
        
        if arrived_vehicles:
            travel_times = [v.end_epoch - v.start_epoch for v in arrived_vehicles]
            wait_times = [v.waiting_time for v in arrived_vehicles]
            
            print(f"Average Travel Time: {np.mean(travel_times):.2f} epochs")
            print(f"Max Travel Time: {np.max(travel_times)} epochs")
            print(f"Average Waiting Time: {np.mean(wait_times):.2f} epochs")
            print(f"Max Waiting Time: {np.max(wait_times)} epochs")
            
        # 2. Road Statistics
        print("\n--- Road Statistics ---")
        for road_id, road in self.simulator.roads.items():
            print(f"Road {road_id} ({road.source_node} -> {road.dest_node}):")
            print(f"  Current Vehicles Traveling: {len(road.vehicles_traveling)}")
            print(f"  Current End Queue Length: {len(road.end_queue)}")
            print(f"  Capacity Utilization: {road.get_num_vehicles() / road.capacity * 100:.1f}%")
