from typing import Dict, Any
from datetime import datetime, timedelta
import json

def schedule_followup_tool(user_input: str, llm_response: str) -> Dict[str, Any]:
    """
    Tool to schedule follow-up actions and reminders.
    
    Args:
        user_input: Request to schedule follow-up
        llm_response: Structured follow-up details from LLM
        
    Returns:
        Dictionary with follow-up schedule information
    """
    try:
        followup_data = {
            "follow_up_date": None,
            "follow_up_action": None,
            "priority": "medium",
            "reminder_type": "email"
        }
        
        # Try to parse JSON response from LLM
        try:
            parsed_data = json.loads(llm_response)
            followup_data.update(parsed_data)
        except json.JSONDecodeError:
            # Fallback: extract basic info
            lower_input = user_input.lower()
            
            # Determine priority
            if "urgent" in lower_input or "asap" in lower_input:
                followup_data["priority"] = "high"
            elif "low priority" in lower_input:
                followup_data["priority"] = "low"
            
            # Set default follow-up date if mentioned
            if "next week" in lower_input:
                followup_data["follow_up_date"] = (datetime.utcnow() + timedelta(weeks=1)).isoformat()
            elif "tomorrow" in lower_input:
                followup_data["follow_up_date"] = (datetime.utcnow() + timedelta(days=1)).isoformat()
            elif "2 weeks" in lower_input:
                followup_data["follow_up_date"] = (datetime.utcnow() + timedelta(weeks=2)).isoformat()
        
        return {
            "status": "success",
            "action": "schedule_followup",
            "data": followup_data
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to schedule follow-up: {str(e)}"
        }


def format_schedule_followup_prompt(user_input: str) -> str:
    """
    Format the prompt for the LLM to extract follow-up details.
    """
    return f"""You are an AI assistant helping to schedule follow-up actions for healthcare professional (HCP) interactions.

The user wants to schedule a follow-up:
"{user_input}"

Extract follow-up details and return as a JSON object:
- follow_up_date: Date for follow-up (ISO format)
- follow_up_action: Description of the action needed
- priority: Priority level (high, medium, low)
- reminder_type: Type of reminder (email, call, meeting)

Return ONLY valid JSON. Example:
{{
    "follow_up_date": "{(datetime.utcnow() + timedelta(weeks=2)).isoformat()}",
    "follow_up_action": "Share clinical trial results and schedule product demo",
    "priority": "high",
    "reminder_type": "meeting"
}}"""

