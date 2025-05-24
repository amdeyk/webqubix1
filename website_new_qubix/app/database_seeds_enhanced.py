# app/database_seeds_enhanced.py
# Enhanced database seeding with MICEkart physical event services
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.events import EventCategory, Service
import json

def create_enhanced_data():
    """Create enhanced categories and services data including MICEkart physical events"""
    
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
        
        # Create Enhanced Services including MICEkart physical events
        services_data = [
            # Conference Management Services
            {
                "category_id": 1,
                "name": "Basic Conference Setup",
                "slug": "basic-conference-setup",
                "short_description": "Essential conference setup for small meetings and conferences up to 50 guests with professional AV equipment",
                "full_description": """
                <h3>Basic Conference Setup Package</h3>
                <p>Perfect for fundamental meetings, conferences and corporate meets with indoor space for approximately 50 individuals. Our basic package provides all essential audio-visual equipment and staging for a professional conference experience.</p>
                
                <h4>Package Inclusions</h4>
                <ul>
                    <li><strong>Stage Setup:</strong> 16 ft x 12 ft x 1.5 ft elevated stage for speakers</li>
                    <li><strong>Audio Equipment:</strong> Superior quality hand and collar microphones</li>
                    <li><strong>Visual Display:</strong> Moveable screen on tri-pod stand with projector</li>
                    <li><strong>Sound System:</strong> Basic P.A system with two tops</li>
                    <li><strong>Backdrop:</strong> Solid colour vinyl stage backdrop (16 x 8 feet)</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Minimum venue required: 1600 sq ft indoor space</p>
                
                <h4>Additional Services Available</h4>
                <p>Laptop rental, clicker, pointer, standee, internet connection, additional microphones, photography, and videography services available at additional cost.</p>
                """,
                "features": json.dumps([
                    "16x12x1.5 ft stage setup", "Hand & collar microphones", "Projector & moveable screen",
                    "Basic PA system with 2 tops", "16x8 ft stage backdrop", "Suitable for 50 guests",
                    "Indoor venue setup", "Professional audio-visual equipment"
                ]),
                "price_range": "₹27,000 - ₹37,000",
                "meta_title": "Basic Conference Setup - Small Meeting Room AV Setup | Qubix Events",
                "meta_description": "Basic conference setup for small meetings up to 50 guests including stage, microphones, projector, PA system and backdrop. Professional AV equipment rental.",
                "keywords": "basic conference setup, small meeting setup, conference equipment rental, AV setup, stage rental",
                "is_featured": True
            },
            
            # Advanced AV Production Services
            {
                "category_id": 5,
                "name": "Curve LED Backdrop Setup",
                "slug": "curve-led-backdrop-setup",
                "short_description": "Premium curved LED backdrop setup for large conferences and events up to 300 guests with immersive visual experience",
                "full_description": """
                <h3>Curve LED Backdrop Event Setup</h3>
                <p>Our premium curved LED backdrop setup is designed for large conferences, corporate meetings, and gala events accommodating up to 300 guests. The highlight of this package is the stunning 36-foot curved LED screen that creates an immersive visual experience for your audience.</p>
                
                <h4>Technical Specifications</h4>
                <ul>
                    <li><strong>Main Stage:</strong> 36 ft x 24 ft x 2 ft professional stage setup</li>
                    <li><strong>Curved LED Wall:</strong> 36 ft x 10 ft high-resolution curved LED display</li>
                    <li><strong>Audio System:</strong> Professional P.A system with 4 tops and 2 dual base</li>
                    <li><strong>Microphones:</strong> Premium hand and collar microphones (2 pieces each)</li>
                    <li><strong>Podium:</strong> Professional podium with flexible goose microphone</li>
                    <li><strong>Lighting:</strong> Moving head par cans with goal post truss setup</li>
                    <li><strong>Control:</strong> Professional console for equipment management</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Minimum venue required: 4500 sq ft indoor space</p>
                
                <h4>Perfect For</h4>
                <ul>
                    <li>Large corporate conferences and meetings</li>
                    <li>Product launches and brand activations</li>
                    <li>Awards ceremonies and gala events</li>
                    <li>Medical conferences and symposiums</li>
                </ul>
                """,
                "features": json.dumps([
                    "36ft curved LED wall", "Large stage setup (36x24x2 ft)", "Professional PA system (4 tops, 2 dual base)",
                    "Moving head lighting system", "Premium microphones", "Goal post truss lighting", 
                    "Professional console", "Up to 300 guests", "High-resolution display"
                ]),
                "price_range": "₹9,10,000 - ₹16,30,000",
                "meta_title": "Curved LED Backdrop Setup - Premium AV Production | Qubix Events",
                "meta_description": "Premium curved LED backdrop setup for large events up to 300 guests. 36ft LED wall with professional audio-visual production and lighting.",
                "keywords": "curved LED backdrop, LED wall setup, professional AV production, conference technology, large event setup",
                "is_featured": True
            },
            
            {
                "category_id": 5,
                "name": "Hanging LED Event Setup",
                "slug": "hanging-led-event-setup",
                "short_description": "Elite hanging LED setup with multiple screens and advanced lighting for prestigious conferences up to 300 guests",
                "full_description": """
                <h3>Hanging LED Event Setup</h3>
                <p>Our most sophisticated audio-visual setup designed for elite conferences and prestigious corporate events. This comprehensive package features multiple LED screens, advanced lighting systems, and professional audio equipment for up to 300 guests.</p>
                
                <h4>Complete Setup Specifications</h4>
                <ul>
                    <li><strong>Main Stage:</strong> 30 ft x 20 ft x 2 ft professional stage with on-stage sharpies</li>
                    <li><strong>Center LED Display:</strong> 14 ft x 8 ft high-resolution LED screen with riser (14x4x2 ft)</li>
                    <li><strong>Side LED Wings:</strong> 6 wings of 2 ft x 10 ft LED panels with black masking</li>
                    <li><strong>Side LED Walls:</strong> Two 8 ft x 6 ft LED screens on goal post truss</li>
                    <li><strong>Audio System:</strong> Professional P.A system with 4 tops and 2 bases</li>
                    <li><strong>Lighting System:</strong> 4 T-truss with sharpies and par cans, goal post truss with lighting</li>
                    <li><strong>Special Effects:</strong> Blinders (2) on each goal post for dramatic effect</li>
                    <li><strong>Control Systems:</strong> Professional console and DJ console</li>
                </ul>
                
                <h4>Technical Advantages</h4>
                <ul>
                    <li>360-degree visual coverage for maximum impact</li>
                    <li>Multiple viewing angles ensure visibility from any seat</li>
                    <li>Professional-grade lighting creates ambiance</li>
                    <li>Comprehensive audio coverage throughout venue</li>
                </ul>
                
                <h4>Ideal For</h4>
                <ul>
                    <li>High-profile corporate conferences</li>
                    <li>International business summits</li>
                    <li>Premium product launches</li>
                    <li>Award ceremonies and galas</li>
                </ul>
                """,
                "features": json.dumps([
                    "30x20x2 ft main stage", "14x8 ft center LED screen", "6 side LED wings (2x10 ft each)",
                    "Two 8x6 ft side LED walls", "Professional PA system", "Advanced lighting with sharpies",
                    "Goal post truss setup", "Blinder effects", "Professional control consoles", "Up to 300 guests"
                ]),
                "price_range": "₹10,20,000 - ₹21,00,000",
                "meta_title": "Hanging LED Event Setup - Elite AV Production | Qubix Events",
                "meta_description": "Elite hanging LED event setup with multiple screens, advanced lighting, and professional audio for prestigious conferences up to 300 guests.",
                "keywords": "hanging LED setup, elite AV production, multiple LED screens, professional lighting, premium conference setup",
                "is_featured": True
            },
            
            # Themed Events from MICEkart
            {
                "category_id": 6,
                "name": "Bollywood Theme Event",
                "slug": "bollywood-theme-event",
                "short_description": "Vibrant Bollywood themed event setup with colorful décor, celebrity cutouts, red carpet experience, and entertainment",
                "full_description": """
                <h3>Bollywood Theme Event Setup</h3>
                <p>Experience the glamour and excitement of Bollywood with our vibrant themed event setup. Perfect for corporate celebrations, award ceremonies, and gala nights that want to capture the spirit and energy of Indian cinema.</p>
                
                <h4>Complete Theme Inclusions</h4>
                <ul>
                    <li><strong>Grand Entrance:</strong> Thematic movie reel entrance arch with bollywood aesthetics</li>
                    <li><strong>Red Carpet Experience:</strong> Professional red carpet area with bollywood celebrity cutouts</li>
                    <li><strong>Pathway Décor:</strong> Vibrant LED blocks and movie banners creating cinematic walkways</li>
                    <li><strong>Arena Décor:</strong> Bollywood movie posters, film reels, and themed backdrops</li>
                    <li><strong>Photo Experiences:</strong> Magic mirror photo booth and multiple photo opportunity zones</li>
                    <li><strong>Furniture & Seating:</strong> Bollywood themed silk cushions and colorful furniture</li>
                    <li><strong>Food & Bar Setup:</strong> Themed food stalls and bar counters with movie-inspired designs</li>
                    <li><strong>Stage & Entertainment:</strong> Professional stage setup with themed elements</li>
                    <li><strong>Audio Visual:</strong> Professional sound and lighting systems</li>
                </ul>
                
                <h4>Entertainment Recommendations</h4>
                <ul>
                    <li>Professional Bollywood dance performances</li>
                    <li>Live sand art shows with bollywood themes</li>
                    <li>DJ playing bollywood hits and remixes</li>
                    <li>Celebrity look-alike entertainers</li>
                    <li>Traditional and fusion dance groups</li>
                </ul>
                
                <h4>Venue Specifications</h4>
                <p>Suitable for both indoor and outdoor venues, minimum 4500 sq ft, accommodating up to 300 guests</p>
                
                <h4>Perfect For</h4>
                <ul>
                    <li>Corporate annual celebrations</li>
                    <li>Product launches with Indian themes</li>
                    <li>Award ceremonies and recognition events</li>
                    <li>Cultural festivals and celebrations</li>
                </ul>
                """,
                "features": json.dumps([
                    "Movie reel entrance arch", "Red carpet with celebrity cutouts", "LED pathway décor", 
                    "Magic mirror photo booth", "Bollywood themed furniture", "Professional stage setup",
                    "Themed food & bar counters", "Professional sound & lighting", "Up to 300 guests",
                    "Indoor/outdoor flexibility"
                ]),
                "price_range": "₹3,00,000 - ₹8,00,000",
                "meta_title": "Bollywood Theme Event Setup - Indian Cinema Themed Corporate Events | Qubix",
                "meta_description": "Vibrant Bollywood themed event setup with red carpet, celebrity cutouts, magic mirror booth, themed décor and professional entertainment for corporate celebrations.",
                "keywords": "bollywood theme events, indian cinema theme, themed corporate events, bollywood party, red carpet events",
                "is_featured": True
            },
            
            {
                "category_id": 6,
                "name": "James Bond 007 Theme Event",
                "slug": "james-bond-theme-event",
                "short_description": "Sophisticated James Bond 007 themed event with luxury elements, spy-themed entertainment, and premium setups",
                "full_description": """
                <h3>James Bond 007 Theme Event</h3>
                <p>Create an exclusive, sophisticated atmosphere with our James Bond themed event setup. Perfect for corporate galas, product launches, and premium events that demand elegance, mystery, and luxury.</p>
                
                <h4>Premium Theme Inclusions</h4>
                <ul>
                    <li><strong>Grand Entrance:</strong> White limousine at entrance with professional ramp setup</li>
                    <li><strong>Red Carpet Experience:</strong> VIP red carpet with foreign hostess escort service</li>
                    <li><strong>Character Elements:</strong> 3D life-sized Bond character cutouts strategically placed</li>
                    <li><strong>Stage Production:</strong> Professional stage with LED backdrop and premium lighting</li>
                    <li><strong>Audio Enhancement:</strong> RCF sound system for award ceremonies and announcements</li>
                    <li><strong>Visual Effects:</strong> GOBO projections with 007 themes and spy elements</li>
                    <li><strong>Lounge Areas:</strong> Themed sofas and sophisticated seating arrangements</li>
                    <li><strong>Photo Opportunities:</strong> Professional photo booth with riser and spy-themed props</li>
                    <li><strong>Technical Setup:</strong> Box truss system and professional sound (JBL-Vertec)</li>
                    <li><strong>Ambiance Lighting:</strong> Sophisticated lighting design with light décor stands</li>
                </ul>
                
                <h4>Luxury Additions Available</h4>
                <ul>
                    <li>Aston Martin DB10 car display for authentic Bond experience</li>
                    <li>Professional casino gaming tables (Poker, Blackjack, Roulette)</li>
                    <li>Ice bar with 007 customization and premium spirits</li>
                    <li>Magazine-style photo booth for glamour shots</li>
                    <li>Interactive dance floor with spy-themed entertainment</li>
                    <li>Customized 007 invitations and hampers</li>
                </ul>
                
                <h4>Dress Code & Experience</h4>
                <p>Recommended dress code: Elegant tuxedos and evening gowns. Create an authentic Bond experience with sophisticated ambiance and premium service.</p>
                
                <h4>Venue Requirements</h4>
                <p>Suitable for both indoor and outdoor venues, minimum 3000 sq ft, accommodating up to 200 guests</p>
                """,
                "features": json.dumps([
                    "Limousine entrance display", "3D Bond character cutouts", "GOBO projections", 
                    "Foreign hostess service", "LED backdrop stage", "Premium JBL-Vertec sound", 
                    "Professional lighting design", "VIP red carpet experience", "Luxury lounge setup",
                    "Casino gaming options"
                ]),
                "price_range": "₹8,00,000 - ₹18,00,000",
                "meta_title": "James Bond 007 Theme Event - Luxury Spy Themed Corporate Events | Qubix",
                "meta_description": "Sophisticated James Bond 007 themed events with limousine entrance, premium setups, casino elements, and luxury entertainment for corporate galas.",
                "keywords": "james bond theme, 007 events, luxury themed events, spy theme party, corporate gala, casino theme",
                "is_featured": True
            },
            
            {
                "category_id": 6,
                "name": "Casino Theme Event",
                "slug": "casino-theme-event",
                "short_description": "Glamorous casino themed event with Las Vegas style setup, gaming tables, and premium entertainment",
                "full_description": """
                <h3>Casino Theme Event Setup</h3>
                <p>Bring the glamour and excitement of Las Vegas to your corporate event with our casino themed setup. Experience the thrill of Monte Carlo and the glitz of Atlantic City without the financial risk - perfect for corporate entertainment and team building.</p>
                
                <h4>Casino Theme Inclusions</h4>
                <ul>
                    <li><strong>Themed Entrance:</strong> Casino-style entrance gate with playing card and dice decorations</li>
                    <li><strong>Gaming Elements:</strong> Professional casino cutouts including roulette wheels, blackjack tables, and card symbols</li>
                    <li><strong>Photo Experiences:</strong> Casino-themed photo booth with props and King/Queen of Hearts backdrops</li>
                    <li><strong>Arena Décor:</strong> Las Vegas style decorations with neon-inspired elements</li>
                    <li><strong>Bar Setup:</strong> Themed bar counter designed like a casino lounge</li>
                    <li><strong>Table Centerpieces:</strong> Casino-inspired centerpieces with cards, chips, and dice</li>
                    <li><strong>Stage Setup:</strong> Professional stage with casino-themed elements</li>
                    <li><strong>LED Dance Floor:</strong> Interactive LED dance floor for evening entertainment</li>
                    <li><strong>DJ Console:</strong> Professional DJ setup with casino-themed masking</li>
                    <li><strong>Audio Visual:</strong> Professional sound and lighting systems</li>
                </ul>
                
                <h4>Gaming Experience</h4>
                <ul>
                    <li>Professional casino gaming tables (no real money - fun chips only)</li>
                    <li>Poker, Roulette, Baccarat, Blackjack, and Craps tables</li>
                    <li>Professional dealers and gaming staff</li>
                    <li>Prize distribution based on chip winnings</li>
                </ul>
                
                <h4>Dress Code & Atmosphere</h4>
                <p>Recommended dress code: Suits and elegant evening wear to match the sophisticated casino atmosphere. Create a James Bond-style casino royale experience.</p>
                
                <h4>Venue Requirements</h4>
                <p>Indoor venue preferred, minimum 3000 sq ft, accommodating up to 200 guests</p>
                """,
                "features": json.dumps([
                    "Casino-themed entrance gate", "Professional gaming table setups", "Photo booth with casino props",
                    "LED dance floor", "Themed bar counter", "Casino centerpieces", "Professional dealers",
                    "Stage with casino elements", "Professional sound & lighting", "Up to 200 guests"
                ]),
                "price_range": "₹3,00,000 - ₹7,00,000",
                "meta_title": "Casino Theme Event Setup - Las Vegas Style Corporate Entertainment | Qubix",
                "meta_description": "Glamorous casino themed corporate events with professional gaming tables, Las Vegas style décor, LED dance floor, and premium entertainment.",
                "keywords": "casino theme events, las vegas theme party, corporate casino night, themed entertainment, gaming events",
                "is_featured": False
            },
            
            {
                "category_id": 6,
                "name": "Egyptian Theme Event",
                "slug": "egyptian-theme-event",
                "short_description": "Mystical Egyptian themed event with pharaoh decorations, ancient artifacts, and cultural entertainment",
                "full_description": """
                <h3>Egyptian Theme Event Setup</h3>
                <p>Transport your guests to the fascinating world of ancient Egypt with our mystical Egyptian themed event setup. Perfect for clients seeking an elegant cultural theme that combines history, mystery, and sophistication.</p>
                
                <h4>Egyptian Theme Inclusions</h4>
                <ul>
                    <li><strong>Grand Entrance:</strong> Majestic Egyptian arch with Anubis statue and golden carpet</li>
                    <li><strong>Cultural Elements:</strong> Pharaoh decorations, pyramids, and hieroglyphic displays</li>
                    <li><strong>Artifacts Display:</strong> Ancient Egyptian inspired artifacts and tomb replicas</li>
                    <li><strong>Photo Booth:</strong> Egyptian themed photo opportunities with pharaoh props</li>
                    <li><strong>Arena Décor:</strong> Sand-colored decorations with pyramid and sphinx elements</li>
                    <li><strong>Bar Setup:</strong> Themed bar counter with Egyptian motifs and designs</li>
                    <li><strong>Table Centerpieces:</strong> Egyptian inspired centerpieces with golden elements</li>
                    <li><strong>Visual Effects:</strong> GOBO projections of Egyptian monuments on walls</li>
                    <li><strong>Stage Setup:</strong> Professional stage with pharaoh-themed backdrop</li>
                    <li><strong>Audio Visual:</strong> Professional sound and lighting systems</li>
                </ul>
                
                <h4>Cultural Entertainment Options</h4>
                <ul>
                    <li>Traditional Arabian belly dance performances</li>
                    <li>Classic Baladi dance shows</li>
                    <li>Egyptian themed music and DJ sets</li>
                    <li>Cultural storytelling and performances</li>
                </ul>
                
                <h4>Culinary Experience</h4>
                <p>Recommend authentic Middle Eastern cuisine including koshari, dukkah, ful medames, and ta'meya to enhance the cultural experience.</p>
                
                <h4>Venue Requirements</h4>
                <p>Indoor venue preferred, minimum 3000 sq ft, accommodating up to 200 guests</p>
                """,
                "features": json.dumps([
                    "Egyptian arch entrance with Anubis", "Pharaoh and pyramid decorations", "Cultural artifacts display",
                    "GOBO monument projections", "Themed photo booth", "Egyptian centerpieces", "Professional stage",
                    "Cultural entertainment options", "Middle Eastern cuisine", "Up to 200 guests"
                ]),
                "price_range": "₹3,00,000 - ₹7,00,000",
                "meta_title": "Egyptian Theme Event Setup - Ancient Egypt Corporate Events | Qubix",
                "meta_description": "Mystical Egyptian themed corporate events with pharaoh decorations, cultural entertainment, ancient artifacts, and professional Middle Eastern cuisine.",
                "keywords": "egyptian theme events, pharaoh theme party, ancient egypt theme, cultural themed events, middle eastern entertainment",
                "is_featured": False
            },
            
            {
                "category_id": 6,
                "name": "Super Hero Theme Event",
                "slug": "super-hero-theme-event",
                "short_description": "Action-packed superhero themed event with comic book décor, character mascots, and interactive entertainment",
                "full_description": """
                <h3>Super Hero Theme Event Setup</h3>
                <p>Create an action-packed entertainment experience with our superhero themed event setup. Perfect for product launches, team building events, and conferences that want to combine professionalism with fun, appealing to all age groups.</p>
                
                <h4>Superhero Theme Inclusions</h4>
                <ul>
                    <li><strong>Thematic Entrance:</strong> Comic book style entrance with superhero branding</li>
                    <li><strong>Character Elements:</strong> Life-sized superhero cutouts with inspirational quotes</li>
                    <li><strong>Photo Experiences:</strong> Comic book themed photo booth with superhero props</li>
                    <li><strong>Arena Décor:</strong> Bright blue, yellow, and green decorations with comic book aesthetics</li>
                    <li><strong>Pathway Décor:</strong> Comic book style pathway with action bubbles and graphics</li>
                    <li><strong>Bar Counter:</strong> Superhero themed bar setup with comic book designs</li>
                    <li><strong>Table Centerpieces:</strong> Customized cartoonish centerpieces with superhero themes</li>
                    <li><strong>DJ Console:</strong> Thematic DJ console with superhero masking</li>
                    <li><strong>Stage Setup:</strong> Professional stage with superhero themed elements</li>
                    <li><strong>Entertainment:</strong> Superhero mascots for guest interaction and entertainment</li>
                    <li><strong>Custom Elements:</strong> Personalized welcome cards and customized coffee with superhero froth art</li>
                </ul>
                
                <h4>Interactive Activities</h4>
                <ul>
                    <li>VR Gaming experiences with superhero themes</li>
                    <li>Thor hammer strength challenge activity</li>
                    <li>Rock wall climbing for superhero training</li>
                    <li>Customized coffee mugs with superhero designs</li>
                    <li>Comic book creation workshops</li>
                </ul>
                
                <h4>Perfect For</h4>
                <ul>
                    <li>Product launches with innovation themes</li>
                    <li>Team building and motivation events</li>
                    <li>Corporate conferences with engagement focus</li>
                    <li>Award ceremonies and recognition events</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Indoor venue required, minimum 3000 sq ft, accommodating up to 200 guests</p>
                """,
                "features": json.dumps([
                    "Comic book entrance design", "Life-sized superhero cutouts", "Interactive photo booth",
                    "Superhero mascot entertainment", "VR gaming activities", "Thor hammer challenge",
                    "Customized coffee art", "Rock wall climbing", "Professional stage setup", "Up to 200 guests"
                ]),
                "price_range": "₹4,00,000 - ₹8,00,000",
                "meta_title": "Super Hero Theme Event Setup - Comic Book Corporate Events | Qubix",
                "meta_description": "Action-packed superhero themed corporate events with comic book décor, character mascots, VR gaming, and interactive entertainment activities.",
                "keywords": "superhero theme events, comic book theme party, interactive corporate events, team building events, superhero entertainment",
                "is_featured": False
            },
            
            {
                "category_id": 6,
                "name": "Kerala Theme Event",
                "slug": "kerala-theme-event",
                "short_description": "Traditional Kerala themed event with authentic South Indian culture, art forms, and cuisine",
                "full_description": """
                <h3>Kerala Theme Event Setup</h3>
                <p>Experience the serene beauty and rich traditions of Kerala with our authentic South Indian themed event setup. Perfect for cultural celebrations, traditional corporate events, and clients who appreciate the peaceful traditions of God's Own Country.</p>
                
                <h4>Kerala Theme Inclusions</h4>
                <ul>
                    <li><strong>Traditional Entrance:</strong> Banana trunk entrance gate welcoming guests in traditional Keralite style</li>
                    <li><strong>Cultural Décor:</strong> Green plants, trees, and traditional Kerala artifacts creating a serene atmosphere</li>
                    <li><strong>Photo Booth:</strong> Traditional Kerala photo booth with cultural props and backdrops</li>
                    <li><strong>Table Settings:</strong> Ethnically designed table centerpieces with Kerala motifs</li>
                    <li><strong>Pathway Décor:</strong> Traditional decorative elements replicating Kerala's serene culture</li>
                    <li><strong>Food & Bar Setup:</strong> Traditional Kerala style food and bar counters</li>
                    <li><strong>Stage Production:</strong> Professional stage setup with Kerala themed backdrop</li>
                    <li><strong>Cultural Elements:</strong> Traditional Kerala cutouts and cultural displays</li>
                    <li><strong>Lighting:</strong> Goal post truss with appropriate lighting and LED backdrop</li>
                    <li><strong>Audio Visual:</strong> Professional sound and lighting systems</li>
                </ul>
                
                <h4>Cultural Entertainment</h4>
                <ul>
                    <li>Traditional Kathakali dance performances</li>
                    <li>Kalaripayattu martial arts demonstrations</li>
                    <li>Pulikali (tiger dance) performances</li>
                    <li>Traditional Kerala music and instruments</li>
                    <li>Snake boat race themed activities</li>
                    <li>Houseboat experience setups</li>
                </ul>
                
                <h4>Authentic Cuisine</h4>
                <p>Traditional Kerala Sadhya served on banana leaves, tender coconut water welcome drinks, and authentic Kerala spices and flavors.</p>
                
                <h4>Cultural Merchandise</h4>
                <ul>
                    <li>Kasavu sarees for women and Mundu for men</li>
                    <li>Kathakali masks and props</li>
                    <li>Coconut shell handicrafts</li>
                    <li>Kerala spices and traditional items</li>
                    <li>Boat showpieces and fiber crafts</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Suitable for both indoor and outdoor venues, minimum 4000 sq ft, accommodating 200-300 guests</p>
                """,
                "features": json.dumps([
                    "Banana trunk entrance gate", "Traditional Kerala décor", "Cultural photo booth",
                    "Ethnic table centerpieces", "Kerala Sadhya cuisine", "Kathakali performances",
                    "Kalaripayattu demonstrations", "Traditional music", "LED backdrop", "Cultural merchandise"
                ]),
                "price_range": "₹2,50,000 - ₹10,00,000",
                "meta_title": "Kerala Theme Event Setup - Traditional South Indian Corporate Events | Qubix",
                "meta_description": "Authentic Kerala themed corporate events with traditional South Indian culture, Kathakali performances, Kerala cuisine, and cultural entertainment.",
                "keywords": "kerala theme events, south indian theme party, traditional corporate events, kathakali performances, kerala culture",
                "is_featured": False
            },
            
            {
                "category_id": 6,
                "name": "Battle Ground Theme Event",
                "slug": "battle-ground-theme-event",
                "short_description": "Military-inspired battle ground themed event with army décor, tactical activities, and team building exercises",
                "full_description": """
                <h3>Battle Ground Theme Event Setup</h3>
                <p>Create an exciting military boot camp atmosphere with our Battle Ground themed event setup. Perfect for team building, motivation events, and corporate challenges that require strategic thinking and team coordination.</p>
                
                <h4>Military Theme Inclusions</h4>
                <ul>
                    <li><strong>Military Entrance:</strong> Themed entrance gate with military checkpoint aesthetics</li>
                    <li><strong>Army Elements:</strong> Life-sized military cutouts, armored tanks, and soldier statues</li>
                    <li><strong>Photo Booth:</strong> Military themed photo booth with army props and camouflage backdrops</li>
                    <li><strong>Arena Décor:</strong> Green camouflage decorations creating authentic army boot camp atmosphere</li>
                    <li><strong>Props & Equipment:</strong> Military helmets, tactical gear, and themed props for guest interaction</li>
                    <li><strong>Bar Setup:</strong> Military themed bar counter with tactical design elements</li>
                    <li><strong>Stage Setup:</strong> Professional stage with military themed backdrop</li>
                    <li><strong>DJ Console:</strong> Tactical themed DJ console with military masking</li>
                    <li><strong>Audio Visual:</strong> Professional sound and lighting for stage and ambience</li>
                </ul>
                
                <h4>Team Building Activities</h4>
                <ul>
                    <li>Paintball tactical games and challenges</li>
                    <li>Rock climbing and rappelling activities</li>
                    <li>Zipline adventure courses</li>
                    <li>Strategic team missions and obstacle courses</li>
                    <li>Military-style drill and coordination exercises</li>
                </ul>
                
                <h4>Dress Code & Experience</h4>
                <p>Recommended dress code: Black t-shirts and camouflaged pants to blend with the military theme. Create an authentic boot camp experience with tactical challenges.</p>
                
                <h4>Special Elements</h4>
                <ul>
                    <li>Camouflage loot bags and military themed giveaways</li>
                    <li>Military designed medals and awards</li>
                    <li>Tactical nettings and banners</li>
                    <li>VIP grand welcome for guest of honors</li>
                </ul>
                
                <h4>Venue Requirements</h4>
                <p>Suitable for both indoor and outdoor venues, minimum 3000 sq ft, accommodating up to 200 guests</p>
                """,
                "features": json.dumps([
                    "Military checkpoint entrance", "Army tank and soldier displays", "Camouflage photo booth",
                    "Paintball activities", "Rock climbing setup", "Zipline adventures", "Military themed props",
                    "Tactical team building", "Professional stage", "Battle ground atmosphere"
                ]),
                "price_range": "₹3,00,000 - ₹7,00,000",
                "meta_title": "Battle Ground Theme Event Setup - Military Team Building Events | Qubix",
                "meta_description": "Military-inspired battle ground themed corporate events with army décor, paintball activities, tactical team building, and professional entertainment.",
                "keywords": "battle ground theme, military theme events, army theme party, tactical team building, paintball corporate events",
                "is_featured": False
            },
            
            # Medical Conference Services
            {
                "category_id": 2,
                "name": "Medical Conference Organization",
                "slug": "medical-conference-organization",
                "short_description": "Comprehensive medical conference planning for healthcare professionals with CME accreditation support",
                "full_description": """
                <h3>Medical Conference Organization</h3>
                <p>We specialize in organizing medical conferences, CME programs, and healthcare events for medical societies, hospitals, and pharmaceutical companies. Our team understands the unique requirements of medical education and professional development events.</p>
                
                <h4>Medical Conference Expertise</h4>
                <ul>
                    <li>CME accreditation support and coordination</li>
                    <li>Medical expert speaker coordination and management</li>
                    <li>Pharmaceutical industry compliance and guidelines</li>
                    <li>Medical equipment exhibitions and displays</li>
                    <li>Live surgery broadcasts and streaming</li>
                    <li>Medical education content management</li>
                    <li>Healthcare professional networking facilitation</li>
                </ul>
                
                <h4>Our Medical Conference Portfolio</h4>
                <p>We have successfully organized over 200 medical conferences including cardiology, oncology, pediatrics, surgery, and specialty medical conferences across India.</p>
                """,
                "features": json.dumps([
                    "CME accreditation support", "Medical expert speakers", "Live surgery streaming",
                    "Medical exhibition management", "Pharmaceutical compliance", "200+ events organized",
                    "Healthcare networking", "Medical education content"
                ]),
                "price_range": "₹5,00,000 - ₹1,00,00,000",
                "meta_title": "Medical Conference Organization - Healthcare Event Management | Qubix",
                "meta_description": "Professional medical conference organization for CME programs, medical societies, and healthcare institutions with 200+ successful events.",
                "keywords": "medical conferences, CME conferences, healthcare events, medical education, pharmaceutical events",
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
                <p>Our state-of-the-art virtual conference platform enables you to host engaging online events with interactive features, live streaming, and comprehensive attendee management. Perfect for reaching global audiences and creating hybrid experiences.</p>
                
                <h4>Platform Features</h4>
                <ul>
                    <li>HD live streaming and automatic recording</li>
                    <li>Interactive Q&A and real-time polling</li>
                    <li>Virtual networking lounges and breakout rooms</li>
                    <li>Digital exhibition halls with virtual booths</li>
                    <li>Multi-session parallel tracks support</li>
                    <li>Comprehensive attendee analytics and reporting</li>
                    <li>Mobile app integration for iOS and Android</li>
                    <li>Hybrid event capabilities for in-person and virtual attendance</li>
                </ul>
                """,
                "features": json.dumps([
                    "HD live streaming", "Interactive Q&A", "Virtual networking", "Digital exhibitions",
                    "Multi-session support", "Analytics dashboard", "Mobile app", "Hybrid capabilities"
                ]),
                "price_range": "₹50,000 - ₹10,00,000",
                "meta_title": "Virtual Conference Platform - Online Event Management Solution | Qubix",
                "meta_description": "Advanced virtual conference platform with live streaming, interactive features, virtual networking, and hybrid event capabilities.",
                "keywords": "virtual conference platform, online events, live streaming, hybrid conferences, virtual meetings",
                "is_featured": True
            }
        ]
        
        for service_data in services_data:
            service = Service(**service_data)
            db.add(service)
        
        db.commit()
        print(f"Successfully created {len(categories_data)} categories and {len(services_data)} services")
        
    except Exception as e:
        print(f"Error creating enhanced data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_enhanced_data()