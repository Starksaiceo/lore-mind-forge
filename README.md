# AI CEO Platform

An autonomous business automation platform that enables users to create, manage, and scale online businesses through AI-powered automation. The platform combines multi-agent AI systems, revenue sharing, and enterprise-grade integrations to create a complete business-in-a-box solution.

## Features

🤖 **Multi-Agent AI System** - Autonomous business operations and decision-making  
💰 **Revenue Sharing** - Users keep 90-95% of earnings via Stripe Connect  
🔐 **Enterprise OAuth** - One-click platform integrations  
📊 **Google Ads Automation** - Intelligent campaign management  
🎥 **YouTube Integration** - Automated content creation and posting  
🛡️ **Privacy Controls** - Invite-only registration system  
👑 **Admin Panel** - Complete user and system management  

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Required API keys (see Environment Variables section)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/starksaiceo45/ai-ceo-platform.git
cd ai-ceo-platform
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (see below)

4. Initialize the database:
```bash
python -c "from app_saas import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all()"
```

### Running Locally

```bash
python app_saas.py
```

The application will be available at `http://localhost:5000`

### Production Deployment

```bash
gunicorn app_saas:app --timeout 120 --workers 3 --bind 0.0.0.0:$PORT
```

## Environment Variables

Copy `.env.example` to `.env` and configure the following:

### Core Services
- `OPENROUTER_API_KEY` - AI model access for content generation
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask session encryption key

### Payment Processing
- `STRIPE_SECRET_KEY` - Stripe payment processing
- `STRIPE_PUBLISHABLE_KEY` - Stripe frontend integration
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook verification

### Google Services
- `GOOGLE_ADS_DEVELOPER_TOKEN` - Google Ads API access
- `GOOGLE_ADS_CLIENT_ID` - OAuth client for Google Ads
- `GOOGLE_ADS_CLIENT_SECRET` - OAuth secret for Google Ads
- `GOOGLE_ADS_REFRESH_TOKEN` - Persistent Google Ads access

### YouTube Integration
- `YOUTUBE_CLIENT_ID` - YouTube API OAuth client
- `YOUTUBE_CLIENT_SECRET` - YouTube API OAuth secret
- `YOUTUBE_REFRESH_TOKEN` - YouTube API persistent access

### Social Media APIs (Optional)
- `TWITTER_CLIENT_ID` - Twitter/X API integration
- `TWITTER_CLIENT_SECRET` - Twitter/X API secret
- `META_ACCESS_TOKEN` - Facebook/Instagram API access
- `META_AD_ACCOUNT_ID` - Meta advertising account

### E-commerce (Optional)
- `SHOPIFY_API_KEY` - Shopify store integration
- `SHOPIFY_ACCESS_TOKEN` - Shopify API access

## Project Structure

```
ai-ceo-platform/
├── app_saas.py              # Main Flask application
├── models.py                # Database models and schemas
├── requirements.txt         # Python dependencies
├── Procfile                # Deployment configuration
├── .env.example            # Environment variables template
├── templates/              # HTML templates
├── static/                 # CSS, JS, and static assets
├── database_export.sql     # Database schema and sample data
└── docs/                   # Documentation
```

## Database Setup

The platform uses PostgreSQL. If you have a database export:

```bash
psql $DATABASE_URL < database_export.sql
```

## Deployment Notes

### GitHub → Lovable.dev Import

1. Push your code to GitHub using the provided deployment guide
2. Import the repository into Lovable.dev
3. Configure environment variables in Lovable.dev settings
4. Deploy with automatic PostgreSQL database provisioning

### Manual Deployment

The platform is configured for deployment on any service supporting:
- Python 3.8+ with pip
- PostgreSQL database
- Environment variable configuration

## API Documentation

- Health check: `GET /health`
- User dashboard: `GET /dashboard` (requires auth)
- Admin panel: `GET /admin` (requires admin privileges)
- Autopilot status: `GET /api/autopilot/status`
- KPIs: `GET /api/kpis`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For deployment assistance or technical support, refer to the included documentation in the `docs/` directory.

## License

Proprietary - All rights reserved
