# Section 1: API endpoints for form submissions and data
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

from app.database import get_db
from app.models.events import Inquiry, Service
from app.services.email_service import EmailService

router = APIRouter()
email_service = EmailService()

# Section 2: Pydantic models for request validation
class ContactForm(BaseModel):
    """Contact form submission model"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    service_id: Optional[int] = None
    event_type: Optional[str] = None
    event_date: Optional[datetime.date] = None
    location: Optional[str] = None
    expected_attendees: Optional[int] = None
    budget_range: Optional[str] = None
    message: str
    requirements: Optional[str] = None

class QuoteRequest(BaseModel):
    """Quote request form model"""
    name: str
    email: EmailStr
    phone: str
    company: str
    service_id: int
    event_date: datetime.date
    location: str
    expected_attendees: int
    budget_range: str
    requirements: str

# Section 3: Contact form submission endpoint
@router.post("/contact")
async def submit_contact_form(
    form_data: ContactForm,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle contact form submissions"""
    try:
        # Section 4: Create inquiry record
        inquiry = Inquiry(
            service_id=form_data.service_id,
            name=form_data.name,
            email=form_data.email,
            phone=form_data.phone,
            company=form_data.company,
            event_type=form_data.event_type,
            event_date=form_data.event_date,
            location=form_data.location,
            expected_attendees=form_data.expected_attendees,
            budget_range=form_data.budget_range,
            message=form_data.message,
            requirements=form_data.requirements,
            status="new"
        )
        
        db.add(inquiry)
        db.commit()
        db.refresh(inquiry)
        
        # Section 5: Send notification emails in background
        background_tasks.add_task(
            email_service.send_inquiry_notification,
            inquiry.id,
            form_data.dict()
        )
        
        background_tasks.add_task(
            email_service.send_confirmation_email,
            form_data.email,
            form_data.name
        )
        
        return {
            "success": True,
            "message": "Thank you for your inquiry. We'll get back to you within 24 hours.",
            "inquiry_id": inquiry.id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to submit inquiry. Please try again.")

# Section 6: Quote request endpoint
@router.post("/quote")
async def submit_quote_request(
    quote_data: QuoteRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle quote request submissions"""
    try:
        # Verify service exists
        service = db.query(Service).filter(Service.id == quote_data.service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # Create high-priority inquiry
        inquiry = Inquiry(
            service_id=quote_data.service_id,
            name=quote_data.name,
            email=quote_data.email,
            phone=quote_data.phone,
            company=quote_data.company,
            event_date=quote_data.event_date,
            location=quote_data.location,
            expected_attendees=quote_data.expected_attendees,
            budget_range=quote_data.budget_range,
            requirements=quote_data.requirements,
            status="new",
            is_priority=True
        )
        
        db.add(inquiry)
        db.commit()
        db.refresh(inquiry)
        
        # Send priority notification
        background_tasks.add_task(
            email_service.send_quote_request_notification,
            inquiry.id,
            quote_data.dict()
        )
        
        return {
            "success": True,
            "message": "Quote request submitted successfully. Our team will contact you within 6 hours.",
            "inquiry_id": inquiry.id
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to submit quote request. Please try again.")

# Section 7: Get services endpoint
@router.get("/services")
async def get_services(db: Session = Depends(get_db)):
    """Get all active services for forms"""
    services = db.query(Service).filter(Service.is_active == True).all()
    return [
        {
            "id": service.id,
            "name": service.name,
            "category": service.category.name if service.category else "General"
        }
        for service in services
    ]