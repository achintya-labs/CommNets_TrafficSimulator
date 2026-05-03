from traffic_sim.core import Road, Sink, TrafficSource
from traffic_sim.TrafficGeneratorDistribution import BernoulliGenerator, PoissonGenerator
from traffic_sim.junctions import Junction, RoundRobinStrategy
from traffic_sim.simulator import Simulator
from traffic_sim.stats import StatsCollector
from traffic_sim.visualization import Visualizer

def main():
    # 1. Initialize Simulator
    sim = Simulator()
    
    # 2. Define network topology (Nodes/Junctions & Sinks)
    # We create a simple planar network
    # N0 -> N1 -> N2 -> N4
    #       |     ^
    #       v     |
    #       N3 ---+
    
    node_positions = {
        'N0': (0, 0),
        'N1': (0, 1),
        'N2': (0, 2),
        'N3': (1, 0),
        'N4': (1, 1),
        'N5': (1, 2),
        'N6': (2, 0),
        'N7': (2, 1),
        'N8': (2, 2),
        'N9': (3, 0),
        'N10': (3, 1),
        'N11': (3, 2),

    }
    
    # Add Junctions
    for node in node_positions.keys():
        sim.add_junction(Junction(node, strategy=RoundRobinStrategy()))


    # Add Sinks
    sim.add_sink(Sink('N9'))
    sim.add_sink(Sink('N11')) # N2 also acts as a sink for some traffic
    sim.add_sink(Sink('N2')) # N2 also acts as a sink for some traffic

    # 3. Add Roads (id, src, dst, length, max_speed, capacity)
    sim.add_road(Road('R_3_4', 'N3', 'N4', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_4_3', 'N4', 'N3', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_4_5', 'N4', 'N5', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_5_4', 'N5', 'N4', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_6_7', 'N6', 'N7', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_7_6', 'N7', 'N6', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_7_8', 'N7', 'N8', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_8_7', 'N8', 'N7', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_0_3', 'N0', 'N3', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_3_0', 'N3', 'N0', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_3_6', 'N3', 'N6', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_6_3', 'N6', 'N3', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_6_9', 'N6', 'N9', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_9_6', 'N9', 'N6', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_1_4', 'N1', 'N4', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_4_1', 'N4', 'N1', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_4_7', 'N4', 'N7', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_7_4', 'N7', 'N4', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_7_10', 'N7', 'N10', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_10_7', 'N10', 'N7', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_2_5', 'N2', 'N5', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_5_2', 'N5', 'N2', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_5_8', 'N5', 'N8', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_8_5', 'N8', 'N5', length=10, max_speed=5, capacity=5))

    sim.add_road(Road('R_8_11', 'N8', 'N11', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_11_8', 'N11', 'N8', length=10, max_speed=5, capacity=5))
    
    
    # 4. Add Traffic Sources
    sim.add_source(TrafficSource('N0', 'N11', generator=BernoulliGenerator(0.4)))
    sim.add_source(TrafficSource('N1', 'N9', generator=PoissonGenerator(0.4)))
    sim.add_source(TrafficSource('N10', 'N2', generator=PoissonGenerator(0.4)))

    # sim.add_source(TrafficSource('N1', 'N4', generator=BernoulliGenerator(0.1)))
    
    # 5. Compute Routes
    sim.compute_routing_tables()
    print("Routing tables computed:")
    for src, targets in sim.routing_tables.items():
        print(f"  From {src}: {targets}")
        
    # 6. Run Simulation
    SIMULATION_EPOCHS = 100
    print(f"\nRunning simulation for {SIMULATION_EPOCHS} epochs...")
    for epoch in range(SIMULATION_EPOCHS):
        sim.step()
        
    # 7. Collect and Print Statistics
    stats = StatsCollector(sim)
    stats.generate_report()
    
    # 8. Visualize
    vis = Visualizer(sim, node_positions)
    vis.animate('assignment_simulation.gif')

if __name__ == "__main__":
    main()
