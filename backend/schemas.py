from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class InteractionBase(BaseModel):
    hcp_name: str
    interaction_date: Optional[datetime] = None
    sentiment: Optional[str] = None
    products_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = None
    interaction_type: Optional[str] = None
    location: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    follow_up_action: Optional[str] = None

class InteractionCreate(InteractionBase):
    pass

class InteractionUpdate(BaseModel):
    hcp_name: Optional[str] = None
    interaction_date: Optional[datetime] = None
    sentiment: Optional[str] = None
    products_discussed: Optional[str] = None
    materials_shared: Optional[List[str]] = None
    interaction_type: Optional[str] = None
    location: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    follow_up_action: Optional[str] = None

class InteractionResponse(InteractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    current_data: Optional[Dict[str, Any]] = None  # Current form data for editing

class ChatResponse(BaseModel):
    response: str
    action: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

# HCP Profile schemas
class HCPProfileBase(BaseModel):
    npi_number: Optional[str] = None
    name: str
    specialty: Optional[str] = None
    tier: Optional[str] = None
    institution: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class HCPProfileCreate(HCPProfileBase):
    pass

class HCPProfileResponse(HCPProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    role: Optional[str] = "field_rep"
    territory: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True

