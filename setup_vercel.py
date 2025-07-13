#!/usr/bin/env python3
"""
Setup script for Vercel deployment with Supabase
"""

import os
import sys

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your Vercel environment variables.")
        return False
    
    print("✅ All required environment variables are set")
    return True

def check_files():
    """Check if required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'vercel.json',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files exist")
    return True

def check_supabase_setup():
    """Check if Supabase setup files exist"""
    setup_files = [
        'supabase_setup.sql',
        'supabase_storage_setup.sql'
    ]
    
    print("📋 Supabase setup files:")
    for file in setup_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
    
    return True

def main():
    print("🚀 Vercel + Supabase Deployment Setup Check")
    print("=" * 50)
    
    # Check environment variables
    print("\n1. Environment Variables:")
    env_ok = check_environment()
    
    # Check required files
    print("\n2. Required Files:")
    files_ok = check_files()
    
    # Check Supabase setup
    print("\n3. Supabase Setup:")
    check_supabase_setup()
    
    print("\n" + "=" * 50)
    
    if env_ok and files_ok:
        print("✅ Your project is ready for Vercel deployment!")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Connect your repository to Vercel")
        print("3. Set environment variables in Vercel dashboard")
        print("4. Deploy!")
    else:
        print("❌ Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main() 