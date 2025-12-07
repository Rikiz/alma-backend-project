import json
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..models.schemas import LeadOut, StateUpdate
from ..server.lead_dao import list_leads, get_lead, update_lead_state, delete_lead

router = APIRouter()

@router.get("/leads", response_model=List[LeadOut])
def read_leads(skip: int = 0, limit: int = 100):
    return list_leads(skip=skip, limit=limit)

@router.get("/leads/{lead_id}", response_model=LeadOut)
def read_lead(lead_id: int):
    lead = get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.patch("/leads/{lead_id}/state", response_model=LeadOut)
def patch_lead_state(lead_id: int, payload: StateUpdate):
    lead = update_lead_state(lead_id, payload.state)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.delete("/leads/{lead_id}")
def delete_lead_endpoint(lead_id: int):
    if delete_lead(lead_id):
        return {"message": "Lead deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Lead not found")
