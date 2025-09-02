# AI CEO - Autonomous Business Automation Platform

## Overview

AI CEO is a comprehensive SaaS platform that enables users to create, manage, and scale online businesses through AI-powered automation. The platform combines autonomous business generation, multi-channel marketing, payment processing, and intelligent decision-making to create a complete business-in-a-box solution. Users can generate digital products, launch stores, run advertising campaigns, and manage their revenue streams through a unified dashboard with minimal manual intervention.

## User Preferences

Preferred communication style: Simple, everyday language.

## GitHub Integration

The AI CEO platform is now connected to GitHub account: starksaiceo45@gmail.com
- Repository initialized with project files
- Workflow configured to serve Flask application on port 5000
- Platform accessible at http://0.0.0.0:5000

## System Architecture

### Frontend Architecture
- **Flask-based Web Application**: Primary web interface with user authentication and session management
- **Streamlit Dashboard**: Interactive analytics and control panel for real-time monitoring
- **Multi-tenancy Support**: User-based isolation with subscription tiers and usage limits
- **Voice System Integration**: AI personality management with voice interaction capabilities

### Backend Architecture
- **Agent-Based System**: Modular AI agents for specific tasks (SEO, content creation, marketing, product generation)
- **Autonomous Loop Controller**: Continuous background processes for business operations
- **Event-Driven Architecture**: Activity logging and performance tracking across all business operations
- **Memory System**: AI learning and pattern recognition for optimizing business strategies

### Data Storage Solutions
- **SQLite Database**: Primary storage with Flask-SQLAlchemy ORM for user data, sessions, and business metrics
- **File Storage Manager**: Local and cloud storage integration for media files and generated content
- **Replit Database**: Key-value storage for caching and temporary data
- **JSON-based Configuration**: Flexible settings management and API configurations

### Authentication and Authorization
- **Flask-Login Integration**: Session-based user authentication with role-based access
- **Subscription Management**: Tiered access control with Stripe integration for billing
- **API Key Management**: Secure storage and validation of third-party service credentials
- **Rate Limiting**: Request throttling to prevent API abuse and manage costs

## External Dependencies

### E-commerce Platforms
- **Shopify API**: Product catalog management and order processing integration
- **Gumroad**: Digital product marketplace for automated sales
- **Stripe Payments**: Primary payment processor for subscription billing and transaction handling

### Marketing and Advertising
- **Meta Ads API**: Facebook and Instagram advertising campaign management
- **Google Ads API**: Search and display advertising automation
- **TikTok Ads**: Social media advertising integration
- **Twitter/X API**: Social media content automation and engagement

### AI and Analytics
- **OpenRouter API**: LLM access for content generation and business intelligence
- **Google Trends API**: Market research and trend analysis
- **PyTrends Library**: Enhanced trending data collection and analysis

### Communication Services
- **Email Automation**: Marketing sequence generation and delivery
- **SMS Integration**: Customer communication and notifications
- **Voice System**: AI personality voices and interactive communication

### Development Tools
- **GitHub Integration**: Version control and deployment automation
- **Replit Infrastructure**: Cloud hosting and database services
- **SQLAlchemy ORM**: Database abstraction and migration management