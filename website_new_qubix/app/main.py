# Section 1: Imports and Initial Setup
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pathlib import Path

# Section 2: Import custom modules
from app.routers import pages, api
from app.database import engine, Base
from app.config import settings
from app.services.seo_service import SEOService

# Section 3: Create FastAPI application instance
app = FastAPI(
    title="Qubix Events & Conferences",
    description="Professional event planning and conference management services",
    version="2.0.0",
    # docs_url="/admin/docs" if settings.ENVIRONMENT != "production" else None,
    # redoc_url="/admin/redoc" if settings.ENVIRONMENT != "production" else None
)

# Section 4: CORS and Security Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Section 5: Static Files and Templates Setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Section 6: Database initialization
@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables on startup"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

# Section 7: Include routers for different sections
app.include_router(pages.router, tags=["pages"])
app.include_router(api.router, prefix="/api", tags=["api"])
# app.include_router(admin.router, prefix="/admin", tags=["admin"])

# Section 8: Root endpoint with SEO optimization
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Main homepage with full SEO optimization"""
    seo_service = SEOService()
    seo_data = seo_service.get_homepage_seo()
    
    context = {
        "request": request,
        "title": seo_data["title"],
        "meta_description": seo_data["meta_description"],
        "keywords": seo_data["keywords"],
        "canonical_url": f"{settings.BASE_URL}/",
        "og_image": f"{settings.BASE_URL}/static/images/qubix-og-image.jpg",
        "schema_data": seo_data["schema_data"]
    }
    return templates.TemplateResponse("index.html", context)

# Section 9: Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "Qubix Events & Conferences"}

# Section 10: 404 Error handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 page with SEO considerations"""
    context = {
        "request": request,
        "title": "Page Not Found - Qubix Events",
        "meta_description": "The page you're looking for doesn't exist. Explore our event management services.",
    }
    return templates.TemplateResponse("404.html", context, status_code=404)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )