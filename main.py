import streamlit as st
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import core modules
from agent import Agent
from agent_logic import generate_business_ideas, create_digital_product
from auto_loop import AutoLoop
from profit_tracker import log_profit, get_total_revenue, get_profit_data
from marketplace_uploader import upload_product_to_shopify
from payment_processor import create_stripe_payment
from models import create_all
from success_dashboard import get_success_metrics_safe, get_comprehensive_dashboard_safe
from one_click_enhanced import OneClickBusinessGenerator
from agent_session import AgentSession
from google_trends_tool import get_trending_keywords
from marketing_tools.email_generator import generate_email_sequence
from marketing_tools.ad_writer import generate_ad_copy
from marketing_tools.scheduler import get_scheduled_jobs
from billing import is_subscription_active, get_user_subscription
from config import *

# Initialize database for Streamlit
# init_streamlit_db() # Assuming this is handled elsewhere or not needed for this version

# Set page config
st.set_page_config(
    page_title="AI CEO - Autonomous Business System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🤖 AI CEO SaaS - Autonomous Business System")
    st.subheader("Multi-Tenant SaaS Platform with Shopify + Stripe Integration")

    # Sidebar for navigation
    st.sidebar.title("🤖 AI CEO Dashboard")

    # Show SaaS features in sidebar
    st.sidebar.markdown("### 🚀 NEW: SaaS Features")
    st.sidebar.info("✅ Billing & Subscriptions\n✅ Team Management\n✅ Marketing Tools\n✅ 1-Click Generator\n✅ Timeline Tracking")

    if st.sidebar.button("🌐 Open SaaS App"):
        st.sidebar.markdown("**SaaS App:** [http://localhost:5000](http://localhost:5000)")

    st.sidebar.markdown("---")

    page = st.sidebar.selectbox(
        "Navigation",
        ["🏠 Dashboard", "🎯 Agent Control", "📈 Success Metrics", "🚀 One-Click Generator", 
         "⚙️ Auto Pilot", "💰 Profit Tracker", "🛍️ Product Manager", "📊 Analytics",
         "🔄 Auto Loop Status", "🎲 Agent Sessions", "📈 Trending Analysis", "🛠️ SaaS Features"]
    )

    # Render the selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🎯 Agent Control":
        show_agent_control()
    elif page == "📈 Success Metrics":
        show_success_metrics_page()
    elif page == "🚀 One-Click Generator":
        show_one_click_generator_page()
    elif page == "⚙️ Auto Pilot":
        show_auto_pilot_page()
    elif page == "💰 Profit Tracker":
        show_profit_tracker_page()
    elif page == "🛍️ Product Manager":
        show_product_manager_page()
    elif page == "📊 Analytics":
        show_analytics_page()
    elif page == "🔄 Auto Loop Status":
        show_auto_loop_status_page()
    elif page == "🎲 Agent Sessions":
        show_agent_sessions_page()
    elif page == "📈 Trending Analysis":
        show_trending_analysis_page()
    elif page == "🛠️ SaaS Features":
        show_saas_features_page()

# --- Page Functions ---

def show_dashboard():
    st.header("🏠 AI CEO Full Automation Dashboard")
    st.write("Welcome to your 100% Automated Business System!")
    
    # Full Automation Controls
    st.subheader("🤖 Full Automation System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 START FULL AUTOMATION", type="primary", use_container_width=True):
            st.success("🤖 Full automation system starting...")
            st.info("The AI CEO will now:\n• Scan for trending products\n• Create digital products\n• Build stores automatically\n• Upload to marketplace\n• Launch marketing campaigns\n• Learn and improve continuously")
            
            # Run single cycle for demo
            try:
                from full_automation_controller import run_single_automation_cycle
                with st.spinner("Running automation cycle..."):
                    result = run_single_automation_cycle()
                
                if result.get("success"):
                    st.success(f"✅ Automation cycle completed!")
                    st.write(f"📊 Products created: {result.get('products_created', 0)}")
                    st.write(f"🏪 Stores built: {result.get('stores_built', 0)}")
                    st.write(f"📢 Campaigns launched: {result.get('campaigns_launched', 0)}")
                    st.write(f"⏱️ Duration: {result.get('duration', 0):.1f} seconds")
                else:
                    st.error("❌ Automation cycle encountered errors")
                    if result.get("errors"):
                        st.write("Errors:", result["errors"])
                        
            except Exception as e:
                st.error(f"Automation error: {e}")
    
    with col2:
        if st.button("🔍 SCAN TRENDING NOW", use_container_width=True):
            try:
                from web_scanner import scan_for_trending_products
                with st.spinner("Scanning for trending products..."):
                    trending = scan_for_trending_products()
                
                st.success(f"✅ Found {len(trending)} trending opportunities!")
                
                if trending:
                    st.subheader("🔥 Top Trending Opportunities")
                    for i, trend in enumerate(trending[:5], 1):
                        with st.expander(f"{i}. {trend.get('title', 'Unknown')} (Score: {trend.get('interest_score', 0)})"):
                            st.write(f"**Type:** {trend.get('product_type', 'Unknown')}")
                            st.write(f"**Price:** ${trend.get('suggested_price', 0):.2f}")
                            st.write(f"**Market Size:** {trend.get('market_size', 'Unknown')}")
                            st.write(f"**Competition:** {trend.get('competition', 'Unknown')}")
                            st.write(f"**Description:** {trend.get('description', 'No description')}")
                            
            except Exception as e:
                st.error(f"Trending scan error: {e}")
    
    with col3:
        if st.button("🧠 AI INTELLIGENCE", use_container_width=True):
            try:
                from ai_memory_system import get_ai_intelligence
                intelligence = get_ai_intelligence()
                
                st.success("🧠 AI Intelligence Report")
                st.write(f"**Total Experiences:** {intelligence.get('total_experiences', 0)}")
                st.write(f"**Learning Status:** {intelligence.get('learning_status', 'Unknown')}")
                
                if intelligence.get('top_niches'):
                    st.write("**Best Performing Niches:**")
                    for niche in intelligence['top_niches'][:3]:
                        st.write(f"• {niche['niche']}: {niche['success_rate']:.1%} success")
                        
            except Exception as e:
                st.error(f"AI intelligence error: {e}")
    
    # Real-time Status
    st.subheader("📊 Real-time Status")
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    
    try:
        from profit_tracker import get_total_revenue
        total_revenue = get_total_revenue()
        status_col1.metric("💰 Total Revenue", f"${total_revenue:.2f}")
    except:
        status_col1.metric("💰 Total Revenue", "$0.00")
    
    status_col2.metric("🎯 Products Created", "0", help="Products created this session")
    status_col3.metric("🏪 Stores Built", "0", help="Automated stores built")
    status_col4.metric("📢 Campaigns Active", "0", help="Marketing campaigns running")
    
    # Automation Features Overview
    st.subheader("🚀 Automation Features")
    
    features = [
        "🔍 **Web Scanning:** Automatically scans Google Trends, Reddit, Amazon for trending products",
        "🎯 **Product Creation:** AI generates digital products based on market demand",
        "🏪 **Store Building:** Fully automated Shopify store creation and customization",
        "📦 **Marketplace Upload:** Automatic product upload with SEO optimization",
        "📢 **Marketing Campaigns:** AI-generated ad copy and email sequences",
        "🧠 **AI Learning:** Continuous improvement based on performance data",
        "💰 **Revenue Tracking:** Real-time profit monitoring and reinvestment",
        "⚡ **Zero-Touch Operation:** Just click start and let AI handle everything"
    ]
    
    for feature in features:
        st.markdown(feature)

def show_agent_control():
    st.header("🎯 Agent Control")
    st.write("Control and manage your AI agents.")

    # Placeholder for agent control UI
    st.info("Agent control interface coming soon.")

def show_success_metrics_page():
    st.header("📈 Success Metrics")
    st.write("Track your business growth and success metrics.")
    
    try:
        # Use safe functions that don't require Flask context
        user_id_for_metrics = 1
        metrics = get_success_metrics_safe(user_id_for_metrics)
        
        st.subheader("Key Performance Indicators")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${metrics.get('total_revenue', 0):.2f}")
        col2.metric("Products Launched", metrics.get('products_created', 0))
        col3.metric("Orders Fulfilled", metrics.get('orders_fulfilled', 0))

        st.subheader("Comprehensive Dashboard")
        comprehensive_data = get_comprehensive_dashboard_safe(user_id_for_metrics)
        st.dataframe(comprehensive_data, use_container_width=True)

    except Exception as e:
        st.error(f"Could not load success metrics: {e}")
        st.info("Using demo data - connect database for real metrics")

def show_one_click_generator_page():
    st.header("🚀 One-Click Business Generator")
    st.write("Generate a complete business idea, products, and marketing strategy.")

    # Use demo user ID for Streamlit interface
    demo_user_id = 1
    generator = OneClickBusinessGenerator(demo_user_id)

    niche = st.text_input("Enter Business Niche", placeholder="e.g., sustainable fashion, AI productivity tools")
    
    if st.button("Generate Business"):
        if niche:
            with st.spinner("Generating your business..."):
                try:
                    business_plan = generator.generate_business_plan(niche)
                    
                    st.success("Business generated successfully!")
                    st.subheader("Business Plan")
                    st.write(business_plan)
                    
                    # Example: Display generated products
                    st.subheader("Generated Products")
                    products = generator.get_generated_products()
                    if products:
                        for product in products:
                            st.write(f"- {product['title']}: ${product['price']}")
                    else:
                        st.info("No products generated for this niche.")

                except Exception as e:
                    st.error(f"Error generating business: {e}")
        else:
            st.warning("Please enter a business niche.")

def show_auto_pilot_page():
    st.header("⚙️ Auto Pilot")
    st.write("Automate your business operations with the AI CEO.")

    auto_loop = AutoLoop()

    if st.button("Start Auto Pilot Cycle"):
        with st.spinner("Running autonomous cycle..."):
            try:
                result = auto_loop.run_cycle()
                st.success(f"Auto pilot cycle completed: {result}")
            except Exception as e:
                st.error(f"Error running auto pilot cycle: {e}")
    
    st.subheader("Current Status")
    st.info("Auto Pilot is ready. Click 'Start Auto Pilot Cycle' to begin.")

def show_profit_tracker_page():
    st.header("💰 Profit Tracker")
    st.write("Monitor your business revenue and profits.")

    try:
        total_revenue = get_total_revenue()
        st.metric("Total Revenue", f"${total_revenue:.2f}")

        profit_data = get_profit_data()
        if profit_data:
            df_profit = pd.DataFrame(profit_data)
            st.dataframe(df_profit, use_container_width=True)
            
            # Visualize profit
            fig = px.bar(df_profit, x='source', y='amount', title='Profit by Source')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No profit data available yet.")
    
    except Exception as e:
        st.error(f"Could not load profit data: {e}")

def show_product_manager_page():
    st.header("🛍️ Product Manager")
    st.write("Manage your products, upload to Shopify, and track sales.")

    st.subheader("Upload Product to Shopify")
    with st.form("shopify_upload_form"):
        product_title = st.text_input("Product Title")
        product_description = st.text_area("Product Description")
        product_price = st.number_input("Price ($)", min_value=0.01, format="%.2f")

        if st.form_submit_button("Upload Product"):
            if product_title and product_description:
                product_data = {
                    "title": product_title,
                    "description": product_description,
                    "price": str(product_price)
                }
                with st.spinner("Uploading to Shopify..."):
                    try:
                        upload_result = upload_product_to_shopify(product_data)
                        if upload_result.get("success"):
                            st.success("Product uploaded successfully!")
                            st.markdown(f"[View Product]({upload_result.get('url')})")
                        else:
                            st.error(f"Shopify upload failed: {upload_result.get('error')}")
                    except Exception as e:
                        st.error(f"Error during Shopify upload: {e}")
            else:
                st.warning("Please provide title and description for the product.")

def show_analytics_page():
    st.header("📊 Analytics")
    st.write("Detailed analytics for your business performance.")
    
    st.subheader("Revenue Trends")
    try:
        total_revenue = get_total_revenue()
        st.metric("Total Revenue", f"${total_revenue:.2f}")
        
        # Dummy data for trend visualization
        dates = pd.to_datetime(pd.date_range(start=datetime.now() - pd.Timedelta(days=30), periods=30, freq='D'))
        revenues = [max(0, total_revenue * (1 + (i-15)/30 * 0.2 + (i % 5 - 2) * 0.05)) for i in range(30)] # Simulate some fluctuation
        df_trends = pd.DataFrame({'Date': dates, 'Revenue': revenues})
        
        fig_trends = px.line(df_trends, x='Date', y='Revenue', title='Daily Revenue Trend')
        st.plotly_chart(fig_trends, use_container_width=True)
        
    except Exception as e:
        st.error(f"Could not load analytics data: {e}")

def show_auto_loop_status_page():
    st.header("🔄 Auto Loop Status")
    st.write("Monitor the status of your autonomous business cycles.")
    
    st.info("Auto Loop status information will be displayed here.")

def show_agent_sessions_page():
    st.header("🎲 Agent Sessions")
    st.write("Manage and review individual agent sessions.")

    st.subheader("Create New Agent Session")
    user_id = st.text_input("User ID", placeholder="Enter User ID")
    if st.button("Start New Session"):
        if user_id:
            try:
                session = AgentSession.create(user_id)
                st.success(f"Agent session started for user {user_id} with ID: {session.session_id}")
                st.write(f"Session ID: {session.session_id}")
            except Exception as e:
                st.error(f"Failed to start agent session: {e}")
        else:
            st.warning("Please enter a User ID.")

    st.subheader("Active Sessions")
    # Placeholder for listing active sessions
    st.info("List of active agent sessions will appear here.")

def show_trending_analysis_page():
    st.header("📈 Trending Analysis")
    st.write("Discover trending keywords and market opportunities.")

    keyword = st.text_input("Enter keyword for trend analysis", placeholder="e.g., AI, fitness, crypto")
    
    if st.button("Analyze Trends"):
        if keyword:
            with st.spinner("Fetching trending keywords..."):
                try:
                    trends = get_trending_keywords(keyword)
                    st.subheader(f"Trending Keywords for '{keyword}'")
                    
                    if trends:
                        df_trends = pd.DataFrame(trends)
                        st.dataframe(df_trends, use_container_width=True)
                        
                        # Visualize trends
                        fig_trends = px.line(df_trends, x='date', y='volume', title='Search Volume Trend')
                        st.plotly_chart(fig_trends, use_container_width=True)
                    else:
                        st.info("No trend data found for this keyword.")
                except Exception as e:
                    st.error(f"Error fetching trends: {e}")
        else:
            st.warning("Please enter a keyword.")

def show_saas_features_page():
    st.header("🛠️ SaaS Platform Features")
    st.write("Explore the advanced features of our AI CEO SaaS platform.")

    st.markdown("### Core SaaS Modules")
    features = [
        "**Billing & Subscriptions:** Securely manage recurring payments and subscription plans.",
        "**Team Management:** Collaborate with your team by adding members and assigning roles.",
        "**Marketing Tools:** Leverage AI-powered email sequences, ad copy generation, and scheduling.",
        "**1-Click Business Generator:** Instantly create new business ideas, products, and strategies.",
        "**Timeline Tracking:** Monitor project progress and key business milestones.",
        "**Branding & White-labeling:** Customize the platform with your own brand identity (Enterprise feature).",
        "**Plugin Marketplace:** Extend functionality with third-party integrations (Coming Soon)."
    ]
    for feature in features:
        st.markdown(f"- {feature}")

    st.markdown("### Pricing Plans")
    plans = {
        "Starter": {"price": "$29/month", "features": ["Basic AI CEO Access", "5 Products/Month", "Basic Support"]},
        "Pro": {"price": "$99/month", "features": ["Advanced AI CEO", "Unlimited Products", "Team Management", "Marketing Tools"]},
        "Enterprise": {"price": "$299+/month", "features": ["Custom AI Models", "White-labeling", "Priority Support", "Dedicated Account Manager"]}
    }

    col1, col2, col3 = st.columns(3)
    plan_columns = [col1, col2, col3]

    for i, (plan_name, details) in enumerate(plans.items()):
        with plan_columns[i]:
            st.subheader(plan_name)
            st.write(f"**{details['price']}**")
            for feature in details['features']:
                st.write(f"• {feature}")
            if st.button(f"Get {plan_name}", key=f"plan_{plan_name}"):
                st.info(f"Redirecting to {plan_name} subscription page...")
                # In a real app, this would link to a payment page or checkout flow

if __name__ == "__main__":
    print("🎯 Test log to Console - Main.py is running!")
    print("🔍 Console output test - if you see this, console IS working!")
    print("🔍 Check the Console tab (not Logs) to see these messages")
    print("✅ Starting AI CEO SaaS App...")
    main()