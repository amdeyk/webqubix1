# Section 1: Event-related database models
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EventCategory(Base):
    """Event categories like Conference, Medical Conference, etc."""
    __tablename__ = "event_categories"
    
    # Section 2: Primary fields
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))  # CSS class or image path
    
    # Section 3: SEO fields
    meta_title = Column(String(60))
    meta_description = Column(String(160))
    keywords = Column(String(255))
    
    # Section 4: Tracking fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Section 5: Relationships
    services = relationship("Service", back_populates="category")

class Service(Base):
    """Individual services offered by Qubix"""
    __tablename__ = "services"
    
    # Section 2: Primary fields
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("event_categories.id"))
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    short_description = Column(String(300))
    full_description = Column(Text)
    features = Column(Text)  # JSON string of features list
    price_range = Column(String(100))  # e.g., "₹50,000 - ₹2,00,000"
    
    # Section 3: SEO and media fields
    meta_title = Column(String(60))
    meta_description = Column(String(160))
    keywords = Column(String(255))
    image_url = Column(String(500))
    gallery_images = Column(Text)  # JSON string of image URLs
    
    # Section 4: Tracking fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    
    # Section 5: Relationships
    category = relationship("EventCategory", back_populates="services")
    inquiries = relationship("Inquiry", back_populates="service")

class Inquiry(Base):
    """Contact inquiries and quote requests"""
    __tablename__ = "inquiries"
    
    # Section 2: Primary fields
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    
    # Section 3: Contact information
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    company = Column(String(200))
    
    # Section 4: Event details
    event_type = Column(String(100))
    event_date = Column(DateTime)
    location = Column(String(200))
    expected_attendees = Column(Integer)
    budget_range = Column(String(50))
    
    # Section 5: Message and requirements
    message = Column(Text)
    requirements = Column(Text)  # Specific requirements
    
    # Section 6: Tracking fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="new")  # new, contacted, quoted, closed
    is_priority = Column(Boolean, default=False)
    
    # Section 7: Relationships
    service = relationship("Service", back_populates="inquiries")