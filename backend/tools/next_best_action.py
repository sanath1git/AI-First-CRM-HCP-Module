from typing import Dict, Any, List
import json

def next_best_action_tool(hcp_context: str, llm_response: str) -> Dict[str, Any]:
    """
    Tool to suggest the next best action for a field rep based on HCP context.
    Uses HCP's specialty, recent interaction sentiment, and product portfolio
    to recommend optimal next steps.
    
    Uses llama-3.3-70b-versatile for larger context reasoning.
    
    Args:
        hcp_context: Context about HCP (specialty, interaction history, sentiment)
        llm_response: Recommended actions from LLM
        
    Returns:
        Dictionary with recommended next actions
    """
    try:
        recommendations = {
            "primary_action": None,
            "alternative_actions": [],
            "rationale": None,
            "priority": "medium",
            "timeline": None,
            "resources_needed": []
        }
        
        # Try to parse JSON response from LLM
        try:
            parsed_recommendations = json.loads(llm_response)
            recommendations.update(parsed_recommendations)
        except json.JSONDecodeError:
            # Fallback: basic recommendation structure
            recommendations["primary_action"] = "Schedule follow-up meeting"
            recommendations["alternative_actions"] = [
                "Send product information email",
                "Invite to upcoming webinar"
            ]
            recommendations["rationale"] = "Based on the interaction context"
        
        return {
            "status": "success",
            "action": "next_best_action",
            "data": recommendations,
            "message": f"💡 Recommended next action: {recommendations['primary_action']}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to generate next best action: {str(e)}"
        }


def format_next_best_action_prompt(hcp_context: str) -> str:
    """
    Format the prompt for the LLM to recommend next best action.
    This uses more sophisticated reasoning with larger context.
    """
    return f"""You are an AI sales strategist for pharmaceutical field representatives. Based on the HCP interaction context, recommend the optimal next action.

HCP Context:
{hcp_context}

Consider:
1. HCP's specialty and prescribing patterns
2. Recent interaction sentiment and receptiveness
3. Stage in the engagement cycle
4. Products discussed and interest level
5. Competitive landscape
6. Compliance requirements

Return a JSON object with:
- primary_action: The single best next step (specific and actionable)
- alternative_actions: Array of 2-3 alternative options
- rationale: Brief explanation of why this is the best action
- priority: Priority level (high/medium/low)
- timeline: Recommended timeframe (e.g., "Within 1 week", "2-3 weeks")
- resources_needed: Array of materials/resources needed (e.g., ["Phase III trial data", "Patient case studies"])

Examples of good actions:
- "Send Cardiol Phase III trial abstract via email"
- "Schedule lunch-and-learn for clinic staff"
- "Escalate to medical science liaison for technical questions"
- "Invite to regional medical conference"
- "Provide patient starter samples"

Return ONLY valid JSON. Example:
{{
    "primary_action": "Send Cardiol Phase III trial abstract via email",
    "alternative_actions": [
        "Schedule follow-up call to discuss trial results",
        "Invite to upcoming product webinar"
    ],
    "rationale": "HCP expressed high interest in clinical efficacy data and positive sentiment. Providing trial results will address their questions and move them toward prescribing.",
    "priority": "high",
    "timeline": "Within 3 days",
    "resources_needed": [
        "Phase III trial abstract",
        "Efficacy comparison chart",
        "Safety profile document"
    ]
}}"""

