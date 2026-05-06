from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="field_rep")  # field_rep, manager, admin
    territory = Column(String(255))
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HCPProfile(Base):
    __tablename__ = "hcp_profiles"

    id = Column(Integer, primary_key=True, index=True)
    npi_number = Column(String(10), unique=True, index=True)  # National Provider Identifier
    name = Column(String(255), nullable=False)
    specialty = Column(String(255))
    tier = Column(String(50))  # A, B, C tier classification
    institution = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    prescribing_history = Column(JSON)  # Historical prescribing data
    last_interaction_date = Column(DateTime)
    compliance_flags = Column(JSON)  # Any compliance-related flags
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HCPInteraction(Base):
    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey('hcp_profiles.id'), nullable=True)
    hcp_name = Column(String(255), nullable=False)
    rep_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    interaction_date = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String(50))  # positive, negative, neutral
    sentiment_score = Column(Float)  # 1-5 scale
    products_discussed = Column(Text)
    materials_shared = Column(JSON)  # List of materials like brochures, samples
    interaction_type = Column(String(100))  # Meeting, Call, Email, Conference
    location = Column(String(255))
    duration_minutes = Column(Integer)
    notes = Column(Text)  # Raw notes from user
    llm_summary = Column(Text)  # LLM-generated summary
    follow_up_date = Column(DateTime, nullable=True)
    follow_up_action = Column(Text, nullable=True)
    compliance_status = Column(String(50), default="pending")  # pending, approved, flagged
    compliance_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hcp_profile = relationship("HCPProfile", backref="interactions")
    rep = relationship("User", backref="interactions")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey('hcp_interactions.id'), nullable=False)
    editor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(50))  # create, update, delete
    field_diffs = Column(JSON)  # Field-level differences
    old_values = Column(JSON)
    new_values = Column(JSON)
    reason = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interaction = relationship("HCPInteraction", backref="audit_logs")
    editor = relationship("User", backref="audit_logs")

