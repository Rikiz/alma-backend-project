from sqlalchemy import select, update
from ..models.models import Lead
from ..models.enums import LeadState
from typing import List, Optional
from ..database.db import SessionLocal
from datetime import datetime
from ..services.storage_service import delete_resume_file

def create_lead(first_name: str, last_name: str, email: str, resume_path: Optional[str]):
    with SessionLocal() as session:
        lead = Lead(first_name=first_name, last_name=last_name, email=email, resume_path=resume_path, state=LeadState.PENDING)
        session.add(lead)
        session.commit()
        session.refresh(lead)
        return lead

def get_lead(lead_id: int):
    with SessionLocal() as session:
        q = select(Lead).where(Lead.id == lead_id)
        res = session.execute(q)
        return res.scalars().first()

def get_lead_by_email(email: str):
    with SessionLocal() as session:
        q = select(Lead).where(Lead.email == email)
        res = session.execute(q)
        return res.scalars().first()

def list_leads(skip: int = 0, limit: int = 100):
    with SessionLocal() as session:
        q = select(Lead).order_by(Lead.created_at.desc()).offset(skip).limit(limit)
        res = session.execute(q)
        return res.scalars().all()

def update_lead_state(lead_id: int, new_state: LeadState):
    with SessionLocal() as session:
        q = update(Lead).where(Lead.id == lead_id).values(state=new_state)
        session.execute(q)
        session.commit()
        return get_lead(lead_id)

def update_lead(lead_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, resume_path: Optional[str] = None):
    with SessionLocal() as session:
        update_data = {}
        if first_name is not None:
            update_data['first_name'] = first_name
        if last_name is not None:
            update_data['last_name'] = last_name
        if resume_path is not None:
            update_data['resume_path'] = resume_path
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            q = update(Lead).where(Lead.id == lead_id).values(**update_data)
            session.execute(q)
            session.commit()
        return get_lead(lead_id)

def delete_lead(lead_id: int):
    with SessionLocal() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if lead:
            if lead.resume_path:
                delete_resume_file(lead.resume_path)
            session.delete(lead)
            session.commit()
            return True
        return False
