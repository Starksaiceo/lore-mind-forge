import os
from dotenv import load_dotenv

# Define the secrets that need to be set
SECRETS = {
    "STRIPE_SECRET_KEY": "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",
    "STRIPE_PUBLISHABLE_KEY": "pk_live_51RrfM5G0HoeSSRcXeBHOLDJUazsHVUyCZoNSDz9LK5ozLioIFdS5WdmlUtrugEAwFS1hOKbqSXs3apD8l7oQu2Qt00QUYJrhqv",
    "GUMROAD_API_KEY": "tMYPg6y1nZPo1weCwd7Ohj4_Myv54oRFMRxCBDxFlhE",
    "GUMROAD_ACCESS_TOKEN": "tMYPg6y1nZPo1weCwd7Ohj4_Myv54oRFMRxCBDxFlhE",
    "GUMROAD_APP_SECRET": "ZM8ho_sCw3PA6imjeyL6aMiXep9EHBjcJUPyWNxZ-xc"
}

def setup_environment():
    """Setup environment variables and load .env file"""
    try:
        # Create or update .env file
        with open(".env", "w", encoding="utf-8") as env_file:
            for key, value in SECRETS.items():
                env_file.write(f"{key}={value}\n")

        # Load the environment variables
        load_dotenv()

        # Verify all keys are loaded
        missing_keys = []
        for key in SECRETS.keys():
            if not os.getenv(key):
                missing_keys.append(key)

        if missing_keys:
            print(f"❌ Missing keys: {missing_keys}")
            return False

        print("✅ Environment setup complete!")
        print(f"✅ Keys loaded: {', '.join([f'{k}: {v[:6]}...' for k, v in SECRETS.items()])}")

        # Initialize database
        try:
            from database_upgrade import upgrade_database
            if upgrade_database():
                print("✅ Database initialized successfully!")
            else:
                print("⚠️ Database initialization had issues (may be normal for first run)")
        except Exception as e:
            print(f"⚠️ Database setup warning: {e}")

        print("🚀 Ready to start application!")
        return True

    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_environment()