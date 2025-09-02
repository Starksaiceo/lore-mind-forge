# DEPLOY_TO_GITHUB.md - DevOps Deployment Guide

## 🚀 AI CEO Platform - GitHub Deployment & Lovable Import

This guide provides step-by-step instructions for deploying your AI CEO Platform to GitHub and importing it into Lovable.dev.

## Repository Information
- **GitHub Username**: starksaiceo45
- **Repository Name**: ai-ceo-platform
- **Repository URL**: https://github.com/starksaiceo45/ai-ceo-platform.git
- **Main Branch**: main

## Prerequisites Checklist

✅ **Files Prepared**:
- `.gitignore` - Updated with all security exclusions
- `README.md` - Complete project documentation
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment configuration
- `database_export.sql` - Database backup

## Step 1: Git Safety & Repository Setup

### Open Replit Shell
Click the "Shell" tab in Replit and execute these commands:

```bash
# Clear any git locks
sudo rm -f .git/index.lock .git/config.lock .git/refs/heads/main.lock

# Check git status
git status

# Configure git user
git config user.email "starksaiceo45@gmail.com"
git config user.name "starksaiceo45"

# Ensure we're on main branch
git branch -M main
```

### Untrack Sensitive Files (if tracked)
```bash
# Remove sensitive files from tracking
git rm -r --cached .venv venv __pycache__ *.pyc *.db node_modules .next dist build .DS_Store .idea .pytest_cache coverage || true
git rm --cached .env *.env .replit_secrets secrets.json || true
```

## Step 2: Stage and Commit Changes

```bash
# Add all files (excluding ignored ones)
git add .

# Commit with proper message
git commit -m "chore: prepare repo for GitHub + Lovable import (ignore secrets, add docs)"
```

## Step 3: Connect to GitHub Remote

```bash
# Remove existing origin (if any)
git remote remove origin 2>/dev/null || true

# Add your GitHub repository as origin
git remote add origin https://github.com/starksaiceo45/ai-ceo-platform.git

# Verify remote is set correctly
git remote -v
```

## Step 4: Push to GitHub

```bash
# Push to GitHub (force if needed to overwrite)
git push -u origin main --force

# If push fails, try pull with rebase first:
# git pull --rebase origin main
# git push -u origin main
```

## Step 5: Validation & Verification

### Check File Sizes
```bash
# List files larger than 100MB (should be empty)
find . -type f -size +100M -not -path "./.git/*" -not -path "./venv/*" -not -path "./.venv/*"

# Verify sensitive files are ignored
git status --ignored
```

### Verify Repository
1. Visit: https://github.com/starksaiceo45/ai-ceo-platform
2. Confirm all files are present
3. Check that `.env` files are NOT visible
4. Verify README.md displays properly

## Step 6: Import into Lovable.dev

### Import Process
1. Go to [Lovable.dev](https://lovable.dev)
2. Click "Import from GitHub"
3. Select `starksaiceo45/ai-ceo-platform`
4. Lovable will detect it as a Python Flask project

### Environment Variables Setup
Configure these in Lovable.dev settings (copy from `.env.example`):

```bash
# Core Services
OPENROUTER_API_KEY=your_key_here
DATABASE_URL=postgresql://...
SECRET_KEY=your_secret_key

# Payment Processing
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Google Services
GOOGLE_ADS_DEVELOPER_TOKEN=...
GOOGLE_ADS_CLIENT_ID=...
GOOGLE_ADS_CLIENT_SECRET=...
GOOGLE_ADS_REFRESH_TOKEN=...

# YouTube Integration
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...

# Social Media APIs
TWITTER_CLIENT_ID=...
TWITTER_CLIENT_SECRET=...
META_ACCESS_TOKEN=...
META_AD_ACCOUNT_ID=...

# E-commerce
SHOPIFY_API_KEY=...
SHOPIFY_ACCESS_TOKEN=...
```

### Database Setup
1. Lovable.dev will provision PostgreSQL automatically
2. Import your data: Upload `database_export.sql` through Lovable.dev dashboard
3. Or run: `psql $DATABASE_URL < database_export.sql`

## Future Sync Commands

### Pull Latest Changes
```bash
git pull origin main
```

### Push New Changes
```bash
git add .
git commit -m "feat: your change description"
git push origin main
```

## Final Deployment Checklist

✅ **Repository Setup**:
- [ ] Repository created at https://github.com/starksaiceo45/ai-ceo-platform
- [ ] All code pushed to `main` branch
- [ ] Sensitive files properly ignored
- [ ] README.md displays correctly

✅ **Lovable.dev Import**:
- [ ] Repository imported successfully
- [ ] Environment variables configured
- [ ] Database connected and populated
- [ ] Application starts without errors

✅ **Post-Deployment**:
- [ ] Health check endpoint responding: `/health`
- [ ] Admin panel accessible: `/admin`
- [ ] API endpoints functional: `/api/autopilot/status`

## Start Command for Lovable.dev
```bash
python app_saas.py
```

## Support

Your AI CEO Platform is now ready for production deployment with:
- Multi-agent AI automation
- Revenue sharing (90-95% to users)
- Enterprise OAuth integrations
- Google Ads & YouTube automation
- Complete admin panel
- Privacy controls

---
**✅ Deployment Complete - Ready for Lovable.dev! 🎉**