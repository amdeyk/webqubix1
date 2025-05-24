#!/usr/bin/env python3
"""
Debug and troubleshooting script for Qubix Events website
This script helps identify and fix common issues
"""

import sys
import os
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def check_required_packages():
    """Check if required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = {
        'fastapi': 'FastAPI framework',
        'uvicorn': 'ASGI server',
        'sqlalchemy': 'Database ORM',
        'jinja2': 'Template engine',
        'pydantic': 'Data validation'
    }
    
    missing_packages = []
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description} (MISSING)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def check_file_structure():
    """Check if all required files and directories exist"""
    print("\n📁 Checking file structure...")
    
    required_structure = {
        # Directories
        'app/': 'dir',
        'app/models/': 'dir', 
        'app/routers/': 'dir',
        'app/services/': 'dir',
        'templates/': 'dir',
        'templates/services/': 'dir',
        'static/': 'dir',
        'static/css/': 'dir',
        'static/js/': 'dir',
        'static/images/': 'dir',
        
        # Python files
        'app/__init__.py': 'file',
        'app/main.py': 'file',
        'app/config.py': 'file',
        'app/database.py': 'file',
        'app/models/__init__.py': 'file',
        'app/models/events.py': 'file',
        'app/routers/__init__.py': 'file',
        'app/routers/api.py': 'file',
        'app/routers/pages.py': 'file',
        'app/services/__init__.py': 'file',
        'app/services/email_service.py': 'file',
        'app/services/seo_service.py': 'file',
        
        # Templates
        'templates/base.html': 'file',
        'templates/index.html': 'file',
        'templates/about.html': 'file',
        'templates/contact.html': 'file',
        'templates/404.html': 'file',
        'templates/services/detail.html': 'file',
        'templates/virtual-platform.html': 'file',
        
        # Config files
        'requirements.txt': 'file',
        '.env.template': 'file'
    }
    
    missing_items = []
    
    for item_path, item_type in required_structure.items():
        path = Path(item_path)
        
        if item_type == 'dir':
            if path.is_dir():
                print(f"✅ {item_path} (directory)")
            else:
                print(f"❌ {item_path} (directory missing)")
                missing_items.append(item_path)
        else:  # file
            if path.is_file():
                print(f"✅ {item_path}")
            else:
                print(f"❌ {item_path} (file missing)")
                missing_items.append(item_path)
    
    if missing_items:
        print(f"\n⚠️ Missing items: {len(missing_items)}")
        for item in missing_items:
            print(f"   - {item}")
        return False
    else:
        print("✅ All required files and directories exist")
        return True

def check_database_connection():
    """Test database connection and setup"""
    print("\n🗄️ Checking database connection...")
    
    try:
        # Add the app directory to Python path
        sys.path.append(str(Path.cwd()))
        
        from app.database import engine, Base
        from app.models.events import EventCategory, Service
        from sqlalchemy import text
        
        # Test connection with proper syntax
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['event_categories', 'services', 'inquiries']
        missing_tables = [t for t in expected_tables if t not in tables]
        
        if missing_tables:
            print(f"⚠️ Missing tables: {missing_tables}")
            print("Run: python init_database.py")
            return False
        else:
            print("✅ All database tables exist")
            
            # Check table contents
            try:
                from app.database import SessionLocal
                db = SessionLocal()
                category_count = db.query(EventCategory).count()
                service_count = db.query(Service).count()
                db.close()
                print(f"📊 Database contains: {category_count} categories, {service_count} services")
                
                if category_count == 0:
                    print("⚠️ Database is empty. Run: python init_database.py")
                    return False
                    
            except Exception as e:
                print(f"⚠️ Could not check table contents: {e}")
                
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("Make sure to run: python init_database.py")
        return False

def check_environment_config():
    """Check environment configuration"""
    print("\n⚙️ Checking environment configuration...")
    
    # Check if .env file exists
    env_file = Path('.env')
    env_template = Path('.env.template')
    
    if not env_template.exists():
        print("❌ .env.template file missing")
        return False
    else:
        print("✅ .env.template exists")
    
    if not env_file.exists():
        print("⚠️ .env file doesn't exist")
        print("Copy .env.template to .env and configure your settings")
        
        # Auto-create .env from template
        try:
            import shutil
            shutil.copy('.env.template', '.env')
            print("✅ Auto-created .env from template")
        except Exception as e:
            print(f"❌ Could not create .env: {e}")
            return False
    else:
        print("✅ .env file exists")
    
    # Try to load config
    try:
        from app.config import settings
        print(f"✅ Configuration loaded successfully")
        print(f"   - Environment: {settings.ENVIRONMENT}")
        print(f"   - Debug: {settings.DEBUG}")
        print(f"   - Database URL: {settings.DATABASE_URL[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_template_rendering():
    """Test if templates can be rendered"""
    print("\n🎨 Testing template rendering...")
    
    try:
        from jinja2 import Environment, FileSystemLoader
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader('templates'))
        
        # Test loading base template
        base_template = env.get_template('base.html')
        print("✅ Base template loads successfully")
        
        # Test loading index template
        index_template = env.get_template('index.html')
        print("✅ Index template loads successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Template error: {e}")
        return False

def run_diagnostics():
    """Run all diagnostic checks"""
    print("🔧 QUBIX EVENTS - DIAGNOSTIC SCRIPT")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages), 
        ("File Structure", check_file_structure),
        ("Environment Config", check_environment_config),
        ("Database Connection", check_database_connection),
        ("Template Rendering", test_template_rendering)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} failed with error: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your setup looks good.")
        print("\nTo start the application:")
        print("uvicorn app.main:app --reload")
    else:
        print(f"\n⚠️ {total - passed} issues found. Please fix them before running the application.")
        
        # Provide specific instructions
        print("\n🔧 Next steps:")
        if not Path('requirements.txt').exists():
            print("1. Create requirements.txt file")
        if not Path('.env.template').exists():
            print("2. Create .env.template file")
        if not Path('.env').exists():
            print("3. Copy .env.template to .env")
        print("4. Run: python init_database.py")
        print("5. Run: uvicorn app.main:app --reload")
    
    return passed == total

def quick_fix():
    """Attempt to fix common issues automatically"""
    print("\n🔧 QUICK FIX - Attempting to resolve common issues...")
    
    try:
        # Create missing directories
        directories = [
            "static", "static/css", "static/js", "static/images",
            "static/images/services", "static/images/events", "static/images/testimonials",
            "templates", "templates/services"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        
        # Create placeholder files if they don't exist
        files_to_create = {
            "static/css/custom.css": "/* Custom CSS for Qubix Events */\n/* This file contains custom styles */",
            "static/js/main.js": "// Main JavaScript for Qubix Events\nconsole.log('Qubix Events JS loaded');",
            "static/images/.gitkeep": "# Keep this directory in git",
        }
        
        for file_path, content in files_to_create.items():
            if not Path(file_path).exists():
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"✓ Created file: {file_path}")
            else:
                print(f"⚠️ File already exists: {file_path}")
        
        print("✅ Static file structure setup complete!")
        
        # Create __init__.py files
        init_files = [
            'app/__init__.py',
            'app/models/__init__.py', 
            'app/routers/__init__.py',
            'app/services/__init__.py'
        ]
        
        for init_file in init_files:
            if not Path(init_file).exists():
                Path(init_file).touch()
                print(f"✅ Created {init_file}")
        
        # Copy .env.template to .env if it doesn't exist
        if Path('.env.template').exists() and not Path('.env').exists():
            import shutil
            shutil.copy('.env.template', '.env')
            print("✅ Copied .env.template to .env")
            print("⚠️ Please edit .env file with your configuration")
        
        print("✅ Quick fix completed!")
        
    except Exception as e:
        print(f"❌ Quick fix failed: {e}")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        quick_fix()
        print("\nRunning diagnostics after quick fix...")
    
    success = run_diagnostics()
    
    if not success:
        print("\n🔧 To attempt automatic fixes, run:")
        print("python debug_qubix.py --fix")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())