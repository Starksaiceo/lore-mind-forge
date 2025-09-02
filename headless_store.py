"""
Built-in Headless Store System for AI CEO Platform
Allows users to start selling immediately without external platforms
"""

import os
import json
import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from models import db, Tenant, TenantConnection
from sqlalchemy import select
import stripe
import uuid

logger = logging.getLogger(__name__)

store_bp = Blueprint('store', __name__)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class HeadlessStore:
    """Manages the built-in store for immediate selling"""
    
    def __init__(self):
        self.products_db = 'headless_products.json'
        self.orders_db = 'headless_orders.json'
    
    def get_user_store(self, user_id):
        """Get user's store configuration and products"""
        try:
            # Check if user has a tenant
            tenant = db.session.execute(select(Tenant).where(Tenant.owner_user_id == user_id)).scalar_one_or_none()
            if not tenant:
                return None
            
            # Load products from JSON (in production would be in database)
            products = []
            if os.path.exists(self.products_db):
                with open(self.products_db, 'r') as f:
                    all_products = json.load(f)
                    products = [p for p in all_products if p.get('user_id') == user_id]
            
            store_config = json.loads(tenant.config_json) if tenant.config_json else {}
            
            return {
                'tenant_id': tenant.id,
                'products': products,
                'store_name': store_config.get('business_name', f"{current_user.email}'s Store"),
                'brand_personality': store_config.get('brand_personality', 'professional'),
                'domain': f"aiceo-{tenant.id}.replit.app"  # Custom subdomain
            }
            
        except Exception as e:
            logger.error(f"Failed to get user store: {e}")
            return None
    
    def create_product(self, user_id, product_data):
        """Create a new product in the headless store"""
        try:
            tenant = db.session.execute(select(Tenant).where(Tenant.owner_user_id == user_id)).scalar_one_or_none()
            if not tenant:
                raise ValueError("User has no tenant")
            
            # Generate product ID
            product_id = str(uuid.uuid4())
            
            # Prepare product data
            product = {
                'id': product_id,
                'user_id': user_id,
                'tenant_id': tenant.id,
                'name': product_data['name'],
                'description': product_data['description'],
                'price': float(product_data['price']),
                'type': product_data.get('type', 'digital'),  # digital, physical, service
                'images': product_data.get('images', []),
                'download_url': product_data.get('download_url'),  # For digital products
                'inventory': product_data.get('inventory', -1),  # -1 = unlimited
                'status': 'active',
                'created_at': datetime.utcnow().isoformat(),
                'stripe_price_id': None,  # Will be created on first purchase
                'sales_count': 0,
                'total_revenue': 0.0
            }
            
            # Load existing products
            products = []
            if os.path.exists(self.products_db):
                with open(self.products_db, 'r') as f:
                    products = json.load(f)
            
            # Add new product
            products.append(product)
            
            # Save products
            with open(self.products_db, 'w') as f:
                json.dump(products, f, indent=2)
            
            logger.info(f"✅ Product created: {product['name']} for user {user_id}")
            return product
            
        except Exception as e:
            logger.error(f"Product creation failed: {e}")
            raise
    
    def process_purchase(self, product_id, customer_email, payment_method_id=None):
        """Process a purchase through the headless store"""
        try:
            # Load product
            products = []
            if os.path.exists(self.products_db):
                with open(self.products_db, 'r') as f:
                    products = json.load(f)
            
            product = next((p for p in products if p['id'] == product_id), None)
            if not product:
                raise ValueError("Product not found")
            
            # Get the store owner's Stripe Connect account
            tenant = db.session.get(Tenant, product['tenant_id'])
            if not tenant or not tenant.stripe_connect_account_id:
                raise ValueError("Store owner has no payment account setup")
            
            # Create Stripe payment intent
            amount = int(product['price'] * 100)  # Convert to cents
            platform_fee = int(amount * 0.08)  # 8% platform fee
            
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                application_fee_amount=platform_fee,
                stripe_account=tenant.stripe_connect_account_id,
                metadata={
                    'product_id': product_id,
                    'product_name': product['name'],
                    'store_type': 'headless',
                    'customer_email': customer_email
                }
            )
            
            if payment_intent.status == 'succeeded':
                # Create order record
                order = {
                    'id': str(uuid.uuid4()),
                    'product_id': product_id,
                    'customer_email': customer_email,
                    'amount': product['price'],
                    'platform_fee': platform_fee / 100,
                    'stripe_payment_intent_id': payment_intent.id,
                    'status': 'completed',
                    'created_at': datetime.utcnow().isoformat(),
                    'tenant_id': tenant.id
                }
                
                # Save order
                orders = []
                if os.path.exists(self.orders_db):
                    with open(self.orders_db, 'r') as f:
                        orders = json.load(f)
                
                orders.append(order)
                
                with open(self.orders_db, 'w') as f:
                    json.dump(orders, f, indent=2)
                
                # Update product stats
                for p in products:
                    if p['id'] == product_id:
                        p['sales_count'] += 1
                        p['total_revenue'] += product['price']
                        break
                
                with open(self.products_db, 'w') as f:
                    json.dump(products, f, indent=2)
                
                logger.info(f"✅ Purchase completed: {product['name']} by {customer_email}")
                return order
            else:
                raise ValueError(f"Payment failed: {payment_intent.status}")
                
        except Exception as e:
            logger.error(f"Purchase processing failed: {e}")
            raise
    
    def get_store_analytics(self, user_id):
        """Get analytics for user's headless store"""
        try:
            products = []
            orders = []
            
            # Load data
            if os.path.exists(self.products_db):
                with open(self.products_db, 'r') as f:
                    all_products = json.load(f)
                    products = [p for p in all_products if p.get('user_id') == user_id]
            
            if os.path.exists(self.orders_db):
                with open(self.orders_db, 'r') as f:
                    all_orders = json.load(f)
                    # Get orders for user's products
                    user_product_ids = [p['id'] for p in products]
                    orders = [o for o in all_orders if o.get('product_id') in user_product_ids]
            
            # Calculate analytics
            total_revenue = sum(order['amount'] for order in orders)
            total_sales = len(orders)
            total_products = len(products)
            
            # Recent sales (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_orders = [
                o for o in orders 
                if datetime.fromisoformat(o['created_at']) > thirty_days_ago
            ]
            recent_revenue = sum(order['amount'] for order in recent_orders)
            
            return {
                'total_revenue': total_revenue,
                'total_sales': total_sales,
                'total_products': total_products,
                'recent_revenue': recent_revenue,
                'recent_sales': len(recent_orders),
                'products': products,
                'recent_orders': recent_orders[-10:]  # Last 10 orders
            }
            
        except Exception as e:
            logger.error(f"Analytics calculation failed: {e}")
            return {
                'total_revenue': 0,
                'total_sales': 0,
                'total_products': 0,
                'recent_revenue': 0,
                'recent_sales': 0,
                'products': [],
                'recent_orders': []
            }

# Initialize store manager
headless_store = HeadlessStore()

# Routes
@store_bp.route('/store')
@login_required
def store_dashboard():
    """User's headless store dashboard"""
    try:
        store_data = headless_store.get_user_store(current_user.id)
        analytics = headless_store.get_store_analytics(current_user.id)
        
        return render_template('store_dashboard.html', 
                             store=store_data, 
                             analytics=analytics)
    except Exception as e:
        logger.error(f"Store dashboard failed: {e}")
        return redirect(url_for('dashboard'))

@store_bp.route('/store/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    """Create a new product"""
    if request.method == 'POST':
        try:
            data = request.get_json() or request.form
            
            product_data = {
                'name': data['name'],
                'description': data['description'],
                'price': data['price'],
                'type': data.get('type', 'digital'),
                'images': data.get('images', []),
                'download_url': data.get('download_url'),
                'inventory': data.get('inventory', -1)
            }
            
            product = headless_store.create_product(current_user.id, product_data)
            
            if request.is_json:
                return jsonify({'success': True, 'product': product})
            else:
                return redirect(url_for('store.store_dashboard'))
                
        except Exception as e:
            logger.error(f"Product creation failed: {e}")
            if request.is_json:
                return jsonify({'error': str(e)}), 500
            else:
                return redirect(url_for('store.create_product') + '?error=creation_failed')
    
    return render_template('create_product.html')

@store_bp.route('/store/buy/<product_id>')
def buy_product(product_id):
    """Public product purchase page"""
    try:
        # Load product
        products = []
        if os.path.exists(headless_store.products_db):
            with open(headless_store.products_db, 'r') as f:
                products = json.load(f)
        
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            return "Product not found", 404
        
        return render_template('product_purchase.html', product=product)
        
    except Exception as e:
        logger.error(f"Product page failed: {e}")
        return "Error loading product", 500

@store_bp.route('/store/purchase', methods=['POST'])
def process_purchase():
    """Process product purchase"""
    try:
        data = request.get_json()
        product_id = data['product_id']
        customer_email = data['customer_email']
        payment_method_id = data.get('payment_method_id')
        
        order = headless_store.process_purchase(product_id, customer_email, payment_method_id)
        
        return jsonify({
            'success': True,
            'order': order,
            'message': 'Purchase completed successfully!'
        })
        
    except Exception as e:
        logger.error(f"Purchase failed: {e}")
        return jsonify({'error': str(e)}), 500

@store_bp.route('/store/analytics')
@login_required
def store_analytics():
    """Store analytics API"""
    try:
        analytics = headless_store.get_store_analytics(current_user.id)
        return jsonify(analytics)
    except Exception as e:
        logger.error(f"Analytics failed: {e}")
        return jsonify({'error': str(e)}), 500

@store_bp.route('/api/store/generate-product', methods=['POST'])
@login_required
def ai_generate_product():
    """Use AI to generate a trending product"""
    try:
        data = request.get_json() or {}
        niche = data.get('niche', 'digital tools')
        target_audience = data.get('target_audience', 'entrepreneurs')
        
        # AI-generated product (simplified for demo)
        ai_products = [
            {
                'name': f'{niche.title()} Masterclass Bundle',
                'description': f'Complete digital course teaching {target_audience} how to master {niche}. Includes video lessons, templates, and bonus materials.',
                'price': 97.00,
                'type': 'digital',
                'images': ['/static/img/course-placeholder.jpg'],
                'download_url': f'https://aiceo-content.replit.app/courses/{niche.replace(" ", "-").lower()}'
            },
            {
                'name': f'{niche.title()} Templates Pack',
                'description': f'50+ professional templates for {target_audience} working in {niche}. Save hours of work with ready-to-use designs.',
                'price': 47.00,
                'type': 'digital',
                'images': ['/static/img/templates-placeholder.jpg'],
                'download_url': f'https://aiceo-content.replit.app/templates/{niche.replace(" ", "-").lower()}'
            },
            {
                'name': f'{niche.title()} Automation Tools',
                'description': f'Custom software tools for {target_audience} to automate {niche} workflows. Lifetime license included.',
                'price': 197.00,
                'type': 'digital',
                'images': ['/static/img/software-placeholder.jpg'],
                'download_url': f'https://aiceo-content.replit.app/tools/{niche.replace(" ", "-").lower()}'
            }
        ]
        
        # Select random product
        import random
        selected_product = random.choice(ai_products)
        
        # Create the product
        product = headless_store.create_product(current_user.id, selected_product)
        
        return jsonify({
            'success': True,
            'product': product,
            'message': f'AI generated {selected_product["name"]} for your store!'
        })
        
    except Exception as e:
        logger.error(f"AI product generation failed: {e}")
        return jsonify({'error': str(e)}), 500

@store_bp.route('/store/launch-instant', methods=['POST'])
@login_required
def launch_instant_store():
    """Launch instant store with AI-generated products"""
    try:
        data = request.get_json() or {}
        niche = data.get('niche', 'digital marketing')
        
        # Generate 3 products for instant store
        products_created = []
        for i in range(3):
            try:
                response = ai_generate_product()
                if response.get_json()['success']:
                    products_created.append(response.get_json()['product'])
            except:
                continue
        
        if products_created:
            return jsonify({
                'success': True,
                'products_created': len(products_created),
                'products': products_created,
                'store_url': f'/store/public/{current_user.id}',
                'message': f'Instant store launched with {len(products_created)} products!'
            })
        else:
            return jsonify({'error': 'Failed to generate products'}), 500
            
    except Exception as e:
        logger.error(f"Instant store launch failed: {e}")
        return jsonify({'error': str(e)}), 500

@store_bp.route('/store/public/<int:user_id>')
def public_store(user_id):
    """Public storefront for a user"""
    try:
        store_data = headless_store.get_user_store(user_id)
        if not store_data:
            return "Store not found", 404
        
        return render_template('public_store.html', store=store_data)
        
    except Exception as e:
        logger.error(f"Public store failed: {e}")
        return "Error loading store", 500

@store_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks for headless store"""
    try:
        payload = request.get_data()
        sig_header = request.headers.get('Stripe-Signature')
        
        # Verify webhook signature
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        if not webhook_secret:
            logger.warning("No webhook secret configured")
            return '', 400
        
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        
        # Handle payment success
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            product_id = payment_intent['metadata'].get('product_id')
            customer_email = payment_intent['metadata'].get('customer_email')
            
            if product_id and customer_email:
                logger.info(f"✅ Payment succeeded for product {product_id}")
                # Additional processing could go here (send download links, etc.)
        
        return '', 200
        
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}")
        return '', 400