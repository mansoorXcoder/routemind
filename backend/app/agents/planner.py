import logging
from typing import List, Dict, Any
from backend.app.models import Stop, Vehicle, Package
from backend.app.optimization.solver import ORToolsVRPSolver
from backend.app.core.ai_adapter import ai_service

logger = logging.getLogger("planner_agent")

class PlannerAgent:
    def __init__(self):
        pass
        
    async def run(self, stops: List[Stop], vehicle: Vehicle, packages: List[Package]) -> Dict[str, Any]:
        """
        Runs OR-Tools solver to get mathematically optimized route sequence,
        then uses LLM for post-optimization layout analysis.
        """
        logger.info(f"Planner Agent running VRP solver for vehicle {vehicle.vehicle_number}...")
        
        # 1. Classical optimization run
        solver = ORToolsVRPSolver(stops, vehicle, packages)
        solver_result = solver.solve()
        
        if not solver_result["success"]:
            return solver_result
            
        # 2. AI assessment of optimized sequence
        prompt = f"""
        Analyze the following optimized route sequence for vehicle capacity and travel time efficiency.
        
        Vehicle Capacity: {vehicle.capacity} kg
        Total Optimized Distance: {solver_result['total_distance_km']} km
        Total Transit Duration: {solver_result['total_time_min']} minutes
        Optimization Score: {solver_result['optimization_score']}
        
        Route stops sequence:
        {solver_result['optimized_stops']}
        
        Give a brief 2-sentence summary of the routing profile and confirm if the load distribution is balanced.
        Return response in JSON format matching this schema:
        {{
            "load_balance_ok": true/false,
            "routing_profile_summary": "profile text here"
        }}
        """
        
        try:
            ai_response = await ai_service.generate_text(
                prompt=prompt,
                system_instruction="You are RouteMind Planner Agent, a logistics AI that reviews route profiles.",
                json_mode=True
            )
            import json
            profile_data = json.loads(ai_response)
            solver_result.update(profile_data)
        except Exception as e:
            logger.warning(f"AI post-optimization analysis failed: {e}. Using fallback defaults.")
            solver_result["load_balance_ok"] = True
            solver_result["routing_profile_summary"] = "Route optimized via OR-Tools."
            
        return solver_result
