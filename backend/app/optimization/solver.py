import logging
import math
from typing import List, Dict, Any, Tuple
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from backend.app.models import Stop, Vehicle, Package

logger = logging.getLogger("vrp_solver")

def calculate_haversine_travel_time(lat1: float, lng1: float, lat2: float, lng2: float, speed_kmh: float = 30.0) -> Tuple[float, float]:
    """
    Calculate distance (km) and travel time (seconds) between two points
    using the Haversine formula and average transit speed.
    """
    if lat1 == lat2 and lng1 == lng2:
        return 0.0, 0.0
        
    R = 6371.0  # Earth's radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    # time = distance / speed
    travel_time_sec = (distance / speed_kmh) * 3600.0
    return distance, travel_time_sec

class ORToolsVRPSolver:
    def __init__(self, stops: List[Stop], vehicle: Vehicle, packages: List[Package]):
        self.stops = sorted(stops, key=lambda s: s.sequence)
        self.vehicle = vehicle
        self.packages = packages
        
    def build_matrices(self) -> Tuple[List[List[int]], List[int], List[Tuple[int, int]]]:
        """
        Build distance/time matrix, demands list, and time windows list.
        All times are in seconds relative to departure (t=0).
        """
        n = len(self.stops)
        time_matrix = [[0] * n for _ in range(n)]
        
        # 1. Build Time/Distance Matrix using coordinates
        for i in range(n):
            for j in range(n):
                if i == j:
                    time_matrix[i][j] = 0
                else:
                    _, travel_time_sec = calculate_haversine_travel_time(
                        self.stops[i].latitude, self.stops[i].longitude,
                        self.stops[j].latitude, self.stops[j].longitude
                    )
                    time_matrix[i][j] = int(travel_time_sec)
                    
        # 2. Demands (weights of packages for each stop)
        # Sequence 0 is always the hub (no demand)
        demands = [0] * n
        for pkg in self.packages:
            # Match package to stop index
            for idx, stop in enumerate(self.stops):
                if pkg.stop_id == stop.id:
                    # Weight in kg
                    demands[idx] += int(pkg.weight)
                    break
                    
        # 3. Time Windows (relative to start time in seconds)
        # Hub is at t=0, open for the entire day (e.g. 0 to 24h)
        time_windows = [(0, 86400)] * n
        
        for idx, stop in enumerate(self.stops):
            if stop.stop_type == "hub":
                time_windows[idx] = (0, 86400)
                continue
                
            # If explicit delivery windows exist, use them
            if stop.delivery_window_start and stop.delivery_window_end:
                # Convert datetime to seconds from midnight or relative to route date
                # For demo, use mock values if it cannot be converted easily
                start_sec = int((stop.delivery_window_start - stop.delivery_window_start.replace(hour=0, minute=0, second=0)).total_seconds())
                end_sec = int((stop.delivery_window_end - stop.delivery_window_start.replace(hour=0, minute=0, second=0)).total_seconds())
                time_windows[idx] = (start_sec, end_sec)
            else:
                # Default 9 AM - 6 PM delivery window (relative to t=0 being 8 AM, for example)
                # Let's say: 9 hours to 18 hours
                time_windows[idx] = (3600 * 9, 3600 * 18)
                
        return time_matrix, demands, time_windows

    def solve(self) -> Dict[str, Any]:
        """
        Solve VRP for the given stops and vehicle capacity.
        Returns optimized sequence of stops and metadata.
        """
        if not self.stops:
            return {"success": False, "error": "No stops found"}
            
        time_matrix, demands, time_windows = self.build_matrices()
        
        # Create routing index manager
        # 1 vehicle, start and end at sequence 0 (hub)
        manager = pywrapcp.RoutingIndexManager(len(self.stops), 1, 0)
        routing = pywrapcp.RoutingModel(manager)
        
        # Create and register transit callback (travel times)
        def travel_time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return time_matrix[from_node][to_node]
            
        transit_callback_index = routing.RegisterTransitCallback(travel_time_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Add Capacity Constraint
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return demands[from_node]
            
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        capacity = int(self.vehicle.capacity) if self.vehicle.capacity > 0 else 500  # Default 500kg
        
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            [capacity],  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity"
        )
        
        # Add Time Window Constraint
        routing.AddDimension(
            transit_callback_index,
            30 * 60,  # 30 mins waiting time allowed
            86400,  # maximum time per vehicle (24h)
            False,  # Don't force start cumul to zero
            "Time"
        )
        time_dimension = routing.GetDimensionOrDie("Time")
        for node_idx, (start, end) in enumerate(time_windows):
            index = manager.NodeToIndex(node_idx)
            time_dimension.CumulVar(index).SetRange(start, end)
            
        # Set search parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        
        # Solve
        solution = routing.SolveWithParameters(search_parameters)
        
        if not solution:
            logger.error("No solution found by OR-Tools solver!")
            return {"success": False, "error": "No solution found"}
            
        # Extract route
        index = routing.Start(0)
        route_sequence = []
        total_time = 0
        total_distance = 0.0
        
        previous_node = None
        while not routing.IsEnd(index):
            node_idx = manager.IndexToNode(index)
            route_sequence.append(node_idx)
            
            if previous_node is not None:
                total_time += time_matrix[previous_node][node_idx]
                dist, _ = calculate_haversine_travel_time(
                    self.stops[previous_node].latitude, self.stops[previous_node].longitude,
                    self.stops[node_idx].latitude, self.stops[node_idx].longitude
                )
                total_distance += dist
                
            previous_node = node_idx
            index = solution.Value(routing.NextVar(index))
            
        # Add final leg back to hub
        node_idx = manager.IndexToNode(index)
        route_sequence.append(node_idx)
        if previous_node is not None:
            total_time += time_matrix[previous_node][node_idx]
            dist, _ = calculate_haversine_travel_time(
                self.stops[previous_node].latitude, self.stops[previous_node].longitude,
                self.stops[node_idx].latitude, self.stops[node_idx].longitude
            )
            total_distance += dist
            
        # Map back to Stop sequence
        optimized_stops = []
        for seq_id, stop_idx in enumerate(route_sequence[:-1]):
            stop = self.stops[stop_idx]
            optimized_stops.append({
                "stop_id": str(stop.id),
                "original_sequence": stop.sequence,
                "new_sequence": seq_id,
                "customer_name": stop.customer_name,
                "latitude": stop.latitude,
                "longitude": stop.longitude,
                "stop_type": stop.stop_type
            })
            
        # Calculate optimization score (percentage of savings or based on travel efficiency)
        # For mock score, base it on path length compared to original order
        orig_time = sum(time_matrix[i][i+1] for i in range(len(self.stops)-1)) + time_matrix[-1][0] if len(self.stops) > 1 else 0
        savings = max(0, orig_time - total_time)
        score = min(100, max(70, int(100 - (total_time / max(1, orig_time)) * 30))) if orig_time > 0 else 100
        
        return {
            "success": True,
            "optimized_stops": optimized_stops,
            "total_distance_km": round(total_distance, 2),
            "total_time_min": round(total_time / 60.0, 2),
            "optimization_score": float(score)
        }
