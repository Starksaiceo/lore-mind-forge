# AI CEO Frontend - Lovable Setup

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=/                     # same-origin proxy or set full Replit URL
VITE_PUBLIC_SITE_URL=https://app.ai-ceo.com
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_xxx # optional if using Stripe Elements
```

## Connecting to Replit Backend

1. **Development**: Set `VITE_API_BASE_URL` to your Replit URL (e.g., `https://your-repl-name.username.repl.co`)
2. **Production**: Use same-origin proxy or full backend URL
3. **CORS**: Backend must allow your Lovable preview URL and production domain

## Routes & API Coverage

### Public Routes
- `/` - Landing page
- `/pricing` - Pricing plans → `/billing/checkout`
- `/login` - Login → `/auth/login`
- `/register` - Register → `/auth/register`

### Protected Routes (User)
- `/dashboard` - System status, stats, activity → `/integrations/status`, `/activity`
- `/chat` - Text chat → `/chat/text`
- `/voice` - Voice chat → `/chat/voice`
- `/products` - Product creation → `/products/stripe/create`, `/products/shopify/create`
- `/billing` - Subscription management → `/billing/checkout`, `/billing/portal`
- `/activity` - Activity feed → `/activity`
- `/operations` - System operations → `/ops/e2e_proof`, `/integrations/selftest`

### Admin Routes
- `/admin` - Admin dashboard → `/integrations/status`, `/activity`
- `/admin/users` - User management
- `/admin/system` - System health → `/healthz`, `/config/missing`

## API Endpoints Used

- `GET /healthz` - Health check
- `GET /integrations/status` - Service status
- `POST /integrations/selftest` - Self-test
- `GET /auth/me` - Session info
- `POST /auth/login` - Login
- `POST /auth/register` - Register
- `POST /auth/logout` - Logout
- `POST /chat/text` - Text chat
- `POST /chat/voice` - Voice chat
- `POST /products/stripe/create` - Create Stripe product
- `POST /products/shopify/create` - Create Shopify product
- `POST /billing/checkout` - Start checkout
- `POST /billing/portal` - Billing portal
- `GET /activity` - Activity feed
- `POST /ops/e2e_proof` - E2E proof
- `GET /policy/status` - Policy status
- `GET /config/missing` - Missing config

## Features

- ✅ Dark/neon theme with glassmorphism
- ✅ Responsive design
- ✅ Role-based access control
- ✅ Error handling with toasts
- ✅ Service status badges
- ✅ Voice recording and playback
- ✅ Real-time activity feeds
- ✅ Graceful degradation
- ✅ Admin panel