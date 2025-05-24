# Section 1: Page routing for main website pages
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.events import EventCategory, Service
from app.services.seo_service import SEOService
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")
seo_service = SEOService()

# Section 2: About Us Page
@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About us page with company information"""
    context = {
        "request": request,
        "title": "About Qubix Events & Conferences - Leading MICE Company India",
        "meta_description": "Learn about Qubix Events & Conferences Pvt. Ltd. - Premier event management company with 200+ medical conferences, 400+ corporate events, and 1000+ virtual conferences.",
        "keywords": "about qubix events, event management company India, MICE services, conference planning expertise, event planning team",
        "canonical_url": f"{settings.BASE_URL}/about"
    }
    return templates.TemplateResponse("about.html", context)

# Section 3: Services Overview Page  
@router.get("/services", response_class=HTMLResponse)
async def services_page(request: Request, db: Session = Depends(get_db)):
    """Services overview page listing all service categories"""
    categories = db.query(EventCategory).filter(EventCategory.is_active == True).all()
    featured_services = db.query(Service).filter(Service.is_featured == True, Service.is_active == True).limit(6).all()
    
    context = {
        "request": request,
        "title": "Event Management Services - Conference Planning & MICE Solutions | Qubix",
        "meta_description": "Comprehensive event management services including conference planning, medical conferences, corporate events, virtual platforms, audio-visual production & brand launches.",
        "keywords": "event management services, conference planning services, MICE solutions, corporate event management, medical conference organization, virtual conference platform",
        "canonical_url": f"{settings.BASE_URL}/services",
        "categories": categories,
        "featured_services": featured_services
    }
    return templates.TemplateResponse("services/index.html", context)

# Section 4: Individual Service Pages
@router.get("/services/{service_slug}", response_class=HTMLResponse)
async def service_detail_page(service_slug: str, request: Request, db: Session = Depends(get_db)):
    """Individual service detail page"""
    service = db.query(Service).filter(Service.slug == service_slug, Service.is_active == True).first()
    if not service:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    # Increment view count
    service.view_count += 1
    db.commit()
    
    # Related services
    related_services = db.query(Service).filter(
        Service.category_id == service.category_id,
        Service.id != service.id,
        Service.is_active == True
    ).limit(3).all()
    
    seo_data = seo_service.get_service_seo(service.name, service.short_description)
    
    context = {
        "request": request,
        "title": seo_data["title"],
        "meta_description": seo_data["meta_description"],
        "keywords": seo_data["keywords"],
        "canonical_url": f"{settings.BASE_URL}/services/{service_slug}",
        "service": service,
        "related_services": related_services
    }
    return templates.TemplateResponse("services/detail.html", context)

# Section 5: Contact Page
@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact page with inquiry form"""
    context = {
        "request": request,
        "title": "Contact Qubix Events - Get Quote for Event Management Services",
        "meta_description": "Contact Qubix Events & Conferences for professional event management services. Get custom quotes for conferences, corporate events & MICE solutions. Call +91-98993-39005",
        "keywords": "contact qubix events, event management quote, conference planning inquiry, MICE services contact, event planning consultation",
        "canonical_url": f"{settings.BASE_URL}/contact",
        "addresses": settings.ADDRESSES,
        "phone_numbers": settings.PHONE_NUMBERS,
        "contact_email": settings.CONTACT_EMAIL
    }
    return templates.TemplateResponse("contact.html", context)

# Section 6: Virtual Conference Platform Page
@router.get("/virtual-conference-platform", response_class=HTMLResponse)
async def virtual_platform_page(request: Request):
    """Virtual conference platform dedicated page"""
    context = {
        "request": request,
        "title": "Virtual Conference Platform - Online Event Management Solutions | Qubix",
        "meta_description": "Advanced virtual conference platform by Qubix Events. Host engaging online conferences, webinars & virtual events with interactive features, live streaming & attendee management.",
        "keywords": "virtual conference platform, online event management, virtual events, webinar platform, online conference solution, virtual meeting platform",
        "canonical_url": f"{settings.BASE_URL}/virtual-conference-platform"
    }
    return templates.TemplateResponse("virtual-platform.html", context)

# Section 7: Sitemap XML
@router.get("/sitemap.xml", response_class=Response)
async def sitemap_xml(db: Session = Depends(get_db)):
    """Generate XML sitemap for SEO"""
    urls = seo_service.generate_sitemap_urls()
    
    # Add service URLs
    services = db.query(Service).filter(Service.is_active == True).all()
    for service in services:
        urls.append({
            "loc": f"{settings.BASE_URL}/services/{service.slug}",
            "priority": "0.8",
            "changefreq": "monthly"
        })
    
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        sitemap_content += f'  <url>\n'
        sitemap_content += f'    <loc>{url["loc"]}</loc>\n'
        sitemap_content += f'    <priority>{url["priority"]}</priority>\n'
        sitemap_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        sitemap_content += f'  </url>\n'
    
    sitemap_content += '</urlset>'
    
    return Response(content=sitemap_content, media_type="application/xml")

# Section 8: Robots.txt
@router.get("/robots.txt", response_class=Response)
async def robots_txt():
    """Generate robots.txt for SEO"""
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {settings.BASE_URL}/sitemap.xml
"""
    return Response(content=robots_content, media_type="text/plain")