from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException, Form
from ..models.schemas import LeadOut, LeadForm, LeadUpdate
from ..server.lead_dao import create_lead, get_lead_by_email, update_lead, get_lead
from ..database.db import SessionLocal
from ..services.storage_service import save_resume_file
from ..services.email_service import notify_on_new_lead, EmailError
from pydantic import ValidationError
import asyncio
import logging

logger = logging.getLogger(__name__)

async def _send_notifications_safe(lead):
    """Wrapper to send notifications with proper error handling."""
    try:
        await notify_on_new_lead(lead)
    except EmailError as e:
        logger.error(f"Email notification failed for lead {lead.id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during email notification for lead {lead.id}: {e}")

router = APIRouter()

@router.post("/create_leads", response_model=LeadOut)
async def submit_lead(
    lead_form: LeadForm = Depends(LeadForm.as_form), 
    resume: UploadFile | None = File(None)
):

    # Check if user already exists
    existing_lead = get_lead_by_email(lead_form.email)
    if existing_lead:
        raise HTTPException(status_code=400, detail="A lead with this email already exists")

    with SessionLocal() as db:
        try:
            resume_path = None
            if resume:
                # save file async
                resume_path = await save_resume_file(resume)

            lead = create_lead(
                first_name=lead_form.first_name,
                last_name=lead_form.last_name,
                email=lead_form.email,
                resume_path=resume_path
            )

            # schedule background notifications (create asyncio task)
            asyncio.create_task(_send_notifications_safe(lead))

            return lead
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating lead: {str(e)}")

@router.put("/update_leads/{lead_id}", response_model=LeadOut)
async def update_lead_endpoint(
    lead_id: int,
    first_name: str = Form(None, min_length=1, max_length=128),
    last_name: str = Form(None, min_length=1, max_length=128),
    resume: UploadFile | None = File(None)
):
    try:
        lead_update = LeadUpdate(first_name=first_name, last_name=last_name)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    # Check if lead exists
    existing_lead = get_lead(lead_id)
    if not existing_lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    resume_path = None
    if resume:
        # save file async
        resume_path = await save_resume_file(resume)

    # Update lead
    updated_lead = update_lead(
        lead_id=lead_id,
        first_name=lead_update.first_name,
        last_name=lead_update.last_name,
        resume_path=resume_path
    )

    if not updated_lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return updated_lead
