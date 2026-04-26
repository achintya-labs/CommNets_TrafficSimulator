import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Visualizer:
    def __init__(self, simulator, node_positions):
        self.simulator = simulator
        self.node_positions = node_positions
        self.history = simulator.history
        self.colors = plt.cm.get_cmap('tab10')

    def _get_vehicle_color(self, destination):
        # Hash destination to a color index 0-9
        color_idx = hash(destination) % 10
        return self.colors(color_idx)

    def _get_road_coords(self, road_id):
        road = self.simulator.roads[road_id]
        x1, y1 = self.node_positions[road.source_node]
        x2, y2 = self.node_positions[road.dest_node]
        return np.array([x1, y1]), np.array([x2, y2])

    def animate(self, output_file='simulation.gif'):
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Draw roads (static background)
        for road_id, road in self.simulator.roads.items():
            p1, p2 = self._get_road_coords(road_id)
            
            # Draw an arrow for the road
            ax.annotate('', xy=p2, xytext=p1,
                        arrowprops=dict(arrowstyle="->", color="gray", lw=1.5, alpha=0.5))
            
        # Draw nodes
        for node_id, pos in self.node_positions.items():
            ax.plot(pos[0], pos[1], 'ko', markersize=10)
            ax.text(pos[0] + 0.1, pos[1] + 0.1, str(node_id), fontsize=12, fontweight='bold')
            
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title("Traffic Simulation")
        
        # Calculate limits based on nodes
        x_coords = [p[0] for p in self.node_positions.values()]
        y_coords = [p[1] for p in self.node_positions.values()]
        ax.set_xlim(min(x_coords) - 0.5, max(x_coords) + 0.5)
        ax.set_ylim(min(y_coords) - 0.5, max(y_coords) + 0.5)
        
        # Elements to update
        scatter = ax.scatter([], [], s=80, zorder=5)
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
        
        def init():
            scatter.set_offsets(np.empty((0, 2)))
            # Provide an empty (0, 4) array for RGBA colors
            scatter.set_facecolors(np.empty((0, 4)))
            time_text.set_text('')
            return scatter, time_text

        def update(frame_idx):
            state = self.history[frame_idx]
            time_text.set_text(f"Epoch: {state['epoch']}")
            
            if not state['vehicles']:
                scatter.set_offsets(np.empty((0, 2)))
                scatter.set_facecolors(np.empty((0, 4)))
                scatter.set_edgecolors(np.empty((0, 4)))
                return scatter, time_text
                
            positions = []
            colors = []
            
            for v_data in state['vehicles']:
                if 'road_id' in v_data:
                    p1, p2 = self._get_road_coords(v_data['road_id'])
                    # Linear interpolation based on progress
                    progress = v_data['progress']
                    
                    # Add a slight offset to the right of the road direction so opposite lanes don't overlap perfectly
                    direction = p2 - p1
                    length = np.linalg.norm(direction)
                    if length > 0:
                        normal = np.array([-direction[1], direction[0]]) / length
                        offset = normal * 0.05
                    else:
                        offset = np.array([0, 0])
                        
                    pos = p1 + (p2 - p1) * progress + offset
                    positions.append(pos)
                    colors.append(self._get_vehicle_color(v_data['destination']))
                elif 'node_id' in v_data:
                    # Vehicle waiting at a source node
                    pos = self.node_positions[v_data['node_id']]
                    # Add jitter to show multiple vehicles
                    pos = np.array(pos) + np.random.uniform(-0.1, 0.1, 2)
                    positions.append(pos)
                    colors.append(self._get_vehicle_color(v_data['destination']))
            
            scatter.set_offsets(np.array(positions))
            
            color_array = np.array(colors)
            scatter.set_facecolors(color_array)
            scatter.set_edgecolors(color_array)
            
            return scatter, time_text

        ani = animation.FuncAnimation(fig, update, frames=len(self.history),
                                      init_func=init, blit=True, interval=200)
        
        if output_file.endswith('.mp4'):
            ani.save(output_file, writer='ffmpeg', fps=5)
        else:
            ani.save(output_file, writer='pillow', fps=5)
            
        plt.close(fig)
        print(f"Animation saved to {output_file}")
