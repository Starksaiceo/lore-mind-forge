"""
Google Ads Refresh Token Generator for AI CEO Platform
Run this script to generate the refresh token needed for Google Ads API access
"""

import os
import requests
import urllib.parse
import secrets

def generate_google_ads_refresh_token():
    """Generate refresh token for Google Ads API using OAuth2 flow"""
    
    client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Missing GOOGLE_ADS_CLIENT_ID or GOOGLE_ADS_CLIENT_SECRET")
        print("Add these to your Replit Secrets first")
        return
    
    # Step 1: Generate authorization URL
    state = secrets.token_urlsafe(32)
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob"  # For installed apps
    
    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "https://www.googleapis.com/auth/adwords",
        "response_type": "code",
        "state": state,
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(auth_params)
    
    print("🚀 Google Ads OAuth2 Setup")
    print("=" * 50)
    print("1. Open this URL in your browser:")
    print(f"   {auth_url}")
    print("\n2. Sign in to your Google Ads account")
    print("3. Accept the permissions")
    print("4. Copy the authorization code from the page")
    print("\n" + "=" * 50)
    
    # Step 2: Get authorization code from user
    auth_code = input("Enter the authorization code: ").strip()
    
    if not auth_code:
        print("❌ No authorization code provided")
        return
    
    # Step 3: Exchange code for refresh token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        if response.status_code == 200:
            token_response = response.json()
            refresh_token = token_response.get("refresh_token")
            
            if refresh_token:
                print("✅ SUCCESS! Your Google Ads refresh token:")
                print("=" * 50)
                print(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}")
                print("=" * 50)
                print("\n📋 Next steps:")
                print("1. Add this to your Replit Secrets")
                print("2. Restart your AI CEO platform")
                print("3. Google Ads campaigns will work automatically!")
                return refresh_token
            else:
                print("❌ No refresh token in response")
                print(f"Response: {token_response}")
        else:
            print(f"❌ Token exchange failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Token exchange error: {e}")
    
    return None

if __name__ == "__main__":
    print("🚀 Google Ads Refresh Token Generator")
    print("=" * 50)
    token = generate_google_ads_refresh_token()
    
    if token:
        print(f"\n🎉 Token generated successfully!")
        print("Add this to Replit Secrets and your AI CEO will start creating Google Ads!")
    else:
        print("\n❌ Failed to generate token. Check the error messages above.")