#!/usr/bin/env python3
"""
Quick Start Script for AI-CRM HCP Module
Checks prerequisites and guides setup
"""
import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_command(command, name, install_hint):
    """Check if a command exists."""
    try:
        result = subprocess.run(
            [command, "--version"], 
            capture_output=True, 
            text=True,
            shell=True
        )
        print(f"✓ {name} is installed")
        return True
    except FileNotFoundError:
        print(f"✗ {name} is NOT installed")
        print(f"  Install from: {install_hint}")
        return False

def check_prerequisites():
    """Check all prerequisites."""
    print_header("Checking Prerequisites")
    
    all_ok = True
    
    # Check Python
    if sys.version_info >= (3, 10):
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} is installed")
    else:
        print(f"✗ Python 3.10+ required (found {sys.version_info.major}.{sys.version_info.minor})")
        all_ok = False
    
    # Check Node.js
    all_ok &= check_command("node", "Node.js", "https://nodejs.org/")
    
    # Check PostgreSQL
    all_ok &= check_command("psql", "PostgreSQL", "https://www.postgresql.org/download/")
    
    return all_ok

def check_env_file():
    """Check if .env file exists."""
    print_header("Checking Configuration")
    
    env_path = Path("backend/.env")
    env_example_path = Path("backend/.env.example")
    
    if env_path.exists():
        print("✓ backend/.env file exists")
        
        # Check if GROQ_API_KEY is set
        with open(env_path, 'r') as f:
            content = f.read()
            if "your_groq_api_key_here" in content or "GROQ_API_KEY=" not in content:
                print("⚠ WARNING: GROQ_API_KEY not configured in .env")
                print("  Get your key from: https://console.groq.com/")
                return False
            else:
                print("✓ GROQ_API_KEY appears to be configured")
                return True
    else:
        print("✗ backend/.env file not found")
        if env_example_path.exists():
            print("  Creating .env from .env.example...")
            import shutil
            shutil.copy(env_example_path, env_path)
            print("✓ Created backend/.env")
            print("  ⚠ Please edit backend/.env and add your GROQ_API_KEY")
        return False

def install_backend_dependencies():
    """Install Python dependencies."""
    print_header("Installing Backend Dependencies")
    
    try:
        print("Installing Python packages...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"],
            check=True
        )
        print("✓ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install backend dependencies")
        return False

def install_frontend_dependencies():
    """Install Node.js dependencies."""
    print_header("Installing Frontend Dependencies")
    
    try:
        print("Installing Node packages...")
        subprocess.run(
            ["npm", "install"],
            cwd="frontend",
            check=True,
            shell=True
        )
        print("✓ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install frontend dependencies")
        return False

def setup_database():
    """Guide user through database setup."""
    print_header("Database Setup")
    
    print("To set up the database, run these commands in PostgreSQL:")
    print("\n  psql -U postgres")
    print("  CREATE DATABASE crm_hcp_db;")
    print("  CREATE USER crm_user WITH PASSWORD 'crm_password';")
    print("  GRANT ALL PRIVILEGES ON DATABASE crm_hcp_db TO crm_user;")
    print("  \\q\n")
    
    response = input("Have you set up the database? (y/n): ").lower()
    return response == 'y'

def seed_database():
    """Seed the database with sample data."""
    print_header("Seeding Database")
    
    response = input("Do you want to seed the database with sample data? (y/n): ").lower()
    
    if response == 'y':
        try:
            print("Seeding database...")
            subprocess.run(
                [sys.executable, "backend/seed_data.py"],
                check=True
            )
            print("✓ Database seeded successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to seed database")
            return False
    return True

def print_next_steps():
    """Print next steps to run the application."""
    print_header("Setup Complete!")
    
    print("\n🚀 To start the application:\n")
    print("Terminal 1 (Backend):")
    print("  cd backend")
    print("  python main.py")
    print("\nTerminal 2 (Frontend):")
    print("  cd frontend")
    print("  npm start")
    print("\nThen open: http://localhost:3000")
    print("\n" + "="*60)
    print("\n📚 Additional Resources:")
    print("  - Setup Guide: SETUP_GUIDE.md")
    print("  - Tool Demo Guide: TOOL_DEMO_GUIDE.md")
    print("  - API Testing: API_TESTING.md")
    print("  - Submission Checklist: SUBMISSION_CHECKLIST.md")
    print("\n✨ Good luck with your demo! ✨\n")

def main():
    """Main setup flow."""
    print("\n🏥 AI-CRM HCP Module - Quick Start Setup\n")
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n⚠ Please install missing prerequisites and run again.")
        sys.exit(1)
    
    # Step 2: Check .env file
    env_configured = check_env_file()
    if not env_configured:
        print("\n⚠ Please configure backend/.env with your GROQ_API_KEY")
        print("  Get your key from: https://console.groq.com/")
        sys.exit(1)
    
    # Step 3: Install backend dependencies
    response = input("\nInstall backend dependencies? (y/n): ").lower()
    if response == 'y':
        if not install_backend_dependencies():
            sys.exit(1)
    
    # Step 4: Install frontend dependencies
    response = input("\nInstall frontend dependencies? (y/n): ").lower()
    if response == 'y':
        if not install_frontend_dependencies():
            sys.exit(1)
    
    # Step 5: Setup database
    if not setup_database():
        print("\n⚠ Please set up the database before continuing.")
        sys.exit(1)
    
    # Step 6: Seed database
    seed_database()
    
    # Step 7: Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
        sys.exit(1)

