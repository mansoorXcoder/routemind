import logging
from typing import List, Dict, Any
from backend.app.models import Stop, Vehicle, Package

logger = logging.getLogger("validator_agent")

class ValidationAgent:
    def __init__(self):
        pass
        
    async def run(
        self,
        original_stops: List[Stop],
        optimized_stops_meta: List[Dict[str, Any]],
        vehicle: Vehicle,
        packages: List[Package]
    ) -> Dict[str, Any]:
        """
        Verify the integrity and quality of the optimized route sequence.
        """
        logger.info("Validation Agent verifying route optimization output...")
        
        status = "PASS"
        messages = []
        checks = {
            "duplicate_stops": True,
            "stops_count_match": True,
            "capacity_valid": True,
            "route_loops_hub": True
        }
        
        # 1. Check for Duplicate Stops
        stop_ids = [s["stop_id"] for s in optimized_stops_meta]
        if len(stop_ids) != len(set(stop_ids)):
            status = "FAIL"
            checks["duplicate_stops"] = False
            messages.append("Duplicate stop IDs found in optimized route sequence!")
            
        # 2. Check for Stops Count Match
        # The optimized_stops_meta will contain the stops.
        # Note: If it's a dynamic replan, it might contain a new stop, so we check accordingly
        # But for regular optimization, count should match.
        if len(optimized_stops_meta) < len(original_stops):
            status = "WARNING"
            checks["stops_count_match"] = False
            messages.append(
                f"Optimized route contains fewer stops ({len(optimized_stops_meta)}) "
                f"than original stops ({len(original_stops)})."
            )
            
        # 3. Check Capacity
        total_weight = sum(pkg.weight for pkg in packages)
        if total_weight > vehicle.capacity:
            status = "WARNING"
            checks["capacity_valid"] = False
            messages.append(
                f"Cargo weight ({total_weight:.2f} kg) exceeds vehicle capacity ({vehicle.capacity:.2f} kg)."
            )
            
        # 4. Check Hub loop
        # The first stop in the sequence should usually be a hub
        if optimized_stops_meta and optimized_stops_meta[0]["stop_type"] != "hub":
            status = "WARNING"
            checks["route_loops_hub"] = False
            messages.append("Optimized route sequence does not start at the hub depot.")
            
        if not messages:
            messages.append("All integrity checks passed. Optimized sequence is valid.")
            
        return {
            "status": status,
            "checks": checks,
            "messages": messages
        }
