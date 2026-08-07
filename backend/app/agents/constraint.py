import logging
import json
from typing import List, Dict, Any
from backend.app.models import Stop, Vehicle, Package
from backend.app.core.ai_adapter import ai_service

logger = logging.getLogger("constraint_agent")

class ConstraintAgent:
    def __init__(self):
        pass
        
    async def run(
        self, 
        optimized_stops: List[Dict[str, Any]], 
        vehicle: Vehicle, 
        packages: List[Package],
        max_cod_amount: float = 50000.0,
        max_working_hours: float = 8.0
    ) -> Dict[str, Any]:
        """
        Validate optimized route sequence against hard and soft constraints.
        Returns validation report with list of violations.
        """
        logger.info(f"Constraint Agent validating sequence of {len(optimized_stops)} stops...")
        
        violations = []
        recommendations = []
        
        # 1. Capacity Check
        total_weight = sum(pkg.weight for pkg in packages)
        if total_weight > vehicle.capacity:
            violations.append(
                f"Capacity limit exceeded: Total package weight ({total_weight:.2f} kg) "
                f"exceeds vehicle capacity ({vehicle.capacity:.2f} kg)."
            )
            recommendations.append("Reduce the stop packages or assign a vehicle with higher capacity.")
            
        # 2. COD Limit Check (Indian regulations limit cash collections per driver/route)
        total_cod = sum(pkg.cod_amount for pkg in packages if pkg.cod_amount is not None)
        if total_cod > max_cod_amount:
            violations.append(
                f"COD Limit exceeded: Total collections ({total_cod:.2f} INR) "
                f"exceeds maximum allowed driver cash collection ({max_cod_amount:.2f} INR)."
            )
            recommendations.append("Reschedule high COD package deliveries or assign multi-driver dispatch.")
            
        # 3. Use AI to inspect soft constraints like Indian Zone Rules, local restrictions, and low bridge clearances.
        prompt = f"""
        Inspect the route details for soft constraints:
        - Indian Zone Rules (e.g. state-border checkpoints, urban commercial entry restrictions)
        - Local street clearances (low bridge heights, restricted commercial entry timings)
        
        Route details:
        Stops coordinates: {[{"stop_id": s["stop_id"], "lat": s["latitude"], "lng": s["longitude"]} for s in optimized_stops]}
        Vehicle type: {vehicle.vehicle_type}
        Total cargo weight: {total_weight:.2f} kg
        Total COD collection: {total_cod:.2f} INR
        
        Are there any regional or local entry restrictions? 
        If yes, list them.
        If no, return an empty list of violations.
        
        Return response in JSON matching this schema:
        {{
            "violations": ["list of soft violation strings"],
            "recommendations": ["list of recommendation strings"]
        }}
        """
        
        try:
            ai_response = await ai_service.generate_text(
                prompt=prompt,
                system_instruction="You are RouteMind Constraint Agent, specializing in regional logistics compliance.",
                json_mode=True
            )
            res = json.loads(ai_response)
            violations.extend(res.get("violations", []))
            recommendations.extend(res.get("recommendations", []))
        except Exception as e:
            logger.warning(f"AI soft constraint check failed: {e}")
            
        is_valid = len(violations) == 0
        
        return {
            "is_valid": is_valid,
            "violations": violations,
            "recommendations": recommendations,
            "total_weight_kg": total_weight,
            "total_cod_inr": total_cod
        }
