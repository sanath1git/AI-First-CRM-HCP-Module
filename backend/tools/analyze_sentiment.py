from typing import Dict, Any
import json

def analyze_sentiment_tool(user_input: str, llm_response: str) -> Dict[str, Any]:
    """
    Tool to analyze sentiment and provide insights from interaction data.
    
    Args:
        user_input: Request for sentiment analysis
        llm_response: Analysis result from LLM
        
    Returns:
        Dictionary with sentiment analysis results
    """
    try:
        analysis = {
            "sentiment": None,
            "confidence": None,
            "key_points": [],
            "recommendations": []
        }
        
        # Try to parse JSON response from LLM
        try:
            parsed_analysis = json.loads(llm_response)
            analysis.update(parsed_analysis)
        except json.JSONDecodeError:
            # Store raw analysis
            analysis["raw_analysis"] = llm_response
        
        return {
            "status": "success",
            "action": "sentiment_analysis",
            "data": analysis
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to analyze sentiment: {str(e)}"
        }


def format_analyze_sentiment_prompt(interaction_text: str) -> str:
    """
    Format the prompt for the LLM to analyze sentiment.
    """
    return f"""You are an AI assistant specializing in analyzing healthcare professional (HCP) interactions.

Analyze the sentiment and provide insights for this interaction:
"{interaction_text}"

Return a JSON object with:
- sentiment: Overall sentiment (positive, negative, or neutral)
- confidence: Confidence level (high, medium, low)
- key_points: List of key discussion points
- recommendations: List of recommended follow-up actions

Example:
{{
    "sentiment": "positive",
    "confidence": "high",
    "key_points": ["Interested in product efficacy", "Asked about clinical trials", "Positive about patient outcomes"],
    "recommendations": ["Share latest clinical trial results", "Schedule follow-up in 2 weeks", "Provide patient case studies"]
}}

Return ONLY valid JSON."""

