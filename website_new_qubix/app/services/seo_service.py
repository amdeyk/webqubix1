# Section 1: SEO service for generating meta tags and structured data
import json
from typing import Dict, List
from app.config import settings

class SEOService:
    """Service for managing SEO-related functionality"""
    
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.site_name = settings.SITE_NAME
    
    # Section 2: Homepage SEO data
    def get_homepage_seo(self) -> Dict:
        """Generate SEO data for homepage"""
        schema_data = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": self.site_name,
            "description": "Leading event management and conference planning company providing comprehensive MICE services across India",
            "url": self.base_url,
            "logo": f"{self.base_url}/static/images/qubix-logo.png",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": settings.PHONE_NUMBERS[0],
                "contactType": "customer service",
                "email": settings.CONTACT_EMAIL
            },
            "address": [
                {
                    "@type": "PostalAddress",
                    "streetAddress": addr["address"],
                    "addressLocality": addr["city"],
                    "addressCountry": "IN"
                } for addr in settings.ADDRESSES
            ],
            "sameAs": [
                settings.FACEBOOK_URL,
                settings.INSTAGRAM_URL,
                settings.YOUTUBE_URL,
                settings.LINKEDIN_URL
            ],
            "services": [
                "Conference Planning & Management",
                "Medical Conference Organization", 
                "Corporate Event Management",
                "Virtual Conference Platform",
                "Audio Visual Production",
                "Brand Launch Events"
            ]
        }
        
        return {
            "title": "Qubix Events & Conferences - Premier Event Management Company in India",
            "meta_description": "Professional event management and conference planning services across India. Specializing in medical conferences, corporate events, virtual platforms & MICE services. 200+ successful events.",
            "keywords": "event management company India, conference planning, medical conference, corporate events, MICE services, virtual conference platform, event planning Delhi Kolkata Bangalore",
            "schema_data": json.dumps(schema_data)
        }
    
    # Section 3: Service page SEO
    def get_service_seo(self, service_name: str, service_description: str) -> Dict:
        """Generate SEO data for service pages"""
        return {
            "title": f"{service_name} - Professional Event Management | Qubix Events",
            "meta_description": f"{service_description[:150]}... Expert {service_name.lower()} services by Qubix Events & Conferences.",
            "keywords": f"{service_name.lower()}, event management, conference planning, {service_name.lower()} India, professional event services"
        }
    
    # Section 4: Generate sitemap data
    def generate_sitemap_urls(self) -> List[Dict]:
        """Generate URLs for sitemap.xml"""
        urls = [
            {"loc": f"{self.base_url}/", "priority": "1.0", "changefreq": "weekly"},
            {"loc": f"{self.base_url}/about", "priority": "0.8", "changefreq": "monthly"},
            {"loc": f"{self.base_url}/services", "priority": "0.9", "changefreq": "weekly"},
            {"loc": f"{self.base_url}/contact", "priority": "0.7", "changefreq": "monthly"},
            {"loc": f"{self.base_url}/virtual-conference-platform", "priority": "0.9", "changefreq": "weekly"},
        ]
        return urls