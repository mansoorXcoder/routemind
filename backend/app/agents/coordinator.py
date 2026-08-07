import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.app.models import Route, Stop, Vehicle, Package, Optimization, AIDecision
from backend.app.agents.planner import PlannerAgent
from backend.app.agents.constraint import ConstraintAgent
from backend.app.agents.event import EventAgent
from backend.app.agents.replanner import ReplanningAgent
from backend.app.agents.explainer import ExplainabilityAgent
from backend.app.agents.validator import ValidationAgent

logger = logging.getLogger("coordinator_agent")

class CoordinatorAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.constraint = ConstraintAgent()
        self.event_detector = EventAgent()
        self.replanner = ReplanningAgent()
        self.explainer = ExplainabilityAgent()
        self.validator = ValidationAgent()
        
    async def optimize_route(self, db: AsyncSession, route_id: str) -> Dict[str, Any]:
        """
        Runs the batch route optimization pipeline:
        OR-Tools (Planner) -> Constraints -> Validation -> Explanation -> Save Optimization (Pending)
        """
        logger.info(f"Coordinator: starting batch optimization for route {route_id}...")
        
        import uuid
        try:
            route_uuid = uuid.UUID(route_id)
        except ValueError:
            return {"success": False, "error": "Invalid route ID format."}
            
        # 1. Fetch route with stops and packages
        result = await db.execute(
            select(Route)
            .filter_by(id=route_uuid)
            .options(
                selectinload(Route.vehicle),
                selectinload(Route.driver),
                selectinload(Route.stops),
                selectinload(Route.packages)
            )
        )
        route = result.scalars().first()
        if not route:
            return {"success": False, "error": "Route not found."}
            
        vehicle = route.vehicle
        stops = route.stops
        packages = route.packages
        
        if not vehicle:
            return {"success": False, "error": "No vehicle assigned to this route."}
        if not stops:
            return {"success": False, "error": "No stops found on this route."}
            
        # Compile old route summary for comparison
        old_route_summary = {
            "distance_km": route.planned_distance,
            "duration_min": route.planned_duration,
            "stops_count": len(stops)
        }
        
        # 2. Run Planner (OR-Tools VRP + AI load balance check)
        planner_res = await self.planner.run(stops, vehicle, packages)
        if not planner_res["success"]:
            return planner_res
            
        optimized_stops = planner_res["optimized_stops"]
        
        # 3. Run Constraint check
        constraint_res = await self.constraint.run(optimized_stops, vehicle, packages)
        
        # 4. Run Validation check
        validation_res = await self.validator.run(stops, optimized_stops, vehicle, packages)
        
        # Compile new route summary
        new_route_summary = {
            "distance_km": planner_res["total_distance_km"],
            "duration_min": planner_res["total_time_min"],
            "stops_count": len(optimized_stops),
            "optimization_score": planner_res["optimization_score"]
        }
        
        # 5. Run Explainability
        explain_res = await self.explainer.run(old_route_summary, new_route_summary)
        
        # 6. Save Optimization Run (Pending Supervisor Approval)
        # Store stop sequences in old/new route JSON fields
        old_seq_list = sorted([{"stop_id": str(s.id), "sequence": s.sequence} for s in stops], key=lambda x: x["sequence"])
        new_seq_list = [{"stop_id": s["stop_id"], "sequence": s["new_sequence"]} for s in optimized_stops]
        
        optimization = Optimization(
            route_id=route.id,
            optimization_type="routing",
            algorithm="or-tools",
            old_route=old_seq_list,
            new_route=new_seq_list,
            distance_saved=explain_res["benefits"]["distance_saved_km"],
            time_saved=explain_res["benefits"]["time_saved_min"],
            fuel_saved=explain_res["benefits"]["fuel_saved_liters"],
            carbon_saved=explain_res["benefits"]["fuel_saved_liters"] * 2.68,  # 2.68kg CO2 per liter of diesel
            confidence=explain_res["confidence_score"],
            reason=explain_res["impact_summary"]
        )
        db.add(optimization)
        await db.flush()
        
        # Save AI Decision tracking details
        decision = AIDecision(
            route_id=route.id,
            decision="re_route",
            confidence=explain_res["confidence_score"],
            reason=explain_res["explanation"],
            llm_model="gemini-2.5-flash",
            execution_time=1.5,
            cost=0.001,
            approved=False  # Must be approved by supervisor
        )
        db.add(decision)
        await db.commit()
        
        return {
            "success": True,
            "optimization_id": str(optimization.id),
            "decision_id": str(decision.id),
            "old_summary": old_route_summary,
            "new_summary": new_route_summary,
            "optimized_stops": optimized_stops,
            "constraints": constraint_res,
            "validation": validation_res,
            "explanation": explain_res
        }
        
    async def replan_on_event(
        self,
        db: AsyncSession,
        route_id: str,
        event_type: str,
        event_details: Dict[str, Any],
        current_stop_index: int = 0
    ) -> Dict[str, Any]:
        """
        Runs the dynamic replanning pipeline when a real-time event is triggered:
        Event Detection -> Replanner -> Constraints -> Validation -> Explanation -> Save Optimization (Pending)
        """
        logger.info(f"Coordinator: running dynamic replan for route {route_id} due to {event_type}...")
        
        import uuid
        try:
            route_uuid = uuid.UUID(route_id)
        except ValueError:
            return {"success": False, "error": "Invalid route ID format."}
            
        # 1. Fetch route with stops and packages
        result = await db.execute(
            select(Route)
            .filter_by(id=route_uuid)
            .options(
                selectinload(Route.vehicle),
                selectinload(Route.driver),
                selectinload(Route.stops),
                selectinload(Route.packages)
            )
        )
        route = result.scalars().first()
        if not route:
            return {"success": False, "error": "Route not found."}
            
        vehicle = route.vehicle
        stops = route.stops
        packages = route.packages
        
        if not vehicle:
            return {"success": False, "error": "No vehicle assigned to this route."}
        if not stops:
            return {"success": False, "error": "No stops found on this route."}
            
        # Compile old route summary for comparison
        old_route_summary = {
            "distance_km": route.planned_distance,
            "duration_min": route.planned_duration,
            "stops_count": len(stops)
        }
        
        # 2. Run Event Detector Agent to assess impact
        event_res = await self.event_detector.run(
            event_type=event_type,
            details=event_details,
            route_info={"route_code": route.route_code, "stops_count": len(stops)}
        )
        
        if not event_res["replan_required"]:
            return {
                "success": True,
                "replan_required": False,
                "event_analysis": event_res,
                "message": "Event analyzed. No route replanning is required."
            }
            
        # 3. Run Replanning Agent to optimize remaining stops sequence
        replan_res = await self.replanner.run(
            current_stops=stops,
            vehicle=vehicle,
            packages=packages,
            event_type=event_type,
            event_details=event_details,
            current_stop_index=current_stop_index
        )
        
        if not replan_res["success"]:
            return replan_res
            
        optimized_stops = replan_res["optimized_stops"]
        
        # 4. Run Constraint check on new sequence
        constraint_res = await self.constraint.run(optimized_stops, vehicle, packages)
        
        # 5. Run Validation check on new sequence
        validation_res = await self.validator.run(stops, optimized_stops, vehicle, packages)
        
        # Compile new route summary
        new_route_summary = {
            "distance_km": replan_res["total_distance_km"],
            "duration_min": replan_res["total_time_min"],
            "stops_count": len(optimized_stops),
            "optimization_score": replan_res["optimization_score"]
        }
        
        # 6. Run Explainability comparing the change and the event trigger
        explain_res = await self.explainer.run(
            old_route_summary=old_route_summary,
            new_route_summary=new_route_summary,
            event_trigger=event_res
        )
        
        # 7. Save Optimization (Pending Supervisor Approval)
        old_seq_list = sorted([{"stop_id": str(s.id), "sequence": s.sequence} for s in stops], key=lambda x: x["sequence"])
        new_seq_list = [{"stop_id": s["stop_id"], "sequence": s["new_sequence"]} for s in optimized_stops]
        
        optimization = Optimization(
            route_id=route.id,
            optimization_type="dynamic_replan",
            algorithm="adaptive-ai",
            old_route=old_seq_list,
            new_route=new_seq_list,
            distance_saved=explain_res["benefits"]["distance_saved_km"],
            time_saved=explain_res["benefits"]["time_saved_min"],
            fuel_saved=explain_res["benefits"]["fuel_saved_liters"],
            carbon_saved=explain_res["benefits"]["fuel_saved_liters"] * 2.68,
            confidence=explain_res["confidence_score"],
            reason=f"Event: {event_res['summary']}. {explain_res['impact_summary']}"
        )
        db.add(optimization)
        await db.flush()
        
        decision = AIDecision(
            route_id=route.id,
            decision=f"event_{event_type}",
            confidence=explain_res["confidence_score"],
            reason=explain_res["explanation"],
            llm_model="gemini-2.5-flash",
            execution_time=2.0,
            cost=0.002,
            approved=False
        )
        db.add(decision)
        await db.commit()
        
        return {
            "success": True,
            "replan_required": True,
            "optimization_id": str(optimization.id),
            "decision_id": str(decision.id),
            "event_analysis": event_res,
            "old_summary": old_route_summary,
            "new_summary": new_route_summary,
            "optimized_stops": optimized_stops,
            "constraints": constraint_res,
            "validation": validation_res,
            "explanation": explain_res
        }

# Singleton Instance
coordinator = CoordinatorAgent()
