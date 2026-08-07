import logging
import json
from typing import Dict, Any, List, Optional
from backend.app.core.ai_adapter import ai_service

logger = logging.getLogger("explainer_agent")

class ExplainabilityAgent:
    def __init__(self):
        pass
        
    async def run(
        self,
        old_route_summary: Dict[str, Any],
        new_route_summary: Dict[str, Any],
        event_trigger: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generates natural language explanation for route optimization or replanning.
        """
        logger.info("Explainability Agent generating route explanation...")
        
        prompt = f"""
        Explain the changes and benefits of this route optimization.
        
        Old Route Summary:
        - Distance: {old_route_summary.get('distance_km', 'N/A')} km
        - Duration: {old_route_summary.get('duration_min', 'N/A')} minutes
        - Stops Count: {old_route_summary.get('stops_count', 'N/A')}
        
        New (Optimized) Route Summary:
        - Distance: {new_route_summary.get('distance_km', 'N/A')} km
        - Duration: {new_route_summary.get('duration_min', 'N/A')} minutes
        - Stops Count: {new_route_summary.get('stops_count', 'N/A')}
        - Optimization Score: {new_route_summary.get('optimization_score', 'N/A')}
        
        Event Trigger (if any): {event_trigger if event_trigger else "None (Regular batch optimization)"}
        
        Provide:
        1. Rationale: Why was the route re-sequenced? (1-2 sentences)
        2. Expected Benefits: Time saved, fuel reduction, risk mitigation.
        3. Confidence Score: A score from 0 to 100 on how confident the AI is about this suggestion.
        4. Summary of modifications: List which stops were reordered or skipped.
        
        Return response in JSON matching this schema:
        {{
            "explanation": "Detailed natural language explanation text",
            "confidence_score": 95,
            "benefits": {{
                "time_saved_min": 15.5,
                "distance_saved_km": 5.2,
                "fuel_saved_liters": 1.5,
                "cost_saved_inr": 250.0
            }},
            "impact_summary": "E.g., Bypassed traffic on arterial road, saving 15 mins."
        }}
        """
        
        try:
            ai_response = await ai_service.generate_text(
                prompt=prompt,
                system_instruction="You are RouteMind Explainability Agent, explaining route optimization choices.",
                json_mode=True
            )
            res = json.loads(ai_response)
            return {
                "success": True,
                "explanation": res.get("explanation", "Route optimized to minimize total transit time."),
                "confidence_score": float(res.get("confidence_score", 90.0)),
                "benefits": res.get("benefits", {
                    "time_saved_min": max(0.0, float(old_route_summary.get('duration_min', 0)) - float(new_route_summary.get('duration_min', 0))),
                    "distance_saved_km": max(0.0, float(old_route_summary.get('distance_km', 0)) - float(new_route_summary.get('distance_km', 0))),
                    "fuel_saved_liters": 0.0,
                    "cost_saved_inr": 0.0
                }),
                "impact_summary": res.get("impact_summary", "Route optimized successfully.")
            }
        except Exception as e:
            logger.exception("AI Explainability generation failed")
            t_saved = max(0.0, float(old_route_summary.get('duration_min', 0)) - float(new_route_summary.get('duration_min', 0)))
            d_saved = max(0.0, float(old_route_summary.get('distance_km', 0)) - float(new_route_summary.get('distance_km', 0)))
            return {
                "success": True,
                "explanation": f"The route has been optimized to reduce overall duration by {t_saved:.1f} minutes and distance by {d_saved:.1f} km.",
                "confidence_score": 85.0,
                "benefits": {
                    "time_saved_min": round(t_saved, 2),
                    "distance_saved_km": round(d_saved, 2),
                    "fuel_saved_liters": round(d_saved * 0.15, 2),  # approx 15L/100km fuel consumption
                    "cost_saved_inr": round(d_saved * 15.0, 2)  # approx 15 INR per km
                },
                "impact_summary": "Route optimized to minimize total travel cost and time."
            }
