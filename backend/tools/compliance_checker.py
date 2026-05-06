from typing import Dict, Any, List
import json

def compliance_checker_tool(interaction_text: str, llm_response: str) -> Dict[str, Any]:
    """
    Tool to scan interaction notes for compliance violations.
    Checks for restricted promotional claims, off-label language, or policy violations.
    This is a critical pharma CRM requirement.
    
    Args:
        interaction_text: The interaction notes to check
        llm_response: Compliance analysis from LLM
        
    Returns:
        Dictionary with compliance status and any violations found
    """
    try:
        compliance_result = {
            "is_compliant": True,
            "violations": [],
            "warnings": [],
            "risk_level": "low"
        }
        
        # Try to parse JSON response from LLM
        try:
            parsed_result = json.loads(llm_response)
            compliance_result.update(parsed_result)
        except json.JSONDecodeError:
            # Fallback: basic keyword scanning
            lower_text = interaction_text.lower()
            
            # Check for common compliance red flags
            off_label_keywords = ["off-label", "unapproved use", "not indicated for"]
            promotional_claims = ["guaranteed", "cure", "100% effective", "miracle"]
            
            for keyword in off_label_keywords:
                if keyword in lower_text:
                    compliance_result["is_compliant"] = False
                    compliance_result["violations"].append({
                        "type": "off_label_promotion",
                        "keyword": keyword,
                        "severity": "critical"
                    })
                    compliance_result["risk_level"] = "high"
            
            for keyword in promotional_claims:
                if keyword in lower_text:
                    compliance_result["warnings"].append({
                        "type": "unsubstantiated_claim",
                        "keyword": keyword,
                        "severity": "medium"
                    })
                    if compliance_result["risk_level"] == "low":
                        compliance_result["risk_level"] = "medium"
        
        # Determine action based on compliance
        if not compliance_result["is_compliant"]:
            return {
                "status": "violation",
                "action": "compliance_check_failed",
                "data": compliance_result,
                "message": "⚠️ Compliance violation detected! Please revise the interaction notes before saving."
            }
        else:
            return {
                "status": "success",
                "action": "compliance_check_passed",
                "data": compliance_result,
                "message": "✓ Compliance check passed. Interaction can be saved."
            }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to check compliance: {str(e)}"
        }


def format_compliance_checker_prompt(interaction_text: str) -> str:
    """
    Format the prompt for the LLM to analyze compliance.
    """
    return f"""You are a pharmaceutical compliance AI assistant. Analyze the following HCP interaction notes for regulatory compliance.

Interaction text:
"{interaction_text}"

Check for:
1. Off-label promotion (discussing unapproved uses)
2. Unsubstantiated claims (guarantees, cure claims, exaggerated efficacy)
3. Missing safety information disclosures
4. Inappropriate comparative claims
5. Privacy violations (sharing patient data)

Return a JSON object with:
- is_compliant: boolean (true if no violations found)
- violations: array of objects with type, keyword, and severity (critical/high/medium)
- warnings: array of objects with type, keyword, and severity
- risk_level: overall risk (low/medium/high/critical)
- recommendations: array of strings suggesting how to fix issues

Example:
{{
    "is_compliant": false,
    "violations": [
        {{
            "type": "off_label_promotion",
            "keyword": "off-label use for pediatric patients",
            "severity": "critical"
        }}
    ],
    "warnings": [],
    "risk_level": "high",
    "recommendations": ["Remove reference to unapproved use", "Consult medical affairs team"]
}}

Return ONLY valid JSON."""

