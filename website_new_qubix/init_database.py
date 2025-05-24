#!/usr/bin/env python3
"""
Database initialization script for Qubix Events website
Run this script to create the database and populate it with initial data
"""

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.events import EventCategory, Service
import json

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def seed_basic_data():
    """Seed the database with basic categories and services"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(EventCategory).count() > 0:
            print("Database already contains data. Skipping seed.")
            return
        
        print("Seeding database with initial data...")
        
        # Create categories
        categories = [
            EventCategory(
                name="Conference Management",
                slug="conference-management",
                description="End-to-end conference planning and management services",
                icon="fas fa-users",
                meta_title="Conference Management Services",
                meta_description="Professional conference planning and management services",
                keywords="conference management, event planning",
                is_active=True
            ),
            EventCategory(
                name="Medical Conferences",
                slug="medical-conferences", 
                description="Specialized medical conference and healthcare event management",
                icon="fas fa-user-md",
                meta_title="Medical Conference Organization",
                meta_description="Professional medical conference planning services",
                keywords="medical conferences, healthcare events",
                is_active=True
            ),
            EventCategory(
                name="Virtual Conferences",
                slug="virtual-conferences",
                description="Advanced virtual conference platform and hybrid event solutions", 
                icon="fas fa-laptop",
                meta_title="Virtual Conference Platform",
                meta_description="Advanced virtual conference platform with live streaming",
                keywords="virtual conferences, online events",
                is_active=True
            ),
            EventCategory(
                name="Themed Events",
                slug="themed-events",
                description="Creative themed event design and execution",
                icon="fas fa-palette", 
                meta_title="Themed Event Management",
                meta_description="Creative themed event planning and execution",
                keywords="themed events, creative events",
                is_active=True
            )
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        
        # Create services
        services = [
            Service(
                category_id=1,
                name="Complete Conference Planning",
                slug="complete-conference-planning",
                short_description="End-to-end conference planning from concept to execution",
                full_description="<p>Comprehensive conference planning and management service covering every aspect of your event.</p>",
                features=json.dumps(["Venue selection", "Speaker coordination", "Registration management", "Audio-visual setup"]),
                price_range="₹2,00,000 - ₹50,00,000",
                meta_title="Complete Conference Planning Services",
                meta_description="Professional conference planning from concept to execution",
                keywords="conference planning, event management",
                is_active=True,
                is_featured=True
            ),
            Service(
                category_id=1,
                name="Basic Conference Setup",
                slug="basic-conference-setup",
                short_description="Essential conference setup for small meetings up to 50 guests",
                full_description="<p>Perfect for small meetings and conferences with basic audio-visual equipment.</p>",
                features=json.dumps(["16x12 ft stage", "Hand & collar mics", "Projector & screen", "Basic PA system"]),
                price_range="₹27,000 - ₹37,000",
                meta_title="Basic Conference Setup Services",
                meta_description="Basic conference setup for small meetings up to 50 guests",
                keywords="basic conference setup, small meeting room",
                is_active=True,
                is_featured=True
            ),
            Service(
                category_id=2,
                name="Medical Conference Organization",
                slug="medical-conference-organization",
                short_description="Specialized medical conference planning for healthcare professionals",
                full_description="<p>Professional medical conference organization with CME accreditation support.</p>",
                features=json.dumps(["CME accreditation", "Medical expert speakers", "Live surgery streaming", "Medical exhibitions"]),
                price_range="₹5,00,000 - ₹1,00,00,000",
                meta_title="Medical Conference Organization",
                meta_description="Professional medical conference planning services",
                keywords="medical conferences, CME conferences, healthcare events",
                is_active=True,
                is_featured=True
            ),
            Service(
                category_id=3,
                name="Virtual Conference Platform",
                slug="virtual-conference-platform",
                short_description="Advanced virtual conference platform with live streaming and interactive features",
                full_description="<p>State-of-the-art virtual conference platform for online and hybrid events.</p>",
                features=json.dumps(["HD live streaming", "Interactive Q&A", "Virtual networking", "Digital exhibitions"]),
                price_range="₹50,000 - ₹10,00,000",
                meta_title="Virtual Conference Platform",
                meta_description="Advanced virtual conference platform with live streaming",
                keywords="virtual conferences, online events, live streaming",
                is_active=True,
                is_featured=True
            ),
            Service(
                category_id=4,
                name="Bollywood Theme Event",
                slug="bollywood-theme-event",
                short_description="Vibrant Bollywood themed event with colorful décor and entertainment",
                full_description="<p>Experience the glamour of Bollywood with our vibrant themed event setup.</p>",
                features=json.dumps(["Red carpet entrance", "Bollywood cutouts", "Magic mirror booth", "Themed entertainment"]),
                price_range="₹3,00,000 - ₹8,00,000",
                meta_title="Bollywood Theme Event Setup",
                meta_description="Vibrant Bollywood themed events with professional entertainment",
                keywords="bollywood theme, indian cinema events, themed parties",
                is_active=True,
                is_featured=True
            ),
            Service(
                category_id=4,
                name="James Bond Theme Event",
                slug="james-bond-theme-event",
                short_description="Sophisticated James Bond 007 themed event with luxury elements",
                full_description="<p>Create an exclusive James Bond experience with luxury setups and entertainment.</p>",
                features=json.dumps(["Limousine entrance", "3D Bond cutouts", "Casino tables", "Premium entertainment"]),
                price_range="₹8,00,000 - ₹18,00,000",
                meta_title="James Bond 007 Theme Event",
                meta_description="Sophisticated James Bond themed corporate events",
                keywords="james bond theme, 007 events, luxury corporate events",
                is_active=True,
                is_featured=True
            )
        ]
        
        for service in services:
            db.add(service)
        
        db.commit()
        print(f"Successfully created {len(categories)} categories and {len(services)} services!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Main function to initialize the database"""
    print("Initializing Qubix Events database...")
    
    try:
        create_tables()
        seed_basic_data()
        print("Database initialization completed successfully!")
        print("\nYou can now run the application with:")
        print("uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()