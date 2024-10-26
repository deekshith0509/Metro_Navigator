

import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering
import matplotlib.pyplot as plt

from collections import defaultdict
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import os
from .models import Station, Connection

class PathSegment:
    def __init__(self, station, time, distance):
        self.station = station
        self.time = time
        self.distance = distance

class MetroService:
    def __init__(self):
        self._initialize_graph()

    def _initialize_graph(self):
        self.metro_map = defaultdict(list)
        self.stations = {station.name: station for station in Station.objects.all()}
        
        connections = Connection.objects.select_related('from_station', 'to_station').all()
        for conn in connections:
            self.metro_map[conn.from_station.name].append(
                PathSegment(conn.to_station.name, conn.time, conn.distance)
            )
            self.metro_map[conn.to_station.name].append(
                PathSegment(conn.from_station.name, conn.time, conn.distance)
            )

    def find_path(self, source, destination, mode='time'):
        if source not in self.stations or destination not in self.stations:
            return None, "Invalid station names."

        distances, paths = self._dijkstra(source, destination, mode)
        
        if destination not in distances:
            return None, "No path found."

        path = self._reconstruct_path(paths, source, destination)
        journey_details = self._get_journey_details(path, mode)
        
        return journey_details, None

    def _dijkstra(self, source, destination, mode):
        distances = {source: 0}
        paths = {source: None}
        queue = [(0, source)]
        
        while queue:
            current_cost, current_station = heapq.heappop(queue)
            
            if current_station == destination:
                break
                
            if current_cost > distances[current_station]:
                continue
                
            for segment in self.metro_map[current_station]:
                cost = current_cost + getattr(segment, mode)
                
                if segment.station not in distances or cost < distances[segment.station]:
                    distances[segment.station] = cost
                    paths[segment.station] = current_station
                    heapq.heappush(queue, (cost, segment.station))
        
        return distances, paths

    def _reconstruct_path(self, paths, source, destination):
        path = []
        current = destination
        
        while current is not None:
            path.append(current)
            current = paths.get(current)
            
        return list(reversed(path))

    def _get_journey_details(self, path, mode):
        journey_details = []
        total_distance = 0
        total_time = 0
        
        for i in range(len(path) - 1):
            from_station = path[i]
            to_station = path[i + 1]
            
            segment = next(
                seg for seg in self.metro_map[from_station] 
                if seg.station == to_station
            )
            
            journey_details.append({
                'from': from_station,
                'to': to_station,
                'distance': segment.distance,
                'time': segment.time,
                'from_line': self.stations[from_station].line_color,
                'to_line': self.stations[to_station].line_color,
                'is_interchange': (
                    self.stations[from_station].line_color != 
                    self.stations[to_station].line_color
                )
            })
            
            total_distance += segment.distance
            total_time += segment.time
        
        return {
            'journey_details': journey_details,
            'total_distance': total_distance,
            'total_time': total_time,
            'path': path,
            'num_interchanges': sum(
                1 for detail in journey_details if detail['is_interchange']
            )
        }


    def get_node_positions(self):
        # Define scale factors for x and y axes
        scale_x = 1
        scale_y = 2

        # Define positions for nodes

        return {
            'Ameerpet': (6 * scale_x, 11 * scale_y),
            'Assembly': (8 * scale_x, 6 * scale_y),
            'Balanagar': (2 * scale_x, 17 * scale_y),
            'Begumpet': (8 * scale_x, 12 * scale_y),
            'Bharatnagar': (2 * scale_x, 15 * scale_y),
            'Chaitanyapuri': (15 * scale_x, -3 * scale_y),
            'Chikkadpally': (12 * scale_x, 6 * scale_y),
            'Dilsukhnagar': (15 * scale_x, -2 * scale_y),
            'Durgam Cheruvu': (2 * scale_x, 2 * scale_y),
            'ESI Hospital': (4 * scale_x, 13 * scale_y),
            'Erragadda': (3 * scale_x, 14 * scale_y),
            'Errum Manzil': (7 * scale_x, 9 * scale_y),
            'Gandhi Bhavan': (10 * scale_x, 4 * scale_y),
            'Gandhi Hospital': (12 * scale_x, 9 * scale_y),
            'Habsiguda': (16 * scale_x, 8 * scale_y),
            'Hitec City': (1 * scale_x, 1 * scale_y),
            'JBS Parade Ground': (12 * scale_x, 11 * scale_y),
            'JNTU College': (1 * scale_x, 20 * scale_y),
            'Jubilee Hills Check Post': (2 * scale_x, 5 * scale_y),
            'Jubilee Hills Road No 5': (3 * scale_x, 6 * scale_y),
            'KPHB Colony': (2 * scale_x, 19 * scale_y),
            'Khairatabad': (7 * scale_x, 8 * scale_y),
            'Kukatpally': (2 * scale_x, 18 * scale_y),
            'LB Nagar': (17 * scale_x, -5 * scale_y),
            'Lakdi-Ka-Pul': (7 * scale_x, 7 * scale_y),
            'MG Bus Station': (12 * scale_x, 2 * scale_y),
            'Madhapur': (2 * scale_x, 3 * scale_y),
            'Madhura Nagar': (3.5 * scale_x, 9.4 * scale_y),
            'Malakpet': (13 * scale_x, 1 * scale_y),
            'Mettuguda': (14 * scale_x, 11 * scale_y),
            'Miyapur': (0 * scale_x, 21 * scale_y),
            'Moosapet': (2 * scale_x, 16 * scale_y),
            'Musarambagh': (15 * scale_x, -1 * scale_y),
            'Musheerabad': (12 * scale_x, 8 * scale_y),
            'NGRI': (17 * scale_x, 7 * scale_y),
            'Nagole': (20 * scale_x, 4 * scale_y),
            'Nampally': (9 * scale_x, 5 * scale_y),
            'Narayanguda': (12 * scale_x, 5 * scale_y),
            'New Market': (14 * scale_x, 0 * scale_y),
            'Osmania Medical College': (10 * scale_x, 2.5 * scale_y),
            'Paradise': (11 * scale_x, 12.5 * scale_y),
            'Peddamma Temple': (2 * scale_x, 4 * scale_y),
            'Prakash Nagar': (9 * scale_x, 11 * scale_y),
            'Punjagutta': (7 * scale_x, 10 * scale_y),
            'RTC Cross Roads': (12 * scale_x, 7 * scale_y),
            'Raidurg': (0 * scale_x, 0 * scale_y),
            'Rasoolpura': (10 * scale_x, 12 * scale_y),
            'SR Nagar': (5 * scale_x, 12 * scale_y),
            'Secunderabad East': (13 * scale_x, 12 * scale_y),
            'Secunderabad West': (12 * scale_x, 10 * scale_y),
            'Stadium': (18 * scale_x, 6 * scale_y),
            'Sultan Bazaar': (12 * scale_x, 4 * scale_y),
            'Tarnaka': (15 * scale_x, 10 * scale_y),
            'Uppal': (19 * scale_x, 5 * scale_y),
            'Victoria Memorial': (16 * scale_x, -4 * scale_y),
            'Yousufguda': (3 * scale_x, 7.3 * scale_y),
        }

    def visualize_metro_map(self, source, destination, current_mode):
        try:
            G = nx.Graph()

            # Define node colors based on metro lines
            line_colors = {
                'red': {'Miyapur', 'JNTU College', 'KPHB Colony', 'Kukatpally', 'Balanagar', 'Moosapet',
                         'Bharatnagar', 'Erragadda', 'ESI Hospital', 'SR Nagar', 'Ameerpet',
                         'Punjagutta', 'Errum Manzil', 'Khairatabad', 'Lakdi-Ka-Pul', 'Assembly',
                         'Nampally', 'Gandhi Bhavan', 'Osmania Medical College', 'MG Bus Station',
                         'Malakpet', 'New Market', 'Musarambagh', 'Dilsukhnagar', 'Chaitanyapuri',
                         'Victoria Memorial', 'LB Nagar'},
                'blue': {'Raidurg', 'Hitec City', 'Durgam Cheruvu', 'Madhapur', 'Peddamma Temple',
                          'Jubilee Hills Check Post', 'Jubilee Hills Road No 5', 'Yousufguda',
                          'Madhura Nagar', 'Ameerpet', 'Begumpet', 'Prakash Nagar', 'Rasoolpura',
                          'Paradise', 'JBS Parade Ground', 'Secunderabad East', 'Mettuguda',
                          'Tarnaka', 'Habsiguda', 'NGRI', 'Stadium', 'Uppal', 'Nagole'},
                'green': {'JBS Parade Ground', 'Secunderabad West', 'Gandhi Hospital', 'Musheerabad',
                           'RTC Cross Roads', 'Chikkadpally', 'Narayanguda', 'Sultan Bazaar',
                           'MG Bus Station'},
                'interchange': {'MG Bus Station', 'JBS Parade Ground', 'Ameerpet'}
            }
            # Add edges to the graph and set node colors
            for station, neighbors in self.metro_map.items():
                for neighbor in neighbors:
                    weight = neighbor.distance if current_mode == 'distance' else neighbor.time
                    G.add_edge(station, neighbor.station, weight=weight, distance=neighbor.distance, time=neighbor.time)

            # Get node positions
            pos = self.get_node_positions()  # Assume this function is defined elsewhere

            # Ensure all nodes have positions; assign default if missing
            for node in G.nodes():
                if node not in pos:
                    print(f"Node '{node}' has no position, assigning default position.")
                    pos[node] = (0, 0)  # Assign a default position

            # Draw nodes with colors based on their respective metro lines
            node_colors = []
            for node in G.nodes():
                color = 'lightgray'  # Default color
                for line, stations in line_colors.items():
                    if node in stations:
                        color = line  # Assign the line color
                        break
                node_colors.append(color)

            # Draw all nodes and edges
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=50, edgecolors='black')
            nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray', width=1.5)

            # Find path from source to destination
            path_details, error_message = self.find_path(source, destination, mode=current_mode)

            # Adjust label positions to the right of the nodes
            labels = {node: node for node in G.nodes()}
            label_pos = {node: (x + 0.1, y) for node, (x, y) in pos.items()}  # Shift labels to the right
            nx.draw_networkx_labels(G, label_pos, labels, font_size=6, verticalalignment='center')

            # Create legend text using journey details
            if path_details:
                total_distance = path_details['total_distance']
                total_time = path_details['total_time']
                legend_text = f'Total Distance: {total_distance} m\nTotal Time: {total_time} min'
            else:
                legend_text = error_message if error_message else 'No journey details available.'

            plt.text(0.95, 0.95, legend_text, transform=plt.gca().transAxes, fontsize=10,
                     verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.8))

            plt.title('Metro Map Visualization')
            plt.axis('off')

            # Ensure the images directory exists
            images_dir = os.path.join('static', 'images')
            os.makedirs(images_dir, exist_ok=True)  # Create the directory if it doesn't exist

            # Save the visualization to a file
            visualization_path = os.path.join(images_dir, 'metro_map_visualization.png')
            plt.savefig(visualization_path, bbox_inches='tight', dpi=150)
            plt.close()

            return visualization_path  # Return the path to the saved image

        except Exception as e:
            import traceback
            traceback.print_exc()  # Print full stack trace for debugging
            return None  # Return None in case of an error


