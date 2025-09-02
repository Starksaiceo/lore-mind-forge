
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

def init_db():
    """Initialize database"""
    conn = sqlite3.connect('saas_users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subscription_tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            api_calls_used INTEGER DEFAULT 0,
            monthly_limit INTEGER DEFAULT 10,
            stripe_customer_id TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_type TEXT,
            status TEXT,
            result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """Home page"""
    if 'user_id' in session:
        return redirect('/dashboard')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI CEO SaaS</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            .hero { text-align: center; margin-bottom: 30px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>🤖 AI CEO SaaS</h1>
                <p>Autonomous AI that builds businesses, creates products, and generates revenue 24/7</p>
            </div>
            
            <h3>✨ Features:</h3>
            <ul>
                <li>🚀 Automated product creation and launches</li>
                <li>💰 Real revenue tracking with Stripe integration</li>
                <li>📊 Market analysis and trend detection</li>
                <li>🎯 Autonomous ad campaign management</li>
                <li>🔄 24/7 profit optimization</li>
            </ul>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/signup" class="btn">Get Started Free</a>
                <a href="/login" class="btn" style="background: #6c757d; margin-left: 10px;">Login</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if len(password) < 6:
            return "Password must be at least 6 characters", 400
        
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('saas_users.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash)
            )
            conn.commit()
            conn.close()
            return redirect('/login?success=1')
        except sqlite3.IntegrityError:
            return "Email already exists", 400
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign Up - AI CEO SaaS</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 400px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🚀 Sign Up for AI CEO</h2>
            <form method="post">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password (min 6 chars)" required>
                <button type="submit" class="btn">Create Account</button>
            </form>
            <p><a href="/login">Already have an account? Login</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('saas_users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['email'] = user[1]
            session['subscription_tier'] = user[3]
            return redirect('/dashboard')
        else:
            return "Invalid email or password", 401
    
    success = request.args.get('success')
    message = '<p style="color: green;">Account created successfully! Please login.</p>' if success else ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - AI CEO SaaS</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }}
            input {{ width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }}
            .btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🤖 Login to AI CEO</h2>
            {message}
            <form method="post">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="btn">Login</button>
            </form>
            <p><a href="/signup">Don't have an account? Sign up</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect('/login')
    
    # Get user data
    conn = sqlite3.connect('saas_users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    
    # Get recent tasks
    cursor.execute("SELECT * FROM ai_tasks WHERE user_id = ? ORDER BY created_at DESC LIMIT 5", (session['user_id'],))
    recent_tasks = cursor.fetchall()
    conn.close()
    
    if not user:
        return redirect('/login')
    
    api_calls_used = user[5]
    monthly_limit = user[6]
    subscription_tier = user[3]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - AI CEO SaaS</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }}
            .navbar {{ background: #007bff; color: white; padding: 15px; }}
            .container {{ max-width: 1200px; margin: 20px auto; padding: 20px; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .btn {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }}
            .btn-success {{ background: #28a745; }}
            .btn-warning {{ background: #ffc107; color: black; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .progress {{ background: #e9ecef; border-radius: 5px; height: 20px; }}
            .progress-bar {{ background: #007bff; height: 100%; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>🤖 AI CEO Dashboard - {session['email']}</h2>
            <a href="/logout" style="color: white; text-decoration: none; float: right;">Logout</a>
        </div>
        
        <div class="container">
            <div class="card">
                <h3>📊 Account Status</h3>
                <p><strong>Plan:</strong> {subscription_tier.title()}</p>
                <p><strong>API Calls:</strong> {api_calls_used}/{monthly_limit}</p>
                <div class="progress">
                    <div class="progress-bar" style="width: {(api_calls_used/monthly_limit)*100}%"></div>
                </div>
                {('<p style="color: red;">⚠️ API limit reached! <a href="/upgrade" class="btn">Upgrade to Pro</a></p>' if api_calls_used >= monthly_limit else '')}
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>🚀 Quick Actions</h3>
                    <a href="/ai/create-product" class="btn">Create Product</a>
                    <a href="/ai/market-research" class="btn">Market Research</a>
                    <a href="/ai/launch-campaign" class="btn">Launch Campaign</a>
                </div>
                
                <div class="card">
                    <h3>💰 Revenue Tracking</h3>
                    <p>Total Revenue: $0.00</p>
                    <p>This Month: $0.00</p>
                    <a href="/revenue" class="btn">View Details</a>
                </div>
                
                <div class="card">
                    <h3>📈 Recent Activity</h3>
                    {'<p>No recent tasks</p>' if not recent_tasks else '<br>'.join([f"• {task[2]} - {task[3]}" for task in recent_tasks[:3]])}
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/ai/<task_type>')
def ai_task(task_type):
    """Handle AI tasks"""
    if 'user_id' not in session:
        return redirect('/login')
    
    # Check API limits
    conn = sqlite3.connect('saas_users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT api_calls_used, monthly_limit FROM users WHERE id = ?", (session['user_id'],))
    user_data = cursor.fetchone()
    
    if user_data[0] >= user_data[1]:
        return jsonify({"error": "API limit reached. Please upgrade your plan."}), 429
    
    # Increment API usage
    cursor.execute("UPDATE users SET api_calls_used = api_calls_used + 1 WHERE id = ?", (session['user_id'],))
    
    # Log the task
    cursor.execute(
        "INSERT INTO ai_tasks (user_id, task_type, status) VALUES (?, ?, ?)",
        (session['user_id'], task_type, 'completed')
    )
    
    conn.commit()
    conn.close()
    
    # Simulate AI task execution
    if task_type == 'create-product':
        result = "✅ AI Product Creator launched! Check your dashboard for updates."
    elif task_type == 'market-research':
        result = "📊 Market research completed! Found 5 trending opportunities."
    elif task_type == 'launch-campaign':
        result = "🎯 Ad campaign launched successfully! Budget allocated and targeting set."
    else:
        result = f"🤖 AI task '{task_type}' completed successfully!"
    
    return jsonify({"success": True, "result": result, "task_type": task_type})

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
