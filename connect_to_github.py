#!/usr/bin/env python3
"""
AI CEO Platform GitHub Connection Script
Connect your entire AI CEO platform to GitHub account: starksaiceo45@gmail.com
"""

import os
import subprocess
import sys

def run_command(cmd, description=""):
    """Run a shell command and return the result"""
    print(f"\n🔧 {description}")
    print(f"Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout.strip()}")
            return True, result.stdout
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, str(e)

def main():
    print("🚀 AI CEO Platform - GitHub Connection Setup")
    print("📧 Connecting to GitHub account: starksaiceo45@gmail.com")
    print("📂 Project size: ~1.9GB with 20,000+ files")
    
    # Configure Git identity
    print("\n" + "="*50)
    print("STEP 1: Configure Git Identity")
    print("="*50)
    
    success, _ = run_command(
        'git config user.email "starksaiceo45@gmail.com"',
        "Setting Git email"
    )
    
    success, _ = run_command(
        'git config user.name "AI CEO Platform"',
        "Setting Git username"
    )
    
    # Initialize repository if needed
    print("\n" + "="*50)
    print("STEP 2: Initialize Repository")
    print("="*50)
    
    if not os.path.exists('.git'):
        success, _ = run_command(
            'git init',
            "Initializing Git repository"
        )
    else:
        print("✅ Git repository already exists")
    
    # Show current status
    print("\n" + "="*50)
    print("STEP 3: Repository Status")
    print("="*50)
    
    run_command('git status --porcelain | wc -l', "Counting untracked files")
    
    # Add all files (respecting .gitignore)
    print("\n" + "="*50)
    print("STEP 4: Stage All Files")
    print("="*50)
    
    success, _ = run_command(
        'git add .',
        "Adding all files to staging (this may take a moment for large projects)"
    )
    
    # Create initial commit
    print("\n" + "="*50)
    print("STEP 5: Create Initial Commit")
    print("="*50)
    
    success, _ = run_command(
        'git commit -m "Initial commit: AI CEO Platform - Complete autonomous business automation system with 20K+ files"',
        "Creating initial commit"
    )
    
    # Instructions for GitHub connection
    print("\n" + "="*60)
    print("STEP 6: Connect to GitHub - MANUAL STEPS REQUIRED")
    print("="*60)
    
    print("""
🎯 NEXT STEPS - Complete these manually:

1. CREATE GITHUB REPOSITORY:
   • Go to https://github.com
   • Sign in with: starksaiceo45@gmail.com
   • Click '+' → 'New repository'
   • Name: 'ai-ceo-platform' 
   • Description: 'Autonomous Business Automation Platform'
   • Keep it Public or Private (your choice)
   • DO NOT initialize with README (you have files already)
   • Click 'Create repository'

2. ADD REMOTE AND PUSH:
   Copy and run these commands in Replit Console:

   git remote add origin https://github.com/starksaiceo45/ai-ceo-platform.git
   git branch -M main
   git push -u origin main

3. AUTHENTICATION:
   When prompted for credentials:
   • Username: starksaiceo45
   • Password: Create a Personal Access Token at:
     GitHub → Settings → Developer settings → Personal access tokens
     → Generate new token → Select 'repo' scope

📊 YOUR PLATFORM DATA TO BE UPLOADED:
   • 20,000+ Python files
   • Complete AI CEO SaaS platform
   • User authentication system
   • Business automation tools
   • Marketing automation
   • Voice system integration
   • Database schemas
   • All configurations and assets
   • Total size: ~1.9GB

🔒 PROTECTED FILES (won't be uploaded):
   • Database files (ai_ceo_saas.db, etc.)
   • Environment files (.env)
   • API keys and secrets
   • Session data
   • Cache files

✅ READY FOR GITHUB!
""")

if __name__ == "__main__":
    main()