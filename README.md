# CommNets Traffic Simulator

This project is a modular, discrete-time traffic simulator designed to model vehicle flow across a directional road network containing junctions, roads, sources, and sinks. It is capable of simulating complex routing behavior (using Dijkstra's algorithm) and queueing behavior, as well as visualizing the network traffic.

## Project Structure

The project is structured into modular libraries for ease of maintenance and extensibility.

### `traffic_sim/` (Core Library)
- **`core/`**: Contains the basic entities that make up the traffic simulation:
  - `vehicle.py`: The `Vehicle` class tracking source, destination, routing progress, and wait times.
  - `road.py`: The `Road` class defining properties like length, max speed, and capacity. It manages vehicles currently traveling as well as those queueing at the road's exit.
  - `sink.py`: The `Sink` class which absorbs vehicles once they reach their destination, finalizing their recorded statistics.
  - `traffic_source.py`: The `TrafficSource` class which dictates how vehicles enter the network.

- **`TrafficGeneratorDistribution/`**: Contains strategies for how frequently a source spawns new vehicles.
  - `base_generator.py`: An abstract base class for generators.
  - `bernoulli_generator.py`: Simulates independent probability per epoch (e.g. constant probability of generation).
  - `poisson_generator.py`: Simulates traffic using a Poisson distribution.

- **`junctions.py`**: Defines junctions and strategies for scheduling traffic passing through them (e.g., `RoundRobinStrategy`).

- **`simulator.py`**: The core event engine. It advances the simulation epoch by epoch, triggers vehicle generation, handles vehicle movements, and manages the routing tables computed via Dijkstra's shortest path.

- **`stats.py`**: A logging utility that generates a comprehensive post-simulation report showing throughput, average wait times, travel epochs, and road capacity utilization.

- **`visualization.py`**: Exports the history of the simulation into an animated `.gif` using Matplotlib, mapping node and road statuses step-by-step.

### Examples

- **`example.py`**: A fully working script demonstrating how to construct a network. It instantiates a planar network with several interconnected nodes, assigns `PoissonGenerator` and `BernoulliGenerator` sources, and kicks off a 100-epoch simulation. 
- **`example_simulation.gif`**: The output of `example.py`. It is a visual playback of the simulated epochs showing colored vehicles traversing the network and queuing appropriately.

## Usage

To configure and run your own specific network topology, you can use `example.py` as a blueprint. 

1. Define your nodes (e.g., `'N1': (x, y)`).
2. Connect them via `sim.add_road()` specifying `capacity` and `max_speed`.
3. Add your `TrafficSource`s parameterized with the desired generator.
4. Execute the Python script:
```bash
python3 example.py
```
