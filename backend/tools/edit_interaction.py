from typing import Dict, Any
import json

def edit_interaction_tool(user_input: str, llm_response: str, current_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to edit specific fields in an existing interaction.
    Only updates the fields mentioned in the user input.
    
    Args:
        user_input: Natural language description of what to change
        llm_response: Structured response from LLM identifying changes
        current_data: Current interaction data
        
    Returns:
        Dictionary with fields to update
    """
    try:
        updates = {}
        
        # Try to parse JSON response from LLM
        try:
            parsed_updates = json.loads(llm_response)
            updates = parsed_updates
        except json.JSONDecodeError:
            # Try to extract JSON from markdown or text
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', llm_response, re.DOTALL)
            if json_match:
                try:
                    parsed_updates = json.loads(json_match.group(1))
                    updates = parsed_updates
                except json.JSONDecodeError:
                    pass
            else:
                # Try to find JSON object in the response
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', llm_response, re.DOTALL)
                if json_match:
                    try:
                        parsed_updates = json.loads(json_match.group(0))
                        updates = parsed_updates
                    except json.JSONDecodeError:
                        pass
            
            # If still no updates extracted, use fallback parsing
            if not updates:
                lower_input = user_input.lower()
                
                # Check for name changes (common patterns)
                if "not" in lower_input and "its" in lower_input:
                    # Pattern: "not Dr. X its Dr. Y" or "not X its Y"
                    import re
                    # Look for "its Dr. X" or "it's Dr. X"
                    name_match = re.search(r"it'?s\s+(?:dr\.?\s+)?(\w+)", lower_input, re.IGNORECASE)
                    if name_match:
                        new_name = name_match.group(1)
                        if "dr" in lower_input:
                            updates["hcp_name"] = f"Dr. {new_name.capitalize()}"
                        else:
                            updates["hcp_name"] = new_name.capitalize()
                
                # Check for sentiment changes
                if "sentiment" in lower_input:
                    if "positive" in lower_input:
                        updates["sentiment"] = "positive"
                    elif "negative" in lower_input:
                        updates["sentiment"] = "negative"
                    elif "neutral" in lower_input:
                        updates["sentiment"] = "neutral"
        
        # Only return fields that are being updated
        return {
            "status": "success",
            "action": "update_interaction",
            "data": updates
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to edit interaction: {str(e)}"
        }


def format_edit_interaction_prompt(user_input: str, current_data: Dict[str, Any]) -> str:
    """
    Format the prompt for the LLM to identify what fields to update.
    """
    return f"""You are an AI assistant helping to edit healthcare professional (HCP) interaction records.

Current interaction data:
{json.dumps(current_data, indent=2, default=str)}

The user wants to make changes:
"{user_input}"

Identify which fields need to be updated and return ONLY a JSON object with the fields that should change.
Do NOT include fields that remain the same.

Available fields:
- hcp_name: Name of the healthcare professional
- interaction_date: Date of interaction (ISO format)
- sentiment: positive, negative, or neutral
- products_discussed: Products or topics discussed
- materials_shared: List of materials (e.g., ["brochure", "sample"])
- interaction_type: Meeting, Call, Email, Conference
- location: Location of interaction
- duration_minutes: Duration in minutes
- notes: Additional notes
- follow_up_date: Follow-up date (ISO format)
- follow_up_action: Follow-up action needed

Return ONLY a JSON object with the fields to update. Example:
{{
    "hcp_name": "Dr. John",
    "sentiment": "negative"
}}"""

