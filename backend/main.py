from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

import models
import schemas
from database import engine, get_db, init_db
from agent import process_user_message

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-CRM HCP Module API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "AI-CRM HCP Module API", "status": "running"}

# Interaction endpoints
@app.post("/api/interactions", response_model=schemas.InteractionResponse)
def create_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    """Create a new HCP interaction."""
    db_interaction = models.HCPInteraction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@app.get("/api/interactions", response_model=List[schemas.InteractionResponse])
def list_interactions(
    skip: int = 0,
    limit: int = 100,
    hcp_name: Optional[str] = None,
    sentiment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all HCP interactions with optional filters."""
    query = db.query(models.HCPInteraction)
    
    if hcp_name:
        query = query.filter(models.HCPInteraction.hcp_name.ilike(f"%{hcp_name}%"))
    if sentiment:
        query = query.filter(models.HCPInteraction.sentiment == sentiment)
    
    interactions = query.order_by(models.HCPInteraction.created_at.desc()).offset(skip).limit(limit).all()
    return interactions

@app.get("/api/interactions/{interaction_id}", response_model=schemas.InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific HCP interaction by ID."""
    interaction = db.query(models.HCPInteraction).filter(models.HCPInteraction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

@app.put("/api/interactions/{interaction_id}", response_model=schemas.InteractionResponse)
def update_interaction(
    interaction_id: int,
    interaction_update: schemas.InteractionUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing HCP interaction."""
    db_interaction = db.query(models.HCPInteraction).filter(models.HCPInteraction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    # Update only provided fields
    update_data = interaction_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_interaction, key, value)
    
    db_interaction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@app.delete("/api/interactions/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete an HCP interaction."""
    db_interaction = db.query(models.HCPInteraction).filter(models.HCPInteraction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    db.delete(db_interaction)
    db.commit()
    return {"message": "Interaction deleted successfully"}

# HCP Profile endpoints
@app.post("/api/hcp-profiles", response_model=schemas.HCPProfileResponse)
def create_hcp_profile(profile: schemas.HCPProfileCreate, db: Session = Depends(get_db)):
    """Create a new HCP profile."""
    db_profile = models.HCPProfile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.get("/api/hcp-profiles", response_model=List[schemas.HCPProfileResponse])
def list_hcp_profiles(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    specialty: Optional[str] = None,
    npi: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all HCP profiles with optional filters."""
    query = db.query(models.HCPProfile)
    
    if name:
        query = query.filter(models.HCPProfile.name.ilike(f"%{name}%"))
    if specialty:
        query = query.filter(models.HCPProfile.specialty.ilike(f"%{specialty}%"))
    if npi:
        query = query.filter(models.HCPProfile.npi_number == npi)
    
    profiles = query.offset(skip).limit(limit).all()
    return profiles

@app.get("/api/hcp-profiles/{profile_id}", response_model=schemas.HCPProfileResponse)
def get_hcp_profile(profile_id: int, db: Session = Depends(get_db)):
    """Get a specific HCP profile by ID."""
    profile = db.query(models.HCPProfile).filter(models.HCPProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="HCP profile not found")
    return profile


# Chat endpoint for AI agent
@app.post("/api/chat", response_model=schemas.ChatResponse)
async def chat(message: schemas.ChatMessage, db: Session = Depends(get_db)):
    """
    Process a chat message through the LangGraph AI agent.
    The agent will determine the appropriate action and return structured data.
    """
    try:
        # Get current interaction data from the request (for editing)
        current_data = message.current_data or {}
        
        # Process the message through the agent
        result = process_user_message(message.message, current_data)
        
        # Handle the action
        if result.get("action") == "create_interaction":
            # Create new interaction in database
            interaction_data = result.get("data", {})
            
            # Convert materials_shared to JSON if it's a list
            materials = interaction_data.get("materials_shared", [])
            
            db_interaction = models.HCPInteraction(
                hcp_name=interaction_data.get("hcp_name"),
                interaction_date=datetime.fromisoformat(interaction_data.get("interaction_date")) if interaction_data.get("interaction_date") else datetime.utcnow(),
                sentiment=interaction_data.get("sentiment"),
                products_discussed=interaction_data.get("products_discussed"),
                materials_shared=materials,
                interaction_type=interaction_data.get("interaction_type"),
                location=interaction_data.get("location"),
                duration_minutes=interaction_data.get("duration_minutes"),
                notes=interaction_data.get("notes"),
                follow_up_date=datetime.fromisoformat(interaction_data.get("follow_up_date")) if interaction_data.get("follow_up_date") else None,
                follow_up_action=interaction_data.get("follow_up_action")
            )
            db.add(db_interaction)
            db.commit()
            db.refresh(db_interaction)
            
            return schemas.ChatResponse(
                response=result.get("response", "Interaction logged successfully!"),
                action="create_interaction",
                data={"interaction_id": db_interaction.id, **interaction_data}
            )
        
        elif result.get("action") == "update_interaction":
            # For update, we need to know which interaction to update
            # In a real app, you'd track this in session state
            # For now, we'll return the update data
            return schemas.ChatResponse(
                response=result.get("response", "Ready to update interaction."),
                action="update_interaction",
                data=result.get("data", {})
            )
        
        elif result.get("action") == "search_interactions":
            # Search for interactions
            search_params = result.get("data", {})
            query = db.query(models.HCPInteraction)
            
            if search_params.get("hcp_name"):
                query = query.filter(models.HCPInteraction.hcp_name.ilike(f"%{search_params['hcp_name']}%"))
            if search_params.get("sentiment"):
                query = query.filter(models.HCPInteraction.sentiment == search_params["sentiment"])
            
            interactions = query.limit(10).all()
            
            return schemas.ChatResponse(
                response=f"Found {len(interactions)} matching interactions.",
                action="search_interactions",
                data={"count": len(interactions), "interactions": [{"id": i.id, "hcp_name": i.hcp_name, "date": str(i.interaction_date)} for i in interactions]}
            )
        
        else:
            # General response
            return schemas.ChatResponse(
                response=result.get("response", "I'm here to help you log interactions."),
                action=result.get("action"),
                data=result.get("data")
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

