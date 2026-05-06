from typing import Dict, Any
import json

def hcp_profile_lookup_tool(user_input: str, llm_response: str) -> Dict[str, Any]:
    """
    Tool to look up HCP profile information by NPI number or name.
    Returns specialty, tier, prescribing history, last interaction date, and compliance flags.
    
    Args:
        user_input: Request to look up HCP profile
        llm_response: Structured lookup criteria from LLM
        
    Returns:
        Dictionary with HCP profile lookup parameters
    """
    try:
        lookup_params = {
            "hcp_name": None,
            "npi_number": None,
            "specialty": None
        }
        
        # Try to parse JSON response from LLM
        try:
            parsed_params = json.loads(llm_response)
            lookup_params.update(parsed_params)
        except json.JSONDecodeError:
            # Fallback: basic extraction from user input
            lower_input = user_input.lower()
            
            # Extract name if mentioned with "Dr."
            if "dr." in lower_input or "doctor" in lower_input:
                words = user_input.split()
                for i, word in enumerate(words):
                    if word.lower() in ["dr.", "doctor"] and i + 1 < len(words):
                        lookup_params["hcp_name"] = f"Dr. {words[i+1]}"
                        break
        
        return {
            "status": "success",
            "action": "hcp_profile_lookup",
            "data": lookup_params,
            "message": "Looking up HCP profile information..."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to lookup HCP profile: {str(e)}"
        }


def format_hcp_profile_lookup_prompt(user_input: str) -> str:
    """
    Format the prompt for the LLM to extract HCP lookup criteria.
    """
    return f"""You are an AI assistant helping to look up healthcare professional (HCP) profiles.

The user wants to look up an HCP profile:
"{user_input}"

Extract the search criteria and return as a JSON object:
- hcp_name: Name of the HCP (e.g., "Dr. Smith")
- npi_number: National Provider Identifier if mentioned (10-digit number)
- specialty: Medical specialty if mentioned (e.g., "Cardiology", "Oncology")

Return ONLY valid JSON. Example:
{{
    "hcp_name": "Dr. Smith",
    "npi_number": null,
    "specialty": "Cardiology"
}}"""

