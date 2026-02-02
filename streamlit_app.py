"""
Server Log Analysis - Streamlit Application
Interactive dashboard for analyzing server logs with pandas profiling
"""

import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Server Log Analysis Dashboard",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">🖥️ Server Log Analysis Dashboard</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Navigation")
analysis_type = st.sidebar.radio(
    "Select Analysis:",
    [
        "1️⃣ User Login Analysis",
        "2️⃣ Session Duration Analysis",
        "3️⃣ Authentication Attempts",
        "4️⃣ Security Events (DOS/Blank Requests)",
        "5️⃣ Service Subscriptions"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Each section provides detailed pandas profiling reports and visualizations.")

# Load data function
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Generate profile function
@st.cache_resource
def generate_profile(df, title):
    return ProfileReport(df, title=title, explorative=True, minimal=False)


# ==================== ANALYSIS 1: USER LOGIN ====================
if "1️⃣" in analysis_type:
    st.markdown('<p class="sub-header">1️⃣ User Login Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('/mnt/user-data/outputs/1_user_login_log.csv')
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Login Attempts", len(df))
    with col2:
        success_rate = (df['login_status'] == 'SUCCESS').sum() / len(df) * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")
    with col3:
        unique_users = df['user_id'].nunique()
        st.metric("Unique Users", unique_users)
    with col4:
        unique_ips = df['ip_address'].nunique()
        st.metric("Unique IPs", unique_ips)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login Status Distribution")
        fig = px.pie(df, names='login_status', title='Login Success vs Failed')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Login Methods Used")
        method_counts = df['login_method'].value_counts()
        fig = px.bar(x=method_counts.index, y=method_counts.values, 
                     labels={'x': 'Login Method', 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Pandas Profiling Report
    st.markdown("---")
    st.subheader("📊 Detailed Pandas Profiling Report")
    if st.button("Generate Full Profiling Report", key="login_profile"):
        with st.spinner("Generating comprehensive analysis..."):
            profile = generate_profile(df, "User Login Analysis")
            st_profile_report(profile)


# ==================== ANALYSIS 2: SESSION DURATION ====================
elif "2️⃣" in analysis_type:
    st.markdown('<p class="sub-header">2️⃣ Session Duration Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('/mnt/user-data/outputs/2_session_duration_log.csv')
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sessions", len(df))
    with col2:
        avg_duration = df['duration_minutes'].mean()
        st.metric("Avg Duration (min)", f"{avg_duration:.1f}")
    with col3:
        total_data = df['data_transferred_mb'].sum()
        st.metric("Total Data (MB)", f"{total_data:.1f}")
    with col4:
        avg_pages = df['pages_accessed'].mean()
        st.metric("Avg Pages/Session", f"{avg_pages:.1f}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Session Duration Distribution")
        fig = px.histogram(df, x='duration_minutes', nbins=30,
                          title='Distribution of Session Durations',
                          labels={'duration_minutes': 'Duration (minutes)'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Session Status")
        status_counts = df['session_status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    
    # Pandas Profiling Report
    st.markdown("---")
    st.subheader("📊 Detailed Pandas Profiling Report")
    if st.button("Generate Full Profiling Report", key="session_profile"):
        with st.spinner("Generating comprehensive analysis..."):
            profile = generate_profile(df, "Session Duration Analysis")
            st_profile_report(profile)


# ==================== ANALYSIS 3: AUTHENTICATION ATTEMPTS ====================
elif "3️⃣" in analysis_type:
    st.markdown('<p class="sub-header">3️⃣ Authentication Attempts Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('/mnt/user-data/outputs/3_authentication_attempts_log.csv')
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Attempts", len(df))
    with col2:
        unauth_count = (df['auth_result'] == 'UNAUTHENTIC').sum()
        st.metric("🚨 Unauthentic Attempts", unauth_count, delta=f"{unauth_count/len(df)*100:.1f}%")
    with col3:
        authentic_count = (df['auth_result'] == 'AUTHENTIC').sum()
        st.metric("✅ Authentic Attempts", authentic_count)
    with col4:
        risky_ips = df[df['auth_result'] == 'UNAUTHENTIC']['ip_address'].nunique()
        st.metric("Suspicious IPs", risky_ips)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Authentication Results")
        auth_counts = df['auth_result'].value_counts()
        fig = px.bar(x=auth_counts.index, y=auth_counts.values,
                     labels={'x': 'Result', 'y': 'Count'},
                     color=auth_counts.index,
                     color_discrete_map={'AUTHENTIC': 'green', 'UNAUTHENTIC': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Failure Reasons (Unauthentic)")
        failure_df = df[df['auth_result'] == 'UNAUTHENTIC']
        failure_counts = failure_df['failure_reason'].value_counts()
        fig = px.pie(values=failure_counts.values, names=failure_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Suspicious IPs
    st.subheader("🚨 Top Suspicious IP Addresses")
    suspicious_df = df[df['auth_result'] == 'UNAUTHENTIC'].groupby('ip_address').size().sort_values(ascending=False).head(10)
    st.dataframe(suspicious_df.to_frame('Failed Attempts'), use_container_width=True)
    
    # Pandas Profiling Report
    st.markdown("---")
    st.subheader("📊 Detailed Pandas Profiling Report")
    if st.button("Generate Full Profiling Report", key="auth_profile"):
        with st.spinner("Generating comprehensive analysis..."):
            profile = generate_profile(df, "Authentication Attempts Analysis")
            st_profile_report(profile)


# ==================== ANALYSIS 4: SECURITY EVENTS ====================
elif "4️⃣" in analysis_type:
    st.markdown('<p class="sub-header">4️⃣ Security Events Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('/mnt/user-data/outputs/4_security_events_log.csv')
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", len(df))
    with col2:
        blank_requests = (df['event_type'] == 'BLANK_REQUEST').sum()
        st.metric("🔴 Blank Requests", blank_requests)
    with col3:
        dos_attacks = (df['event_type'] == 'DOS_ATTACK').sum()
        st.metric("⚠️ DOS Attacks", dos_attacks)
    with col4:
        blocked_rate = df['blocked'].sum() / len(df) * 100
        st.metric("Blocked Rate", f"{blocked_rate:.1f}%")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Security Event Types")
        event_counts = df['event_type'].value_counts()
        fig = px.bar(x=event_counts.index, y=event_counts.values,
                     labels={'x': 'Event Type', 'y': 'Count'},
                     color=event_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Severity Distribution")
        severity_counts = df['severity'].value_counts()
        fig = px.pie(values=severity_counts.values, names=severity_counts.index,
                     color=severity_counts.index,
                     color_discrete_map={'LOW': 'green', 'MEDIUM': 'yellow', 
                                        'HIGH': 'orange', 'CRITICAL': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Attack Analysis
    st.subheader("🎯 Attack Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Blank Requests Analysis:**")
        blank_df = df[df['event_type'] == 'BLANK_REQUEST']
        st.write(f"- Total: {len(blank_df)}")
        st.write(f"- Blocked: {blank_df['blocked'].sum()}")
        st.write(f"- Critical: {(blank_df['severity'] == 'CRITICAL').sum()}")
    
    with col2:
        st.write("**DOS Attacks Analysis:**")
        dos_df = df[df['event_type'] == 'DOS_ATTACK']
        st.write(f"- Total: {len(dos_df)}")
        st.write(f"- Blocked: {dos_df['blocked'].sum()}")
        st.write(f"- Avg RPS: {dos_df['requests_per_second'].mean():.0f}")
    
    # Pandas Profiling Report
    st.markdown("---")
    st.subheader("📊 Detailed Pandas Profiling Report")
    if st.button("Generate Full Profiling Report", key="security_profile"):
        with st.spinner("Generating comprehensive analysis..."):
            profile = generate_profile(df, "Security Events Analysis")
            st_profile_report(profile)


# ==================== ANALYSIS 5: SERVICE SUBSCRIPTIONS ====================
elif "5️⃣" in analysis_type:
    st.markdown('<p class="sub-header">5️⃣ Service Subscription Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('/mnt/user-data/outputs/5_service_subscription_log.csv')
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Subscriptions", len(df))
    with col2:
        active_subs = (df['subscription_status'] == 'ACTIVE').sum()
        st.metric("Active Subscriptions", active_subs)
    with col3:
        total_revenue = df[df['subscription_status'] == 'ACTIVE']['monthly_fee_usd'].sum()
        st.metric("Monthly Revenue", f"${total_revenue:,.2f}")
    with col4:
        auto_renew_rate = df['auto_renew'].sum() / len(df) * 100
        st.metric("Auto-Renew Rate", f"{auto_renew_rate:.1f}%")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Service Type Distribution")
        service_counts = df['service_type'].value_counts()
        fig = px.pie(values=service_counts.values, names=service_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Popular Services")
        service_name_counts = df['service_name'].value_counts()
        fig = px.bar(x=service_name_counts.values, y=service_name_counts.index,
                     orientation='h',
                     labels={'x': 'Subscriptions', 'y': 'Service'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Revenue Analysis
    st.subheader("💰 Revenue Analysis by Service Type")
    revenue_by_type = df[df['subscription_status'] == 'ACTIVE'].groupby('service_type')['monthly_fee_usd'].sum().sort_values(ascending=False)
    fig = px.bar(x=revenue_by_type.index, y=revenue_by_type.values,
                 labels={'x': 'Service Type', 'y': 'Monthly Revenue ($)'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Subscription Status
    st.subheader("📊 Subscription Status Breakdown")
    status_df = df['subscription_status'].value_counts().to_frame('Count')
    st.dataframe(status_df, use_container_width=True)
    
    # Pandas Profiling Report
    st.markdown("---")
    st.subheader("📊 Detailed Pandas Profiling Report")
    if st.button("Generate Full Profiling Report", key="subscription_profile"):
        with st.spinner("Generating comprehensive analysis..."):
            profile = generate_profile(df, "Service Subscription Analysis")
            st_profile_report(profile)


# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🖥️ Server Log Analysis Dashboard | Built with Streamlit & Pandas Profiling</p>
        <p>Use the sidebar to navigate between different analyses</p>
    </div>
""", unsafe_allow_html=True)
