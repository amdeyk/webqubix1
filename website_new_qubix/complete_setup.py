#!/usr/bin/env python3
"""
Complete setup script for Qubix Events website
This script sets up the entire project from scratch
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step, message):
    """Print formatted step message"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print(f"{'='*60}")

def run_command(command, description=""):
    """Run a command and handle errors"""
    try:
        print(f"🔧 {description}: {command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"✓ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def create_directory_structure():
    """Create the complete directory structure"""
    directories = [
        "app/models",
        "app/routers", 
        "app/services",
        "templates/services",
        "static/css",
        "static/js",
        "static/images",
        "static/images/services",
        "static/images/events",
        "static/images/testimonials"
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")

def create_init_files():
    """Create __init__.py files"""
    init_files = [
        "app/__init__.py",
        "app/models/__init__.py",
        "app/routers/__init__.py", 
        "app/services/__init__.py"
    ]
    
    print("📄 Creating __init__.py files...")
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write("# Package initialization\n")
        print(f"✓ Created: {init_file}")

def create_placeholder_images():
    """Create placeholder images and files"""
    placeholder_files = {
        "static/images/.gitkeep": "# Keep this directory",
        "static/images/qubix-logo.png": "# Placeholder for Qubix logo",
        "static/images/qubix-logo-white.png": "# Placeholder for white logo",
        "static/images/hero-conference.png": "# Placeholder for hero image",
        "static/images/qubix-og-image.jpg": "# Placeholder for OG image",
        "static/images/favicon.ico": "# Placeholder for favicon"
    }
    
    print("🖼️ Creating placeholder files...")
    for file_path, content in placeholder_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✓ Created: {file_path}")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return False
    
    # Install requirements
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def setup_environment():
    """Setup environment file"""
    print("⚙️ Setting up environment...")
    
    # Copy .env.template to .env if it doesn't exist
    if Path(".env.template").exists() and not Path(".env").exists():
        shutil.copy(".env.template", ".env")
        print("✓ Created .env from template")
        print("⚠️ Please edit .env file with your configuration")
        return True
    elif Path(".env").exists():
        print("✓ .env file already exists")
        return True
    else:
        print("❌ .env.template not found!")
        return False

def initialize_database():
    """Initialize the database with seed data"""
    print("🗄️ Initializing database...")
    
    # Run database initialization
    return run_command("python init_database.py", "Creating database and seed data")

def test_application():
    """Test if the application starts correctly"""
    print("🧪 Testing application startup...")
    
    # Try to import the main app
    try:
        sys.path.append(str(Path.cwd()))
        from app.main import app
        print("✓ Application imports successfully")
        return True
    except Exception as e:
        print(f"❌ Application import failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 QUBIX EVENTS - COMPLETE SETUP")
    print("This script will set up your entire Qubix Events website")
    print(f"Working directory: {Path.cwd()}")
    
    # Confirm setup
    response = input("\nDo you want to proceed with the setup? (y/N): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        return
    
    success_steps = 0
    total_steps = 6
    
    # Step 1: Create directory structure
    print_step(1, "Creating Directory Structure")
    create_directory_structure()
    create_init_files()
    create_placeholder_images()
    success_steps += 1
    
    # Step 2: Setup environment
    print_step(2, "Setting Up Environment")
    if setup_environment():
        success_steps += 1
    
    # Step 3: Install dependencies
    print_step(3, "Installing Dependencies")
    if install_dependencies():
        success_steps += 1
    
    # Step 4: Initialize database
    print_step(4, "Initializing Database")
    if initialize_database():
        success_steps += 1
    
    # Step 5: Test application
    print_step(5, "Testing Application")
    if test_application():
        success_steps += 1
    
    # Step 6: Final instructions
    print_step(6, "Setup Complete")
    
    print(f"\n🎉 SETUP SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successfully completed: {success_steps}/{total_steps} steps")
    
    if success_steps == total_steps:
        print("\n🎊 Congratulations! Setup completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Edit your .env file with proper configuration")
        print("2. Add your actual logo and images to static/images/")
        print("3. Start the development server:")
        print("   uvicorn app.main:app --reload")
        print("4. Visit: http://localhost:8000")
        print("\n📞 Support:")
        print("- Check debug_qubix.py for troubleshooting")
        print("- Review README.md for detailed documentation")
        
    else:
        print(f"\n⚠️ Setup completed with {total_steps - success_steps} issues")
        print("Please resolve the issues above and try again.")
        print("Run 'python debug_qubix.py' for detailed diagnostics")
    
    success_steps += 1
    
    return success_steps == total_steps

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)