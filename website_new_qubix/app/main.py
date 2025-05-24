# Section 1: Imports and Initial Setup
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from pathlib import Path
import logging

# Section 2: Import custom modules
from app.routers import pages, api
from app.database import engine, Base, get_db
from app.config import settings
from app.services.seo_service import SEOService
from app.models.events import EventCategory, Service

# Section 3: Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Section 4: Create FastAPI application instance
app = FastAPI(
    title="Qubix Events & Conferences",
    description="Professional event planning and conference management services",
    version="2.0.0",
)

# Section 5: CORS and Security Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Section 6: Static Files and Templates Setup
print("Setting up static files and templates...")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
print("✓ Static files and templates configured")

# Section 7: Database initialization
@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables on startup"""
    print("🚀 Starting up application...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database initialized successfully")
        
        # Test database connection
        db = next(get_db())
        category_count = db.query(EventCategory).count()
        service_count = db.query(Service).count()
        print(f"📊 Database status: {category_count} categories, {service_count} services")
        db.close()
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise

# Section 8: Include routers for different sections
print("Setting up routers...")
app.include_router(pages.router, tags=["pages"])
app.include_router(api.router, prefix="/api", tags=["api"])
print("✓ Routers configured")

# Section 9: Helper function to convert SQLAlchemy objects to dict
def model_to_dict(model):
    """Convert SQLAlchemy model to dictionary for JSON serialization"""
    if model is None:
        return None
    
    result = {}
    for column in model.__table__.columns:
        result[column.name] = getattr(model, column.name)
    return result

def models_to_dict_list(models):
    """Convert list of SQLAlchemy models to list of dictionaries"""
    if not models:
        return []
    return [model_to_dict(model) for model in models]

# Section 10: Root endpoint with SEO optimization and debug output
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    """Main homepage with full SEO optimization"""
    print("\n🏠 Homepage request received")
    
    try:
        # Initialize SEO service
        print("📄 Initializing SEO service...")
        seo_service = SEOService()
        seo_data = seo_service.get_homepage_seo()
        print("✓ SEO data generated")
        
        # Get featured services for homepage
        print("🔍 Querying featured services...")
        featured_services_query = db.query(Service).filter(
            Service.is_featured == True, 
            Service.is_active == True
        ).limit(6)
        featured_services = featured_services_query.all()
        print(f"✓ Found {len(featured_services)} featured services")
        
        # Get categories for any dropdowns/navigation
        print("🗂️ Querying categories...")
        categories_query = db.query(EventCategory).filter(
            EventCategory.is_active == True
        )
        categories = categories_query.all()
        print(f"✓ Found {len(categories)} active categories")
        
        # Convert SQLAlchemy objects to dictionaries for JSON serialization
        print("🔄 Converting models to dictionaries...")
        featured_services_dict = models_to_dict_list(featured_services)
        categories_dict = models_to_dict_list(categories)
        print("✓ Models converted successfully")
        
        # Build context
        print("🏗️ Building template context...")
        context = {
            "request": request,
            "title": seo_data["title"],
            "meta_description": seo_data["meta_description"],
            "keywords": seo_data["keywords"],
            "canonical_url": f"{settings.BASE_URL}/",
            "og_image": f"{settings.BASE_URL}/static/images/qubix-og-image.jpg",
            "schema_data": seo_data["schema_data"],
            "featured_services": featured_services,  # Keep original for template
            "categories": categories_dict,  # Use dict version for JSON
            "featured_services_json": featured_services_dict  # For any JSON needs
        }
        print("✓ Context built successfully")
        
        print("🎨 Rendering template...")
        return templates.TemplateResponse("index.html", context)
        
    except Exception as e:
        print(f"❌ Homepage error: {e}")
        logger.error(f"Homepage error: {e}", exc_info=True)
        
        # Fallback context in case of error
        fallback_context = {
            "request": request,
            "title": "Qubix Events & Conferences - Premier Event Management",
            "meta_description": "Professional event management services",
            "keywords": "event management, conferences",
            "canonical_url": f"{settings.BASE_URL}/",
            "og_image": f"{settings.BASE_URL}/static/images/qubix-og-image.jpg",
            "schema_data": "{}",
            "featured_services": [],
            "categories": [],
            "featured_services_json": []
        }
        return templates.TemplateResponse("index.html", fallback_context)

# Section 11: Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    print("🏥 Health check requested")
    
    try:
        # Test database connection
        db = next(get_db())
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy", 
            "service": "Qubix Events & Conferences",
            "database": "connected"
        }
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return {
            "status": "unhealthy", 
            "service": "Qubix Events & Conferences",
            "database": "disconnected",
            "error": str(e)
        }

# Section 12: 404 Error handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 page with SEO considerations"""
    print(f"🔍 404 error for path: {request.url.path}")
    
    context = {
        "request": request,
        "title": "Page Not Found - Qubix Events",
        "meta_description": "The page you're looking for doesn't exist. Explore our event management services.",
        "keywords": "qubix events, event management",
        "canonical_url": f"{settings.BASE_URL}/404"
    }
    return templates.TemplateResponse("404.html", context, status_code=404)

# Section 13: Global exception handler
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle internal server errors"""
    print(f"💥 Internal server error: {exc}")
    logger.error(f"Internal server error: {exc}", exc_info=True)
    
    context = {
        "request": request,
        "title": "Server Error - Qubix Events",
        "meta_description": "An internal server error occurred. Please try again later.",
    }
    return templates.TemplateResponse("404.html", context, status_code=500)

if __name__ == "__main__":
    print("🚀 Starting Qubix Events application...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )