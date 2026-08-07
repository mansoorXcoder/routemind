import logging
import json
from typing import Dict, Any, Optional
from backend.app.core.ai_adapter import ai_service

logger = logging.getLogger("event_agent")

class EventAgent:
    def __init__(self):
        pass
        
    async def run(self, event_type: str, details: Dict[str, Any], route_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze an event payload and determine priority and impact score.
        """
        logger.info(f"Event Detection Agent analyzing event: {event_type}...")
        
        prompt = f"""
        Analyze the following real-time logistics event and calculate its priority and impact score.
        
        Event Type: {event_type}
        Event Details: {details}
        Active Route Context: {route_info if route_info else "No route context provided"}
        
        Determine:
        1. Priority: "low", "medium", "high", or "critical"
        2. Impact Score: a score between 0 (no impact) and 100 (total route failure / stop route)
        3. ETA Change (Minutes): estimated delay added (positive) or saved (negative)
        4. Re-plan Required: true or false (should we trigger OR-Tools replanning?)
        
        Return response in JSON matching this schema:
        {{
            "priority": "low/medium/high/critical",
            "impact_score": 75,
            "eta_change_minutes": 45.0,
            "replan_required": true,
            "summary": "Short 1-sentence description of impact"
        }}
        """
        
        try:
            ai_response = await ai_service.generate_text(
                prompt=prompt,
                system_instruction="You are RouteMind Event Agent, analyzing supply chain disruptions.",
                json_mode=True
            )
            res = json.loads(ai_response)
            return {
                "success": True,
                "event_type": event_type,
                "details": details,
                "priority": res.get("priority", "medium"),
                "impact_score": float(res.get("impact_score", 50)),
                "eta_change_minutes": float(res.get("eta_change_minutes", 0.0)),
                "replan_required": bool(res.get("replan_required", False)),
                "summary": res.get("summary", "Event detected on route.")
            }
        except Exception as e:
            logger.exception("AI Event analysis failed")
            # Safe fallbacks
            replan = event_type in ["traffic", "road_closure", "vehicle_breakdown", "new_pickup"]
            priority = "high" if event_type == "vehicle_breakdown" else "medium"
            return {
                "success": True,
                "event_type": event_type,
                "details": details,
                "priority": priority,
                "impact_score": 60.0 if replan else 10.0,
                "eta_change_minutes": 30.0 if replan else 0.0,
                "replan_required": replan,
                "summary": f"Real-time {event_type} event triggered replan check."
            }
        
