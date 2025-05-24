# app/database_seeds.py
# Database seeding script for initial service data
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.events import EventCategory, Service
import json

def create_initial_data():
    """Create initial categories and services data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(EventCategory).count() > 0:
            print("Data already exists. Skipping seed.")
            return
            
        # Create Event Categories
        categories_data = [
            {
                "name": "Conference Management",
                "slug": "conference-management",
                "description": "End-to-end conference planning and management services",
                "icon": "fas fa-users",
                "meta_title": "Conference Management Services - Professional Event Planning",
                "meta_description": "Expert conference management services including venue selection, speaker coordination, registration management, and audio-visual production.",
                "keywords": "conference management, event planning, conference organization, professional conferences"
            },
            {
                "name": "Medical Conferences",
                "slug": "medical-conferences",
                "description": "Specialized medical conference and healthcare event management",
                "icon": "fas fa-user-md",
                "meta_title": "Medical Conference Organization - Healthcare Event Management",
                "meta_description": "Professional medical conference planning services for healthcare institutions, medical societies, and pharmaceutical companies.",
                "keywords": "medical conferences, healthcare events, medical education, CME conferences"
            },
            {
                "name": "Corporate Events",
                "slug": "corporate-events",
                "description": "Corporate event planning and brand activation services",
                "icon": "fas fa-building",
                "meta_title": "Corporate Event Management - Business Event Planning",
                "meta_description": "Comprehensive corporate event management including product launches, annual meetings, team building, and brand activations.",
                "keywords": "corporate events, business events, product launch, annual meetings, team building"
            },
            {
                "name": "Virtual Conferences",
                "slug": "virtual-conferences",
                "description": "Advanced virtual conference platform and hybrid event solutions",
                "icon": "fas fa-laptop",
                "meta_title": "Virtual Conference Platform - Online Event Management",
                "meta_description": "State-of-the-art virtual conference platform with live streaming, interactive features, and hybrid event capabilities.",
                "keywords": "virtual conferences, online events, hybrid conferences, webinar platform"
            },
            {
                "name": "Audio Visual Production",
                "slug": "audio-visual-production",
                "description": "Professional AV production and technical event support",
                "icon": "fas fa-video",
                "meta_title": "Audio Visual Production - Professional AV Services",
                "meta_description": "Complete audio-visual production services including LED walls, sound systems, lighting, and live streaming for events.",
                "keywords": "audio visual production, AV services, LED walls, sound systems, event technology"
            },
            {
                "name": "Themed Events",
                "slug": "themed-events",  
                "description": "Creative themed event design and execution",
                "icon": "fas fa-palette",
                "meta_title": "Themed Event Management - Creative Event Design",
                "meta_description": "Innovative themed event planning including Bollywood, casino, superhero themes with complete décor and entertainment.",
                "keywords": "themed events, creative events, bollywood theme, casino theme, event decoration"
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category = EventCategory(**cat_data)
            db.add(category)
            categories.append(category)
        
        db.commit()
        
        # Create Services
        services_data = [
            # Conference Management Services
            {
                "category_id": 1,
                "name": "Complete Conference Planning & Management",
                "slug": "conference-planning-management",
                "short_description": "End-to-end conference planning from concept to execution with dedicated project management",
                "full_description": """
                <h3>Comprehensive Conference Management Solutions</h3>
                <p>Our complete conference planning and management service covers every aspect of your event from initial concept development to post-event analysis. We handle venue selection, speaker coordination, registration management, catering, audio-visual requirements, and on-site event coordination.</p>
                
                <h4>Our Process</h4>
                <ul>
                    <li>Initial consultation and objective setting</li>
                    <li>Budget planning and venue selection</li>
                    <li>Speaker sourcing and coordination</li>
                    <li>Registration platform setup</li>
                    <li>Marketing and promotional support</li>
                    <li>On-site event management</li>
                    <li>Post-event reporting and analysis</li>
                </ul>
                
                <p>With over 15 years of experience managing conferences across India, we ensure your event achieves its objectives while providing an exceptional experience for all attendees.</p>
                """,
                "features": json.dumps([
                    "Dedicated project manager", "Venue sourcing and negotiation", "Speaker management", 
                    "Registration platform", "Marketing support", "On-site coordination", "Post-event reporting"
                ]),
                "price_range": "₹2,00,000 - ₹50,00,000",
                "meta_title": "Conference Planning & Management Services - Professional Event Planning",
                "meta_description": "Expert conference planning and management services covering venue selection, speaker coordination, registration, and event execution across India.",
                "keywords": "conference planning, event management, conference organization, professional conferences",
                "is_featured": True
            },
            {
                "category_id": 1,
                "name": "Basic Conference Setup",
                "slug": "basic-conference-setup",
                "short_description": "Essential conference setup for small meetings and conferences up to 50 guests",
                "full_description": """
                <h3>Basic Conference Setup Package</h3>
                <p>Perfect for fundamental meetings, conferences and corporate meets with indoor space for approximately 50 individuals. Our basic package provides all essential audio-visual equipment and staging for a professional conference experience.</p>
                
                <h4>Package Inclusions</h4>
                <ul>
                    <li>16 ft x 12 ft x 1.5 ft Stage for speakers</li>
                    <li>Superior quality Hand and Collar Microphones</li>
                    <li>Moveable screen on Tri-pod stand</li>
                    <li>Projector for content screening</li>
                    <li>Basic P.A system with two tops</li>
                    <li>Solid colour vinyl stage backdrop</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Minimum venue required: 1600 sq ft indoor space</p>
                """,
                "features": json.dumps([
                    "Stage setup (16x12x1.5 ft)", "Hand & collar microphones", "Projector & screen",
                    "Basic PA system", "Stage backdrop", "Suitable for 50 guests"
                ]),
                "price_range": "₹27,000 - ₹37,000",
                "meta_title": "Basic Conference Setup - Small Meeting Room Setup",
                "meta_description": "Basic conference setup for small meetings up to 50 guests including stage, microphones, projector and PA system.",
                "keywords": "basic conference setup, small meeting setup, conference equipment rental",
                "is_featured": False
            },
            
            # Medical Conference Services  
            {
                "category_id": 2,
                "name": "Medical Conference Organization",
                "slug": "medical-conference-organization",
                "short_description": "Specialized medical conference planning for healthcare professionals and institutions",
                "full_description": """
                <h3>Medical Conference Organization</h3>
                <p>We specialize in organizing medical conferences, CME programs, and healthcare events for medical societies, hospitals, and pharmaceutical companies. Our team understands the unique requirements of medical education and professional development events.</p>
                
                <h4>Medical Conference Expertise</h4>
                <ul>
                    <li>CME accreditation support</li>
                    <li>Medical expert speaker coordination</li>
                    <li>Pharmaceutical industry compliance</li>
                    <li>Medical equipment exhibitions</li>
                    <li>Live surgery broadcasts</li>
                    <li>Medical education content management</li>
                </ul>
                
                <h4>Our Medical Conference Portfolio</h4>
                <p>We have successfully organized over 200 medical conferences including cardiology, oncology, pediatrics, and surgery conferences across India.</p>
                """,
                "features": json.dumps([
                    "CME accreditation support", "Medical expert speakers", "Live surgery streaming",
                    "Medical exhibition management", "Pharmaceutical compliance", "200+ events organized"
                ]),
                "price_range": "₹5,00,000 - ₹1,00,00,000",
                "meta_title": "Medical Conference Organization - Healthcare Event Management",
                "meta_description": "Professional medical conference organization for CME programs, medical societies, and healthcare institutions with 200+ successful events.",
                "keywords": "medical conferences, CME conferences, healthcare events, medical education",
                "is_featured": True
            },
            
            # Corporate Events
            {
                "category_id": 3,
                "name": "Corporate Event Management",
                "slug": "corporate-event-management",
                "short_description": "Professional corporate event planning including product launches, annual meetings, and team building",
                "full_description": """
                <h3>Corporate Event Management</h3>
                <p>Our corporate event management services help businesses create impactful events that align with their brand objectives. From intimate board meetings to large-scale product launches, we deliver professional event experiences.</p>
                
                <h4>Corporate Event Types</h4>
                <ul>
                    <li>Product launches and brand activations</li>
                    <li>Annual general meetings (AGMs)</li>
                    <li>Team building and employee engagement</li>
                    <li>Awards ceremonies and recognition events</li>
                    <li>Board meetings and executive retreats</li>
                    <li>Sales conferences and training programs</li>
                </ul>
                
                <h4>Why Choose Our Corporate Services</h4>
                <p>We understand corporate culture and business objectives, ensuring every event supports your company's goals while providing memorable experiences for attendees.</p>
                """,
                "features": json.dumps([
                    "Product launch events", "AGM management", "Team building activities",
                    "Awards ceremonies", "Executive retreats", "Sales conferences"
                ]),
                "price_range": "₹1,00,000 - ₹25,00,000",
                "meta_title": "Corporate Event Management - Business Event Planning Services",
                "meta_description": "Professional corporate event management including product launches, annual meetings, team building, and awards ceremonies.",
                "keywords": "corporate events, product launch, annual meetings, team building, business events",
                "is_featured": True
            },
            
            # Virtual Conference Platform
            {
                "category_id": 4,
                "name": "Virtual Conference Platform",
                "slug": "virtual-conference-platform",
                "short_description": "Advanced virtual conference platform with live streaming, interactive features, and hybrid capabilities",
                "full_description": """
                <h3>Virtual Conference Platform</h3>
                <p>Our state-of-the-art virtual conference platform enables you to host engaging online events with interactive features, live streaming, and comprehensive attendee management. Perfect for reaching global audiences.</p>
                
                <h4>Platform Features</h4>
                <ul>
                    <li>HD live streaming and recording</li>
                    <li>Interactive Q&A and polling</li>
                    <li>Virtual networking lounges</li>
                    <li>Digital exhibition halls</li>
                    <li>Multi-session parallel tracks</li>
                    <li>Attendee analytics and reporting</li>
                    <li>Mobile app integration</li>
                </ul>
                
                <h4>Hybrid Event Capabilities</h4>
                <p>Seamlessly combine in-person and virtual attendance for maximum reach and engagement.</p>
                """,
                "features": json.dumps([
                    "HD live streaming", "Interactive Q&A", "Virtual networking", "Digital exhibitions",
                    "Multi-session support", "Analytics dashboard", "Mobile app", "Hybrid capabilities"
                ]),
                "price_range": "₹50,000 - ₹10,00,000",
                "meta_title": "Virtual Conference Platform - Online Event Management Solution",
                "meta_description": "Advanced virtual conference platform with live streaming, interactive features, virtual networking, and hybrid event capabilities.",
                "keywords": "virtual conference platform, online events, live streaming, hybrid conferences",
                "is_featured": True
            },
            
            # Audio Visual Production
            {
                "category_id": 5,
                "name": "Curve LED Backdrop Setup",
                "slug": "curve-led-backdrop-setup",
                "short_description": "Professional curved LED backdrop setup for large conferences and events up to 300 guests",
                "full_description": """
                <h3>Curve LED Backdrop Event Setup</h3>
                <p>Our premium curved LED backdrop setup is perfect for large conferences, corporate meetings, and gala events accommodating up to 300 guests. The highlight of this package is the stunning curved LED screen that creates an immersive visual experience.</p>
                
                <h4>Setup Specifications</h4>
                <ul>
                    <li>36 ft x 24 ft x 2 ft main stage</li>
                    <li>Curved LED screen: 36 ft x 10 ft</li>
                    <li>Professional console setup</li>
                    <li>P.A system with 4 tops and 2 dual base</li>
                    <li>Premium hand and collar microphones (2 pieces)</li>
                    <li>Podium with flexible goose microphone</li>
                    <li>Moving head par cans with goal post truss</li>
                    <li>Professional sound and lighting</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Minimum venue required: 4500 sq ft indoor space</p>
                """,
                "features": json.dumps([
                    "36ft curved LED wall", "Large stage setup", "Professional PA system",
                    "Moving head lighting", "Premium microphones", "Goal post truss", "Up to 300 guests"
                ]),
                "price_range": "₹9,10,000 - ₹16,30,000",
                "meta_title": "Curve LED Backdrop Setup - Professional AV Production",
                "meta_description": "Premium curved LED backdrop setup for large events up to 300 guests with professional audio-visual production.",
                "keywords": "curved LED backdrop, LED wall setup, professional AV, conference technology",
                "is_featured": False
            },
            
            # Themed Events
            {
                "category_id": 6,
                "name": "Bollywood Theme Event",
                "slug": "bollywood-theme-event",
                "short_description": "Vibrant Bollywood themed event setup with colorful décor, celebrity cutouts, and entertainment",
                "full_description": """
                <h3>Bollywood Theme Event Setup</h3>
                <p>Experience the glamour and excitement of Bollywood with our vibrant themed event setup. Perfect for corporate celebrations, award ceremonies, and gala nights that want to capture the spirit of Indian cinema.</p>
                
                <h4>Theme Inclusions</h4>
                <ul>
                    <li>Thematic movie reel entrance arch</li>
                    <li>Red carpet area with bollywood cutouts</li>
                    <li>Vibrant pathway décor with LED blocks</li>
                    <li>Arena décor with bollywood movie banners</li>
                    <li>Magic mirror photo booth</li>
                    <li>Bollywood themed cushions and furniture</li>
                    <li>Food and bar counter setups</li>
                    <li>Professional sound and lighting</li>
                    <li>Stage setup with themed elements</li>
                </ul>
                
                <h4>Entertainment Suggestions</h4>
                <p>We recommend adding Bollywood dance performances, sand art shows, and live music to enhance the experience.</p>
                
                <h4>Venue Requirements</h4>
                <p>Suitable for both indoor and outdoor venues, minimum 4500 sq ft, accommodating up to 300 guests.</p>
                """,
                "features": json.dumps([
                    "Movie reel entrance", "Red carpet area", "Bollywood cutouts", "Magic mirror booth",
                    "Themed furniture", "Professional lighting", "Stage setup", "Up to 300 guests"
                ]),
                "price_range": "₹3,00,000 - ₹8,00,000",
                "meta_title": "Bollywood Theme Event Setup - Indian Cinema Themed Events",
                "meta_description": "Vibrant Bollywood themed event setup with red carpet, celebrity cutouts, magic mirror booth, and professional entertainment.",
                "keywords": "bollywood theme events, indian cinema theme, themed corporate events, bollywood party",
                "is_featured": False
            },
            {
                "category_id": 6,
                "name": "James Bond Theme Event",
                "slug": "james-bond-theme-event", 
                "short_description": "Sophisticated James Bond 007 themed event with luxury elements and spy-themed entertainment",
                "full_description": """
                <h3>James Bond 007 Theme Event</h3>
                <p>Create an exclusive, sophisticated atmosphere with our James Bond themed event setup. Perfect for corporate galas, product launches, and premium events that demand elegance and mystery.</p>
                
                <h4>Premium Theme Inclusions</h4>
                <ul>
                    <li>Grand entrance with white limousine</li>
                    <li>Red carpet with goal post lighting</li>
                    <li>3D life-sized Bond character cutouts</li>
                    <li>Stage with LED backdrop</li>
                    <li>Foreign hostess for VIP escort</li>
                    <li>GOBO projections with 007 themes</li>
                    <li>Themed sofas and lounge areas</li>
                    <li>Photo booth with riser setup</li>
                    <li>Premium sound system (JBL-Vertec)</li>
                    <li>Professional lighting design</li>
                </ul>
                
                <h4>Recommended Additions</h4>
                <ul>
                    <li>Aston Martin car display</li>
                    <li>Casino gaming tables</li>
                    <li>Tuxedo dress code</li>
                    <li>Ice bar with customization</li>
                    <li>Magazine photo booth experience</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Suitable for both indoor and outdoor venues, minimum 3000 sq ft, accommodating up to 200 guests.</p>
                """,
                "features": json.dumps([
                    "Limousine entrance", "3D Bond cutouts", "GOBO projections", "Foreign hostess",
                    "LED backdrop stage", "Premium sound system", "Professional lighting", "VIP experience"
                ]),
                "price_range": "₹8,00,000 - ₹18,00,000",
                "meta_title": "James Bond Theme Event - Luxury 007 Themed Corporate Events",
                "meta_description": "Sophisticated James Bond 007 themed events with limousine entrance, premium setups, and luxury entertainment elements.",
                "keywords": "james bond theme, 007 events, luxury themed events, spy theme party, corporate gala",
                "is_featured": True
            }
        ]
        
        for service_data in services_data:
            service = Service(**service_data)
            db.add(service)
        
        db.commit()
        print(f"Successfully created {len(categories_data)} categories and {len(services_data)} services")
        
    except Exception as e:
        print(f"Error creating initial data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_data()