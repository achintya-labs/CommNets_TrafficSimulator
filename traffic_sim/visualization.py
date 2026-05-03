import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Visualizer:
    def __init__(self, simulator, node_positions):
        self.simulator = simulator
        self.node_positions = node_positions
        self.history = simulator.history
        self.colors = plt.cm.get_cmap('hsv')
        self.dest_colors = {}

    def _get_vehicle_color(self, destination):
        # Deterministically map each destination to a unique color using golden ratio spacing in the HSV spectrum
        if destination not in self.dest_colors:
            self.dest_colors[destination] = len(self.dest_colors)
        
        # 0.618033988749895 is the conjugate of the golden ratio
        h = (self.dest_colors[destination] * 0.618033988749895) % 1.0
        return self.colors(h)

    def _get_road_coords(self, road_id):
        road = self.simulator.roads[road_id]
        x1, y1 = self.node_positions[road.source_node]
        x2, y2 = self.node_positions[road.dest_node]
        return np.array([x1, y1]), np.array([x2, y2])

    def _get_vehicle_pos_color(self, v_data):
        if 'road_id' in v_data:
            p1, p2 = self._get_road_coords(v_data['road_id'])
            progress = v_data['progress']
            direction = p2 - p1
            length = np.linalg.norm(direction)
            if length > 0:
                normal = np.array([-direction[1], direction[0]]) / length
                offset = normal * 0.05
            else:
                offset = np.array([0, 0])
            pos = p1 + (p2 - p1) * progress + offset
            color = self._get_vehicle_color(v_data['destination'])
            return pos, color
        elif 'node_id' in v_data:
            pos = self.node_positions[v_data['node_id']]
            h = hash(str(v_data['id']) + "jitter")
            jitter_x = ((h % 100) / 100.0) * 0.2 - 0.1
            jitter_y = (((h // 100) % 100) / 100.0) * 0.2 - 0.1
            pos = np.array(pos) + np.array([jitter_x, jitter_y])
            color = self._get_vehicle_color(v_data['destination'])
            return pos, color
        return np.array([0, 0]), self._get_vehicle_color(v_data['destination'])

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

        steps_per_epoch = 10
        total_frames = max(1, (len(self.history) - 1) * steps_per_epoch)
        fps = 30
        interval = 1000 // fps

        cache = {'epoch': -1, 'pos0': {}, 'pos1': {}}

        def update(frame):
            if frame % 5 == 0 or frame == total_frames - 1:
                progress = (frame + 1) / total_frames
                bar_len = 40
                filled = int(bar_len * progress)
                bar = '=' * filled + '-' * (bar_len - filled)
                print(f"\rRendering animation: [{bar}] {frame+1}/{total_frames} frames ({progress*100:.1f}%)", end="", flush=True)

            epoch_idx = frame // steps_per_epoch
            alpha = (frame % steps_per_epoch) / steps_per_epoch
            
            if epoch_idx >= len(self.history):
                epoch_idx = len(self.history) - 1
                alpha = 0.0
                
            next_idx = min(epoch_idx + 1, len(self.history) - 1)
            
            state0 = self.history[epoch_idx]
            state1 = self.history[next_idx]
            
            time_text.set_text(f"Epoch: {state0['epoch']} + {alpha:.1f}")
            
            if cache['epoch'] != epoch_idx:
                cache['epoch'] = epoch_idx
                cache['pos0'] = {}
                for v_data in state0['vehicles']:
                    pos, color = self._get_vehicle_pos_color(v_data)
                    cache['pos0'][v_data['id']] = (pos, color, v_data)
                    
                cache['pos1'] = {}
                for v_data in state1['vehicles']:
                    pos, color = self._get_vehicle_pos_color(v_data)
                    cache['pos1'][v_data['id']] = (pos, color, v_data)
                    
            pos0_dict = cache['pos0']
            pos1_dict = cache['pos1']
            
            positions = []
            colors = []
            
            all_vids = set(pos0_dict.keys()) | set(pos1_dict.keys())
            
            for vid in all_vids:
                if vid in pos0_dict and vid in pos1_dict:
                    pos0, color, _ = pos0_dict[vid]
                    pos1, _, _ = pos1_dict[vid]
                    pos = pos0 * (1 - alpha) + pos1 * alpha
                    positions.append(pos)
                    colors.append(color)
                elif vid in pos0_dict:
                    # Vehicle reached sink
                    pos0, color, v_data = pos0_dict[vid]
                    sink_pos = self.node_positions[v_data['destination']]
                    pos = pos0 * (1 - alpha) + np.array(sink_pos) * alpha
                    positions.append(pos)
                    colors.append(color)
                elif vid in pos1_dict:
                    # Vehicle just appeared
                    pos1, color, v_data = pos1_dict[vid]
                    source_pos = self.node_positions[v_data['source']]
                    pos = np.array(source_pos) * (1 - alpha) + pos1 * alpha
                    positions.append(pos)
                    colors.append(color)
            
            if not positions:
                scatter.set_offsets(np.empty((0, 2)))
                scatter.set_facecolors(np.empty((0, 4)))
                scatter.set_edgecolors(np.empty((0, 4)))
                return scatter, time_text

            scatter.set_offsets(np.array(positions))
            
            color_array = np.array(colors)
            scatter.set_facecolors(color_array)
            scatter.set_edgecolors(color_array)
            
            return scatter, time_text

        ani = animation.FuncAnimation(fig, update, frames=total_frames,
                                      init_func=init, blit=True, interval=interval)
        
        if output_file.endswith('.mp4'):
            ani.save(output_file, writer='ffmpeg', fps=fps)
        else:
            ani.save(output_file, writer='pillow', fps=fps)
            
        plt.close(fig)
        print() # Newline after the progress bar finishes
        print(f"Animation saved to {output_file}")
