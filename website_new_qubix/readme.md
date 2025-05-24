# Qubix Events & Conferences Website

<div align="center">

![Qubix Events Logo](https://via.placeholder.com/400x150/2c5aa0/ffffff?text=QUBIX+EVENTS+%26+CONFERENCES)

**Professional Event Management & Conference Planning Services**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org/)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com/)

</div>

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🎭 Services Portfolio](#-services-portfolio)
- [🛠️ Technology Stack](#-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Installation Guide](#-installation-guide)
- [🐳 Docker Deployment](#-docker-deployment)
- [🔧 Configuration](#-configuration)
- [📊 Database Schema](#-database-schema)
- [🎨 Customization](#-customization)
- [🔒 Security](#-security)
- [📈 SEO Features](#-seo-features)
- [🧪 Testing](#-testing)
- [🚀 Production Deployment](#-production-deployment)
- [🔍 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📞 Support](#-support)

---

## 🌟 Overview

Qubix Events & Conferences Website is a modern, SEO-optimized platform for a leading event management company in India. The website showcases comprehensive event planning services including medical conferences, corporate events, virtual conferences, and themed events with detailed service packages integrated from MICEkart industry standards.

### 🎯 Key Highlights

- **1600+ Successful Events** managed across India
- **200+ Medical Conferences** with CME accreditation
- **400+ Corporate Events** for leading companies
- **1000+ Virtual Conferences** with advanced technology
- **50+ Exhibitions** and trade shows organized
- **Pan-India Presence** in Delhi, Kolkata, and Bangalore

---

## ✨ Features

### 🖥️ Frontend Features
- **Responsive Design** - Mobile-first approach with TailwindCSS
- **Modern UI/UX** - Clean, professional interface with smooth animations
- **Interactive Elements** - Hover effects, counters, galleries, and forms
- **Accessibility** - WCAG 2.1 compliant with proper ARIA labels
- **Progressive Enhancement** - Works without JavaScript, enhanced with it

### ⚙️ Backend Features
- **FastAPI Framework** - High-performance async Python web framework
- **RESTful APIs** - Clean API endpoints for all functionality
- **Database ORM** - SQLAlchemy with support for multiple databases
- **Email Integration** - SMTP notifications for inquiries and quotes
- **Background Tasks** - Async processing for better performance

### 🔍 SEO & Performance
- **Meta Tags Optimization** - Dynamic meta tags for all pages
- **Structured Data** - Schema.org markup for rich snippets
- **XML Sitemaps** - Automatic sitemap generation
- **OpenGraph & Twitter Cards** - Social media optimization
- **Performance Optimized** - Lazy loading, caching, and compression

### 🛡️ Security Features
- **Input Validation** - Pydantic models for all data validation
- **SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection
- **XSS Protection** - Template auto-escaping and CSP headers
- **Rate Limiting** - API rate limiting to prevent abuse
- **Security Headers** - Comprehensive security headers via Nginx

---

## 🎭 Services Portfolio

### 🏢 Conference Management
| Service | Capacity | Price Range | Features |
|---------|----------|-------------|----------|
| **Basic Conference Setup** | Up to 50 guests | ₹27,000 - ₹37,000 | Stage, PA system, projector, backdrop |
| **Curve LED Backdrop** | Up to 300 guests | ₹9,10,000 - ₹16,30,000 | 36ft curved LED, advanced lighting |
| **Hanging LED Setup** | Up to 300 guests | ₹10,20,000 - ₹21,00,000 | Multiple LED screens, premium AV |

### 🎨 Themed Events
| Theme | Capacity | Price Range | Highlights |
|-------|----------|-------------|------------|
| **Bollywood Theme** | Up to 300 guests | ₹3,00,000 - ₹8,00,000 | Red carpet, celebrity cutouts, entertainment |
| **James Bond 007** | Up to 200 guests | ₹8,00,000 - ₹18,00,000 | Limousine, casino tables, luxury setup |
| **Casino Theme** | Up to 200 guests | ₹3,00,000 - ₹7,00,000 | Gaming tables, LED dance floor |
| **Egyptian Theme** | Up to 200 guests | ₹3,00,000 - ₹7,00,000 | Pharaoh décor, cultural entertainment |
| **Kerala Theme** | Up to 300 guests | ₹2,50,000 - ₹10,00,000 | Traditional setup, cultural performances |
| **Super Hero Theme** | Up to 200 guests | ₹4,00,000 - ₹8,00,000 | Comic book décor, interactive activities |
| **Battle Ground Theme** | Up to 200 guests | ₹3,00,000 - ₹7,00,000 | Military setup, tactical activities |

### 🏥 Specialized Services
- **Medical Conference Organization** - CME accreditation, expert speakers
- **Virtual Conference Platform** - HD streaming, interactive features
- **Corporate Event Management** - Product launches, annual meetings
- **Audio Visual Production** - Complete AV solutions

---

## 🛠️ Technology Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[SQLAlchemy](https://sqlalchemy.org/)** - Database ORM
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation
- **[Jinja2](https://jinja.palletsprojects.com/)** - Template engine
- **[Uvicorn](https://uvicorn.org/)** - ASGI server

### Frontend
- **[TailwindCSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Font Awesome](https://fontawesome.com/)** - Icon library
- **Vanilla JavaScript** - No heavy frameworks, pure performance

### Database
- **SQLite** (Development) - Zero-configuration database
- **PostgreSQL** (Production) - Robust relational database
- **MySQL** (Alternative) - Popular database option

### DevOps & Deployment
- **[Docker](https://docker.com/)** - Containerization
- **[Nginx](https://nginx.org/)** - Reverse proxy and static files
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container orchestration

---

## 📁 Project Structure

```
website_new_qubix/
├── 📂 app/                          # Main application package
│   ├── 📄 __init__.py              # Package initialization
│   ├── 📄 main.py                  # FastAPI application entry point
│   ├── 📄 config.py                # Configuration settings
│   ├── 📄 database.py              # Database connection setup
│   ├── 📂 models/                  # SQLAlchemy models
│   │   ├── 📄 __init__.py
│   │   └── 📄 events.py            # Event-related models
│   ├── 📂 routers/                 # API route handlers
│   │   ├── 📄 __init__.py
│   │   ├── 📄 api.py               # API endpoints
│   │   └── 📄 pages.py             # Page routes
│   └── 📂 services/                # Business logic services
│       ├── 📄 __init__.py
│       ├── 📄 email_service.py     # Email notifications
│       └── 📄 seo_service.py       # SEO utilities
├── 📂 templates/                   # Jinja2 templates
│   ├── 📄 base.html                # Base template
│   ├── 📄 index.html               # Homepage
│   ├── 📄 about.html               # About page
│   ├── 📄 contact.html             # Contact page
│   ├── 📄 404.html                 # Error page
│   ├── 📄 virtual-platform.html    # Virtual platform page
│   └── 📂 services/                # Service templates
│       ├── 📄 index.html           # Services overview
│       └── 📄 detail.html          # Service detail pages
├── 📂 static/                      # Static assets
│   ├── 📂 css/                     # Stylesheets
│   │   └── 📄 custom.css           # Custom CSS
│   ├── 📂 js/                      # JavaScript files
│   │   └── 📄 main.js              # Main JavaScript
│   └── 📂 images/                  # Image assets
│       ├── 📂 services/            # Service images
│       ├── 📂 events/              # Event photos
│       └── 📂 testimonials/        # Client photos
├── 📂 scripts/                     # Utility scripts
│   ├── 📄 init_database.py         # Database initialization
│   ├── 📄 setup_static.py          # Static file setup
│   └── 📄 debug_qubix.py           # Debug and troubleshooting
├── 📂 deployment/                  # Deployment configurations
│   ├── 📄 Dockerfile               # Container definition
│   ├── 📄 docker-compose.yml       # Multi-container setup
│   └── 📄 nginx.conf               # Nginx configuration
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.template                # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
└── 📄 README.md                    # This comprehensive guide
```

---

## 🚀 Quick Start

Get your Qubix Events website running in 5 minutes:

### 📋 Prerequisites
- **Python 3.8+** installed
- **Git** for version control
- **pip** package manager

### ⚡ One-Command Setup

```bash
# Clone and setup (Windows)
git clone <repository-url> && cd website_new_qubix && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python debug_qubix.py --fix && python init_database.py && uvicorn app.main:app --reload

# Clone and setup (Linux/Mac)
git clone <repository-url> && cd website_new_qubix && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python debug_qubix.py --fix && python init_database.py && uvicorn app.main:app --reload
```

### 🌐 Access Your Website
- **Homepage**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin (if enabled)
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## ⚙️ Installation Guide

### 🔧 Detailed Step-by-Step Setup

#### 1. **Environment Setup**
```bash
# Clone the repository
git clone <repository-url>
cd website_new_qubix

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### 2. **Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Verify installation
python debug_qubix.py
```

#### 3. **Configure Environment**
```bash
# Copy environment template
cp .env.template .env

# Edit configuration (required)
# Update .env file with your settings:
# - SECRET_KEY: Generate a secure secret key
# - EMAIL_USERNAME: Your SMTP email
# - EMAIL_PASSWORD: Your SMTP password
# - BASE_URL: Your domain (for production)
```

#### 4. **Database Setup**
```bash
# Run diagnostic check
python debug_qubix.py

# Initialize database with sample data
python init_database.py

# Verify database setup
python debug_qubix.py
```

#### 5. **Static Files Setup**
```bash
# Setup static file structure
python setup_static.py

# Verify all files are in place
python debug_qubix.py
```

#### 6. **Launch Application**
```bash
# Development server with auto-reload
uvicorn app.main:app --reload

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 🔍 Verification Steps

After setup, verify everything works:

1. **Visit Homepage**: http://localhost:8000
2. **Check Services Page**: http://localhost:8000/services  
3. **Test Contact Form**: http://localhost:8000/contact
4. **Verify API**: http://localhost:8000/docs
5. **Health Check**: http://localhost:8000/health

---

## 🐳 Docker Deployment

### 🚀 Quick Docker Setup

#### Single Container
```bash
# Build image
docker build -t qubix-events .

# Run container
docker run -d -p 8000:8000 --name qubix-website qubix-events
```

#### Multi-Container with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 🔧 Docker Services

The Docker setup includes:

- **Web Application** - FastAPI server
- **Nginx** - Reverse proxy and static files
- **Redis** - Caching and sessions
- **PostgreSQL** - Production database (optional)

#### Environment Variables for Docker
```bash
# Create production .env
cp .env.template .env

# Update for production:
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:password@db:5432/qubix_events
```

#### Docker Health Checks
```bash
# Check container health
docker-compose ps

# Check application health
curl http://localhost/health
```

---

## 🔧 Configuration

### 📝 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Application secret key | `your-secret-key` | ✅ |
| `ENVIRONMENT` | Environment (dev/prod) | `development` | ✅ |
| `DEBUG` | Debug mode | `true` | ✅ |
| `DATABASE_URL` | Database connection | `sqlite:///./qubix_events.db` | ✅ |
| `BASE_URL` | Website base URL | `http://localhost:8000` | ✅ |
| `SMTP_SERVER` | Email server | `smtp.gmail.com` | ❌ |
| `EMAIL_USERNAME` | SMTP username | - | ❌ |
| `EMAIL_PASSWORD` | SMTP password | - | ❌ |
| `CONTACT_EMAIL` | Contact email | `info@qubixsolutions.in` | ✅ |

### 🗄️ Database Configuration

#### SQLite (Development)
```env
DATABASE_URL=sqlite:///./qubix_events.db
```

#### PostgreSQL (Production)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/qubix_events
```

#### MySQL (Alternative)
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/qubix_events
```

### 📧 Email Configuration

#### Gmail SMTP
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

#### Other SMTP Providers
```env
# Outlook
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587

# Yahoo
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

---

## 📊 Database Schema

### 🗂️ Tables Overview

#### EventCategory
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(100) | Category name |
| `slug` | String(100) | URL-friendly identifier |
| `description` | Text | Category description |
| `icon` | String(100) | Font Awesome icon class |
| `meta_title` | String(60) | SEO title |
| `meta_description` | String(160) | SEO description |
| `keywords` | String(255) | SEO keywords |
| `is_active` | Boolean | Active status |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

#### Service
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `category_id` | Integer | Foreign key to EventCategory |
| `name` | String(200) | Service name |
| `slug` | String(200) | URL-friendly identifier |
| `short_description` | String(300) | Brief description |
| `full_description` | Text | Detailed HTML description |
| `features` | Text | JSON array of features |
| `price_range` | String(100) | Price range display |
| `meta_title` | String(60) | SEO title |
| `meta_description` | String(160) | SEO description |
| `keywords` | String(255) | SEO keywords |
| `image_url` | String(500) | Service image URL |
| `gallery_images` | Text | JSON array of gallery images |
| `is_active` | Boolean | Active status |
| `is_featured` | Boolean | Featured on homepage |
| `view_count` | Integer | Page view counter |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

#### Inquiry
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `service_id` | Integer | Optional service reference |
| `name` | String(100) | Customer name |
| `email` | String(100) | Customer email |
| `phone` | String(20) | Customer phone |
| `company` | String(200) | Customer company |
| `event_type` | String(100) | Type of event |
| `event_date` | DateTime | Expected event date |
| `location` | String(200) | Event location |
| `expected_attendees` | Integer | Number of attendees |
| `budget_range` | String(50) | Budget range |
| `message` | Text | Customer message |
| `requirements` | Text | Specific requirements |
| `status` | String(20) | Processing status |
| `is_priority` | Boolean | Priority inquiry |
| `created_at` | DateTime | Submission timestamp |

### 🔄 Database Migrations

```bash
# Initialize database with sample data
python init_database.py

# For production, consider using Alembic for migrations
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## 🎨 Customization

### 🖌️ Styling Customization

#### CSS Variables
Edit `static/css/custom.css`:
```css
:root {
  --qubix-blue: #2c5aa0;
  --qubix-light: #3b82f6;
  --qubix-dark: #1e3a8a;
  --qubix-gradient: linear-gradient(135deg, var(--qubix-dark), var(--qubix-blue));
}
```

#### TailwindCSS Configuration
The project uses TailwindCSS via CDN. For custom builds:
```bash
# Install TailwindCSS
npm install -D tailwindcss

# Create config file
npx tailwindcss init

# Build custom CSS
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

### 🔧 Adding New Services

#### 1. Database Entry
```python
from app.database import SessionLocal
from app.models.events import Service
import json

db = SessionLocal()
service = Service(
    category_id=1,
    name="New Service Name",
    slug="new-service-name",
    short_description="Brief description",
    full_description="<p>Detailed HTML description</p>",
    features=json.dumps(["Feature 1", "Feature 2"]),
    price_range="₹50,000 - ₹2,00,000",
    is_active=True,
    is_featured=True
)
db.add(service)
db.commit()
```

#### 2. Template Customization
Services automatically appear on the website once added to the database.

### 📄 Adding New Pages

#### 1. Create Template
```html
<!-- templates/new-page.html -->
{% extends "base.html" %}
{% block title %}New Page Title{% endblock %}
{% block content %}
<section class="py-16">
    <div class="container mx-auto px-4">
        <h1 class="text-4xl font-bold mb-8">New Page</h1>
        <p>Page content here...</p>
    </div>
</section>
{% endblock %}
```

#### 2. Add Route
```python
# app/routers/pages.py
@router.get("/new-page", response_class=HTMLResponse)
async def new_page(request: Request):
    context = {
        "request": request,
        "title": "New Page - Qubix Events",
        "meta_description": "New page description",
        "canonical_url": f"{settings.BASE_URL}/new-page"
    }
    return templates.TemplateResponse("new-page.html", context)
```

#### 3. Update Navigation
```html
<!-- templates/base.html -->
<a href="/new-page" class="text-gray-700 hover:text-qubix-blue">New Page</a>
```

---

## 🔒 Security

### 🛡️ Security Features Implemented

#### Input Validation
- **Pydantic Models** - All API inputs validated
- **SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection
- **XSS Prevention** - Template auto-escaping enabled

#### Security Headers
```nginx
# nginx.conf
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=63072000" always;
```

#### Rate Limiting
```nginx
# nginx.conf
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=static:10m rate=30r/s;
```

### 🔐 Security Best Practices

#### Environment Security
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set proper file permissions
chmod 600 .env
chmod 700 app/
```

#### Database Security
```python
# Use environment variables for sensitive data
DATABASE_URL=postgresql://user:password@localhost/db
# Never commit credentials to version control
```

#### HTTPS Configuration
```nginx
# nginx.conf - SSL configuration
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
```

---

## 📈 SEO Features

### 🔍 SEO Implementation

#### Meta Tags
- **Dynamic meta titles** and descriptions for all pages
- **Keywords optimization** for each service and page
- **Canonical URLs** to prevent duplicate content

#### Structured Data
```html
<!-- Schema.org markup -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Qubix Events & Conferences",
  "description": "Leading event management company",
  "url": "https://qubixsolutions.in"
}
</script>
```

#### XML Sitemap
- **Automatic generation** at `/sitemap.xml`
- **Dynamic updates** when services are added
- **Search engine submission** ready

#### Performance Optimization
- **Lazy loading** for images
- **Minified CSS/JS** in production
- **Gzip compression** via Nginx
- **CDN ready** for static assets

### 📊 SEO Monitoring

#### Google Analytics Setup
```html
<!-- Add to base.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

#### Search Console Verification
```html
<!-- Add to base.html head -->
<meta name="google-site-verification" content="your-verification-code" />
```

---

## 🧪 Testing

### 🔬 Testing Framework

#### Unit Tests
```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

#### Integration Tests
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "Qubix Events" in response.text

def test_contact_form():
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Test message"
    }
    response = client.post("/api/contact", json=data)
    assert response.status_code == 200
```

#### Load Testing
```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host=http://localhost:8000
```

### 🔍 Quality Assurance

#### Code Quality
```bash
# Install quality tools
pip install black flake8 mypy

# Format code
black app/

# Check style
flake8 app/

# Type checking
mypy app/
```

#### Security Testing
```bash
# Install security scanner
pip install bandit

# Run security scan
bandit -r app/
```

---

## 🚀 Production Deployment

### 🌐 Deployment Options

#### VPS/Cloud Server Deployment

**1. Server Preparation**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv nginx postgresql redis-server

# Create application user
sudo useradd -m -s /bin/bash qubix
sudo su - qubix
```

**2. Application Setup**
```bash
# Clone repository
git clone <repository-url> qubix-website
cd qubix-website

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env with production settings
```

**3. Database Setup**
```bash
# PostgreSQL setup
sudo -u postgres createdb qubix_events
sudo -u postgres createuser qubix_user
sudo -u postgres psql -c "ALTER USER qubix_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE qubix_events TO qubix_user;"

# Initialize database
python init_database.py
```

**4. Systemd Service**
```ini
# /etc/systemd/system/qubix-website.service
[Unit]
Description=Qubix Events Website
After=network.target

[Service]
Type=exec
User=qubix
Group=qubix
WorkingDirectory=/home/qubix/qubix-website
Environment=PATH=/home/qubix/qubix-website/venv/bin
ExecStart=/home/qubix/qubix-website/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**5. Nginx Configuration**
```nginx
# /etc/nginx/sites-available/qubix-website
server {
    listen 80;
    server_name qubixsolutions.in www.qubixsolutions.in;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name qubixsolutions.in www.qubixsolutions.in;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/qubix/qubix-website/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Docker Production Deployment

**1. Production Docker Compose**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    build: .
    environment:
      - DATABASE_URL=postgresql://qubix_user:passwor