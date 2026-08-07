import logging
from typing import List, Dict, Any, Optional
from backend.app.models import Stop, Vehicle, Package
from backend.app.optimization.solver import ORToolsVRPSolver, calculate_haversine_travel_time

logger = logging.getLogger("replanning_agent")

class ReplanningAgent:
    def __init__(self):
        pass
        
    async def run(
        self,
        current_stops: List[Stop],
        vehicle: Vehicle,
        packages: List[Package],
        event_type: str,
        event_details: Dict[str, Any],
        current_stop_index: int = 0
    ) -> Dict[str, Any]:
        """
        Replans the route by freezing completed stops and optimizing the sequence
        of the remaining unvisited stops.
        """
        logger.info(f"Replanning Agent triggered by {event_type} at stop index {current_stop_index}...")
        
        # 1. Separate completed/active stops from remaining stops
        # Sort stops by current sequence
        sorted_stops = sorted(current_stops, key=lambda s: s.sequence)
        
        completed_stops = sorted_stops[:current_stop_index + 1]
        remaining_stops = sorted_stops[current_stop_index + 1:]
        
        if not remaining_stops:
            return {
                "success": False,
                "error": "No remaining stops left to replan."
            }
            
        # 2. Adjust remaining stops based on event type
        # For a new pickup event, add the new stop to the remaining pool
        new_stop_added = None
        if event_type == "new_pickup":
            new_stop_details = event_details.get("stop", {})
            if new_stop_details:
                # Create a temporary Stop object
                import uuid
                # Use a dummy ID for the temporary stop
                dummy_id = uuid.uuid4()
                new_stop_added = Stop(
                    id=dummy_id,
                    route_id=sorted_stops[0].route_id,
                    sequence=999,  # temporary large sequence
                    customer_name=new_stop_details.get("customer_name", "New Pickup"),
                    address=new_stop_details.get("address", "New Location"),
                    latitude=new_stop_details.get("latitude"),
                    longitude=new_stop_details.get("longitude"),
                    stop_type="pickup",
                    status="pending"
                )
                remaining_stops.append(new_stop_added)
                
                # Add package if provided
                new_pkg_details = event_details.get("package", {})
                if new_pkg_details:
                    new_pkg = Package(
                        tracking_number=new_pkg_details.get("tracking_number", f"PKG-PICKUP-{random.randint(1000, 9999)}"),
                        route_id=sorted_stops[0].route_id,
                        stop_id=dummy_id,
                        weight=new_pkg_details.get("weight", 2.0),
                        volume=new_pkg_details.get("volume", 0.01),
                        cod_amount=new_pkg_details.get("cod_amount", 0.0),
                        status="pending"
                    )
                    packages.append(new_pkg)
                    
        # For traffic or road closure, we can simulate congestion by shifting travel times.
        # This will be handled in the solver because it recalculates using the coordinates.
        # If the road closure is on a specific coordinate, we can bypass that stop or increase distance.
        
        # 3. We run the ORToolsVRPSolver on the remaining stops.
        # To do this correctly, the start point of the VRP solver is the driver's current stop (the last completed stop)
        # and it returns the sequence starting from there.
        # Let's set the first stop in our VRP solver list to be the last completed stop (depot/current position).
        # We must change its type temporarily to 'hub' so the solver treats it as start depot.
        start_point = completed_stops[-1]
        orig_type = start_point.stop_type
        start_point.stop_type = "hub"  # Temporarily treat as hub/start point
        
        replan_stops_pool = [start_point] + remaining_stops
        
        solver = ORToolsVRPSolver(replan_stops_pool, vehicle, packages)
        solver_res = solver.solve()
        
        # Restore original stop type
        start_point.stop_type = orig_type
        
        if not solver_res["success"]:
            return solver_res
            
        # 4. Reconstruct the entire route sequence: completed_stops + newly optimized remaining_stops
        optimized_rem_stops_meta = solver_res["optimized_stops"]
        # The VRP solver starts with index 0 (which is start_point / completed_stops[-1]).
        # We should skip the first element in optimized_rem_stops_meta as it is already in completed_stops[-1].
        new_remaining_sequence = optimized_rem_stops_meta[1:]
        
        final_sequence = []
        # Add completed stops
        for s_idx, c_stop in enumerate(completed_stops):
            final_sequence.append({
                "stop_id": str(c_stop.id),
                "original_sequence": c_stop.sequence,
                "new_sequence": s_idx,
                "customer_name": c_stop.customer_name,
                "latitude": c_stop.latitude,
                "longitude": c_stop.longitude,
                "stop_type": c_stop.stop_type,
                "status": c_stop.status
            })
            
        # Add replanned stops
        start_seq = len(completed_stops)
        for r_stop_meta in new_remaining_sequence:
            # Look up stop details
            stop_id = r_stop_meta["stop_id"]
            orig_seq = r_stop_meta["original_sequence"]
            
            # Find in remaining_stops
            stop_obj = None
            for r_s in remaining_stops:
                if str(r_s.id) == stop_id:
                    stop_obj = r_s
                    break
            
            final_sequence.append({
                "stop_id": stop_id,
                "original_sequence": orig_seq,
                "new_sequence": start_seq,
                "customer_name": r_stop_meta["customer_name"],
                "latitude": r_stop_meta["latitude"],
                "longitude": r_stop_meta["longitude"],
                "stop_type": r_stop_meta["stop_type"],
                "status": "pending",
                "is_replanned": True
            })
            start_seq += 1
            
        return {
            "success": True,
            "optimized_stops": final_sequence,
            "total_distance_km": solver_res["total_distance_km"],
            "total_time_min": solver_res["total_time_min"],
            "optimization_score": solver_res["optimization_score"],
            "changed_stops_count": len(new_remaining_sequence),
            "new_pickup_added": new_stop_added is not None
        }
