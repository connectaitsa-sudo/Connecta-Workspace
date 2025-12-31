#!/usr/bin/env python3
"""
Test script to verify backend setup is correct
Run this to check if everything is configured properly
"""

import sys
import os

def print_status(message, status):
    """Print colored status message"""
    colors = {
        'success': '\033[92m✓',
        'error': '\033[91m✗',
        'warning': '\033[93m⚠',
        'info': '\033[94mℹ'
    }
    end = '\033[0m'
    
    symbol = colors.get(status, colors['info'])
    print(f"{symbol} {message}{end}")

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print_status(f"Python version {version.major}.{version.minor}.{version.micro} is compatible", 'success')
        return True
    else:
        print_status(f"Python version {version.major}.{version.minor}.{version.micro} is too old. Need 3.11+", 'error')
        return False

def check_env_file():
    """Check if .env file exists and has API key"""
    if not os.path.exists('.env'):
        print_status(".env file not found", 'error')
        print("  → Run: cp .env.example .env")
        return False
    
    print_status(".env file exists", 'success')
    
    # Check if API key is set
    with open('.env', 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=sk-' in content:
            print_status("OpenAI API key appears to be set", 'success')
            return True
        elif 'OPENAI_API_KEY=' in content:
            print_status("OpenAI API key is empty or invalid", 'warning')
            print("  → Add your API key from https://platform.openai.com/api-keys")
            return False
        else:
            print_status("OPENAI_API_KEY not found in .env", 'error')
            return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'openai',
        'sqlalchemy',
        'pydantic',
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"Package '{package}' is installed", 'success')
        except ImportError:
            print_status(f"Package '{package}' is NOT installed", 'error')
            all_installed = False
    
    if not all_installed:
        print("\n  → Run: pip install -r requirements.txt")
    
    return all_installed

def check_directories():
    """Check if required directories exist"""
    required_dirs = ['uploads', 'exports']
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print_status(f"Directory '{dir_name}/' exists", 'success')
        else:
            print_status(f"Directory '{dir_name}/' does NOT exist", 'warning')
            os.makedirs(dir_name, exist_ok=True)
            print(f"  → Created '{dir_name}/' directory")
            all_exist = False
    
    return True  # We create them if missing

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("🔍 AI Meeting Minutes System - Backend Setup Check")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        results.append(check_func())
    
    print("\n" + "="*60)
    if all(results):
        print_status("All checks passed! Backend is ready to run.", 'success')
        print("\n🚀 Start the backend with: python run.py")
    else:
        print_status("Some checks failed. Please fix the issues above.", 'error')
        print("\n📖 See LOCALHOST_DEPLOYMENT.md for detailed instructions")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
