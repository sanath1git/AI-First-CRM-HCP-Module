from typing import Dict, Any
from datetime import datetime
from dateutil import parser as date_parser
import json

def log_interaction_tool(user_input: str, llm_response: str) -> Dict[str, Any]:
    """
    Tool to extract interaction data from natural language input.
    Uses LLM to parse and structure the interaction details.
    
    Args:
        user_input: Natural language description of the interaction
        llm_response: Structured response from LLM
        
    Returns:
        Dictionary with extracted interaction fields
    """
    try:
        # Parse the LLM response to extract structured data
        interaction_data = {
            "hcp_name": None,
            "interaction_date": None,
            "sentiment": None,
            "products_discussed": None,
            "materials_shared": [],
            "interaction_type": None,
            "location": None,
            "duration_minutes": None,
            "notes": user_input,
            "follow_up_date": None,
            "follow_up_action": None
        }
        
        # Try to parse JSON if LLM returns structured data
        try:
            # Try direct JSON parsing first
            parsed_data = json.loads(llm_response)
            interaction_data.update(parsed_data)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks or text
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', llm_response, re.DOTALL)
            if json_match:
                try:
                    parsed_data = json.loads(json_match.group(1))
                    interaction_data.update(parsed_data)
                except json.JSONDecodeError:
                    pass
            else:
                # Try to find JSON object in the response
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', llm_response, re.DOTALL)
                if json_match:
                    try:
                        parsed_data = json.loads(json_match.group(0))
                        interaction_data.update(parsed_data)
                    except json.JSONDecodeError:
                        pass
            
            # If still no data extracted, use fallback parsing
            if not interaction_data.get("hcp_name"):
                # Fallback for basic extraction
                lower_input = user_input.lower()
                
                # Extract HCP name (look for "Dr." pattern)
                import re
                dr_match = re.search(r'dr\.?\s+(\w+)', user_input, re.IGNORECASE)
                if dr_match:
                    interaction_data["hcp_name"] = f"Dr. {dr_match.group(1)}"
                else:
                    # Look for "met with" pattern
                    met_match = re.search(r'met with\s+([^,\.]+)', user_input, re.IGNORECASE)
                    if met_match:
                        interaction_data["hcp_name"] = met_match.group(1).strip()
                    else:
                        interaction_data["hcp_name"] = "Unknown HCP"
                
                # Extract sentiment
                if "positive" in lower_input or "good" in lower_input or "excellent" in lower_input:
                    interaction_data["sentiment"] = "positive"
                elif "negative" in lower_input or "bad" in lower_input or "poor" in lower_input:
                    interaction_data["sentiment"] = "negative"
                elif "neutral" in lower_input or "okay" in lower_input:
                    interaction_data["sentiment"] = "neutral"
                
                # Extract products discussed
                product_match = re.search(r'(product\s+\w+|discussed\s+(\w+))', user_input, re.IGNORECASE)
                if product_match:
                    interaction_data["products_discussed"] = product_match.group(0)
                    
                # Extract materials
                if "brochure" in lower_input:
                    interaction_data["materials_shared"].append("brochure")
                if "sample" in lower_input:
                    interaction_data["materials_shared"].append("sample")
                if "presentation" in lower_input:
                    interaction_data["materials_shared"].append("presentation")
        
        # Ensure date is set to today if not provided
        if not interaction_data["interaction_date"]:
            interaction_data["interaction_date"] = datetime.utcnow().isoformat()
        
        return {
            "status": "success",
            "action": "create_interaction",
            "data": interaction_data
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to log interaction: {str(e)}"
        }


def format_log_interaction_prompt(user_input: str) -> str:
    """
    Format the prompt for the LLM to extract interaction data.
    """
    return f"""You are an AI assistant helping to log healthcare professional (HCP) interactions.
Extract information from the user's message and return it as a JSON object.

IMPORTANT: Return ONLY the JSON object, no explanations or markdown formatting.

Required fields:
- hcp_name: Name of the healthcare professional (e.g., "Dr. Smith")
- interaction_date: Today's date in ISO format: "{datetime.utcnow().isoformat()}"
- sentiment: Overall sentiment (positive, negative, or neutral)
- products_discussed: Products or topics discussed
- materials_shared: Array of materials (e.g., ["brochure", "sample", "presentation"])
- interaction_type: Type (Meeting, Call, Email, Conference)
- location: Where it took place (or null)
- duration_minutes: Duration in minutes (or null)
- notes: The full user message
- follow_up_date: Follow-up date in ISO format (or null)
- follow_up_action: Follow-up action needed (or null)

User message: "{user_input}"

Return ONLY this JSON (no markdown, no explanation):
{{
    "hcp_name": "Dr. Smith",
    "interaction_date": "{datetime.utcnow().isoformat()}",
    "sentiment": "positive",
    "products_discussed": "Product X efficiency",
    "materials_shared": ["brochure"],
    "interaction_type": "Meeting",
    "location": null,
    "duration_minutes": null,
    "notes": "{user_input}",
    "follow_up_date": null,
    "follow_up_action": null
}}"""

