from typing import Dict, Any, List
import json

def retrieve_interaction_tool(user_input: str, llm_response: str) -> Dict[str, Any]:
    """
    Tool to search and retrieve past interactions based on criteria.
    
    Args:
        user_input: Natural language search query
        llm_response: Structured search criteria from LLM
        
    Returns:
        Dictionary with search parameters
    """
    try:
        search_params = {
            "hcp_name": None,
            "sentiment": None,
            "date_from": None,
            "date_to": None,
            "products_discussed": None
        }
        
        # Try to parse JSON response from LLM
        try:
            parsed_params = json.loads(llm_response)
            search_params.update(parsed_params)
        except json.JSONDecodeError:
            # Fallback parsing
            pass
        
        return {
            "status": "success",
            "action": "search_interactions",
            "data": search_params
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve interaction: {str(e)}"
        }


def format_retrieve_interaction_prompt(user_input: str) -> str:
    """
    Format the prompt for the LLM to extract search criteria.
    """
    return f"""You are an AI assistant helping to search healthcare professional (HCP) interaction records.

The user wants to search for interactions:
"{user_input}"

Extract search criteria and return as a JSON object with these fields:
- hcp_name: Name to search for (use null if not specified)
- sentiment: Sentiment filter (positive, negative, neutral, or null)
- date_from: Start date for date range (ISO format, or null)
- date_to: End date for date range (ISO format, or null)
- products_discussed: Product name to search for (or null)

Return ONLY a valid JSON object. Example:
{{
    "hcp_name": "Dr. Smith",
    "sentiment": "positive",
    "date_from": null,
    "date_to": null,
    "products_discussed": null
}}"""

