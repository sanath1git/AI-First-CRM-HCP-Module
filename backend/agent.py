from typing import Dict, Any, List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
import json
from tools.log_interaction import log_interaction_tool, format_log_interaction_prompt
from tools.edit_interaction import edit_interaction_tool, format_edit_interaction_prompt
from tools.retrieve_interaction import retrieve_interaction_tool, format_retrieve_interaction_prompt
from tools.analyze_sentiment import analyze_sentiment_tool, format_analyze_sentiment_prompt
from tools.schedule_followup import schedule_followup_tool, format_schedule_followup_prompt
from tools.hcp_profile_lookup import hcp_profile_lookup_tool, format_hcp_profile_lookup_prompt
from tools.compliance_checker import compliance_checker_tool, format_compliance_checker_prompt
from tools.next_best_action import next_best_action_tool, format_next_best_action_prompt

load_dotenv()

# Initialize Groq LLM with llama-3.3-70b-versatile
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=2000
)

# Define the state structure for the agent
class AgentState(TypedDict):
    messages: List[str]
    user_input: str
    intent: str
    current_data: Dict[str, Any]
    result: Dict[str, Any]
    error: str

def classify_intent(state: AgentState) -> AgentState:
    """
    Classify the user's intent to determine which tool to use.
    """
    user_input = state["user_input"].lower()
    
    # Intent classification logic
    if any(keyword in user_input for keyword in ["log", "met with", "discussed", "talked to", "interaction with", "visited", "today i"]):
        state["intent"] = "log_interaction"
    elif any(keyword in user_input for keyword in ["edit", "change", "update", "modify", "correct", "actually", "sorry"]):
        state["intent"] = "edit_interaction"
    elif any(keyword in user_input for keyword in ["search", "find", "retrieve", "show me", "get", "look up", "past interactions"]):
        state["intent"] = "retrieve_interaction"
    elif any(keyword in user_input for keyword in ["analyze", "sentiment", "how was", "feedback", "opinion", "insights"]):
        state["intent"] = "analyze_sentiment"
    elif any(keyword in user_input for keyword in ["schedule", "follow-up", "follow up", "reminder", "next meeting", "plan"]):
        state["intent"] = "schedule_followup"
    elif any(keyword in user_input for keyword in ["profile", "look up", "who is", "tell me about", "hcp info", "doctor info", "npi"]):
        state["intent"] = "hcp_profile_lookup"
    elif any(keyword in user_input for keyword in ["compliance", "check", "compliant", "violation", "regulatory", "approve"]):
        state["intent"] = "compliance_checker"
    elif any(keyword in user_input for keyword in ["what should i", "recommend", "next action", "next step", "what to do", "suggest"]):
        state["intent"] = "next_best_action"
    else:
        # Default to log_interaction if unclear
        state["intent"] = "log_interaction"
    
    return state

def execute_tool(state: AgentState) -> AgentState:
    """
    Execute the appropriate tool based on the classified intent.
    """
    intent = state["intent"]
    user_input = state["user_input"]
    current_data = state.get("current_data", {})
    
    try:
        if intent == "log_interaction":
            # Get LLM to extract structured data
            prompt = format_log_interaction_prompt(user_input)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = log_interaction_tool(user_input, llm_response)
            state["result"] = result
            
        elif intent == "edit_interaction":
            # Get LLM to identify changes
            prompt = format_edit_interaction_prompt(user_input, current_data)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = edit_interaction_tool(user_input, llm_response, current_data)
            state["result"] = result
            
        elif intent == "retrieve_interaction":
            # Get LLM to extract search criteria
            prompt = format_retrieve_interaction_prompt(user_input)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = retrieve_interaction_tool(user_input, llm_response)
            state["result"] = result
            
        elif intent == "analyze_sentiment":
            # Get LLM to analyze sentiment
            prompt = format_analyze_sentiment_prompt(user_input)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = analyze_sentiment_tool(user_input, llm_response)
            state["result"] = result
            
        elif intent == "schedule_followup":
            # Get LLM to extract follow-up details
            prompt = format_schedule_followup_prompt(user_input)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = schedule_followup_tool(user_input, llm_response)
            state["result"] = result
            
        elif intent == "hcp_profile_lookup":
            # Get LLM to extract lookup criteria
            prompt = format_hcp_profile_lookup_prompt(user_input)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = hcp_profile_lookup_tool(user_input, llm_response)
            state["result"] = result
            
        elif intent == "compliance_checker":
            # Get LLM to analyze compliance
            prompt = format_compliance_checker_prompt(user_input)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = compliance_checker_tool(user_input, llm_response)
            state["result"] = result
            
        elif intent == "next_best_action":
            # Get LLM to recommend next action
            prompt = format_next_best_action_prompt(user_input)
            response = llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            result = next_best_action_tool(user_input, llm_response)
            state["result"] = result
        
    except Exception as e:
        state["error"] = str(e)
        state["result"] = {
            "status": "error",
            "message": f"Error executing {intent}: {str(e)}"
        }
    
    return state

def generate_response(state: AgentState) -> AgentState:
    """
    Generate a natural language response for the user.
    """
    result = state.get("result", {})
    intent = state["intent"]
    
    # Create a friendly response based on the action taken
    if result.get("status") == "success":
        action = result.get("action", "")
        
        if action == "create_interaction":
            response_text = "I've logged the interaction. The form has been populated with the details you provided."
        elif action == "update_interaction":
            response_text = "I've updated the interaction with the changes you specified."
        elif action == "search_interactions":
            response_text = "I'm searching for interactions matching your criteria."
        elif action == "sentiment_analysis":
            response_text = "I've analyzed the sentiment of the interaction."
        elif action == "schedule_followup":
            response_text = "I've scheduled the follow-up action."
        elif action == "hcp_profile_lookup":
            response_text = result.get("message", "I've retrieved the HCP profile information.")
        elif action == "compliance_check_passed":
            response_text = result.get("message", "✓ Compliance check passed.")
        elif action == "next_best_action":
            response_text = result.get("message", "I've generated next best action recommendations.")
        else:
            response_text = "Action completed successfully."
    elif result.get("status") == "violation":
        # Compliance violation
        response_text = result.get("message", "⚠️ Compliance issue detected.")
    else:
        response_text = result.get("message", "I encountered an error processing your request.")
    
    state["result"]["response"] = response_text
    return state

# Build the LangGraph workflow
def build_agent_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("execute_tool", execute_tool)
    workflow.add_node("generate_response", generate_response)
    
    # Add edges
    workflow.add_edge("classify_intent", "execute_tool")
    workflow.add_edge("execute_tool", "generate_response")
    workflow.add_edge("generate_response", END)
    
    # Set entry point
    workflow.set_entry_point("classify_intent")
    
    return workflow.compile()

# Create the agent
agent_graph = build_agent_graph()

def process_user_message(user_input: str, current_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Process a user message through the LangGraph agent.
    
    Args:
        user_input: The user's message
        current_data: Current form data (for edit operations)
        
    Returns:
        Result dictionary with action and data
    """
    initial_state = {
        "messages": [],
        "user_input": user_input,
        "intent": "",
        "current_data": current_data or {},
        "result": {},
        "error": ""
    }
    
    # Run the agent
    final_state = agent_graph.invoke(initial_state)
    
    return final_state["result"]

