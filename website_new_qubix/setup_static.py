#!/usr/bin/env python3
"""
Setup script to create static directories and basic files
Run this before starting the application
"""

import os
from pathlib import Path

def create_static_structure():
    """Create the static file structure"""
    print("🗂️ Setting up static file structure...")
    
    # Define directories to create
    directories = [
        "static",
        "static/css",
        "static/js", 
        "static/images",
        "static/images/services",
        "static/images/events",
        "static/images/testimonials",
        "templates",
        "templates/services"
    ]
    
    # Create directories
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

def check_dependencies():
    """Check if all required files exist"""
    print("\n🔍 Checking project dependencies...")
    
    required_files = [
        "app/main.py",
        "app/config.py", 
        "app/database.py",
        "app/models/events.py",
        "requirements.txt",
        "templates/base.html",
        "templates/index.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Warning: {len(missing_files)} required files are missing!")
        return False
    else:
        print("\n✅ All required files are present!")
        return True

def main():
    """Main setup function"""
    print("🚀 Qubix Events - Static Setup Script")
    print("=" * 50)
    
    try:
        create_static_structure()
        check_dependencies()
        
        print("\n" + "=" * 50)
        print("✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python init_database.py")
        print("2. Run: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())