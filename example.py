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
        'N0': (0, 1),
        'N1': (1, 1),
        'N2': (2, 1),
        'N3': (1, 0),
        'N4': (3, 1),
        'N5': (1, 2)
    }
    
    # Add Junctions
    sim.add_junction(Junction('N0'))
    sim.add_junction(Junction('N1', strategy=RoundRobinStrategy()))
    sim.add_junction(Junction('N2', strategy=RoundRobinStrategy()))
    sim.add_junction(Junction('N3', strategy=RoundRobinStrategy()))
    sim.add_junction(Junction('N4'))
    sim.add_junction(Junction('N5'))

    # Add Sinks
    sim.add_sink(Sink('N4'))
    sim.add_sink(Sink('N3')) # N2 also acts as a sink for some traffic
    sim.add_sink(Sink('N5')) # N2 also acts as a sink for some traffic

    # 3. Add Roads (id, src, dst, length, max_speed, capacity)
    sim.add_road(Road('R_0_1', 'N0', 'N1', length=10, max_speed=5, capacity=5))
    sim.add_road(Road('R_1_3', 'N1', 'N3', length=10, max_speed=2, capacity=5))
    sim.add_road(Road('R_1_5', 'N1', 'N5', length=10, max_speed=2, capacity=5))
    sim.add_road(Road('R_3_2', 'N3', 'N2', length=14, max_speed=5, capacity=5))
    sim.add_road(Road('R_2_4', 'N2', 'N4', length=10, max_speed=5, capacity=5))
    
    # 4. Add Traffic Sources
    sim.add_source(TrafficSource('N0', 'N4', generator=BernoulliGenerator(0.1)))
    sim.add_source(TrafficSource('N0', 'N3', generator=PoissonGenerator(0.1)))
    sim.add_source(TrafficSource('N0', 'N5', generator=PoissonGenerator(0.1)))

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
    vis.animate('example_simulation.gif')

if __name__ == "__main__":
    main()
