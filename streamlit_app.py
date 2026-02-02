"""
Server Log Analysis - Streamlit Application
Interactive dashboard for analyzing server logs with custom profiling
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

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
st.sidebar.info("💡 **Tip:** Each section provides detailed profiling and visualizations.")

# Load data function
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Custom profiling function
def generate_custom_profile(df, title):
    st.subheader(f"📊 {title} - Detailed Profile")
    
    # Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())
    with col4:
        st.metric("Duplicate Rows", df.duplicated().sum())
    
    # Data types
    st.subheader("📋 Column Information")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.values,
        'Non-Null Count': df.count().values,
        'Null Count': df.isnull().sum().values,
        'Unique Values': [df[col].nunique() for col in df.columns]
    })
    st.dataframe(col_info, use_container_width=True)
    
    # Statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.subheader("📈 Numeric Columns Statistics")
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    
    # Value counts for categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        st.subheader("📊 Categorical Columns - Top Values")
        for col in categorical_cols[:5]:  # Show first 5 categorical columns
            with st.expander(f"🔍 {col}"):
                value_counts = df[col].value_counts().head(10)
                fig = px.bar(x=value_counts.index, y=value_counts.values,
                           labels={'x': col, 'y': 'Count'},
                           title=f"Top 10 values in {col}")
                st.plotly_chart(fig, use_container_width=True)
    
    # Sample data
    st.subheader("📄 Sample Data (First 10 Rows)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Correlation matrix for numeric columns
    if len(numeric_cols) > 1:
        st.subheader("🔗 Correlation Matrix")
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(corr_matrix, 
                       text_auto=True, 
                       aspect="auto",
                       title="Correlation Heatmap",
                       color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)


# ==================== ANALYSIS 1: USER LOGIN ====================
if "1️⃣" in analysis_type:
    st.markdown('<p class="sub-header">1️⃣ User Login Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('1_user_login_log.csv')
    
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
        fig = px.pie(df, names='login_status', title='Login Success vs Failed',
                    color_discrete_sequence=['#2ecc71', '#e74c3c'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Login Methods Used")
        method_counts = df['login_method'].value_counts()
        fig = px.bar(x=method_counts.index, y=method_counts.values, 
                     labels={'x': 'Login Method', 'y': 'Count'},
                     color=method_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Device Type Distribution")
        device_counts = df['device_type'].value_counts()
        fig = px.pie(values=device_counts.values, names=device_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Browser Usage")
        browser_counts = df['browser'].value_counts()
        fig = px.bar(x=browser_counts.index, y=browser_counts.values,
                    labels={'x': 'Browser', 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Profiling
    st.markdown("---")
    if st.button("📊 Show Detailed Profile Report", key="login_profile"):
        generate_custom_profile(df, "User Login Analysis")


# ==================== ANALYSIS 2: SESSION DURATION ====================
elif "2️⃣" in analysis_type:
    st.markdown('<p class="sub-header">2️⃣ Session Duration Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('2_session_duration_log.csv')
    
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
                          labels={'duration_minutes': 'Duration (minutes)'},
                          color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Session Status")
        status_counts = df['session_status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Transfer Distribution")
        fig = px.histogram(df, x='data_transferred_mb', nbins=30,
                          labels={'data_transferred_mb': 'Data Transferred (MB)'},
                          color_discrete_sequence=['#9b59b6'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Pages Accessed Distribution")
        fig = px.histogram(df, x='pages_accessed', nbins=30,
                          labels={'pages_accessed': 'Pages Accessed'},
                          color_discrete_sequence=['#f39c12'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot
    st.subheader("Duration vs Data Transferred")
    fig = px.scatter(df, x='duration_minutes', y='data_transferred_mb',
                    color='session_status',
                    labels={'duration_minutes': 'Duration (minutes)',
                           'data_transferred_mb': 'Data Transferred (MB)'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Profiling
    st.markdown("---")
    if st.button("📊 Show Detailed Profile Report", key="session_profile"):
        generate_custom_profile(df, "Session Duration Analysis")


# ==================== ANALYSIS 3: AUTHENTICATION ATTEMPTS ====================
elif "3️⃣" in analysis_type:
    st.markdown('<p class="sub-header">3️⃣ Authentication Attempts Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('3_authentication_attempts_log.csv')
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Attempts", len(df))
    with col2:
        unauth_count = (df['auth_result'] == 'UNAUTHENTIC').sum()
        st.metric("🚨 Unauthentic Attempts", unauth_count, delta=f"{unauth_count/len(df)*100:.1f}%", delta_color="inverse")
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
                     color_discrete_map={'AUTHENTIC': '#2ecc71', 'UNAUTHENTIC': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Failure Reasons (Unauthentic)")
        failure_df = df[df['auth_result'] == 'UNAUTHENTIC']
        if len(failure_df) > 0:
            failure_counts = failure_df['failure_reason'].value_counts()
            fig = px.pie(values=failure_counts.values, names=failure_counts.index)
            st.plotly_chart(fig, use_container_width=True)
    
    # Geographic distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Geographic Distribution")
        geo_counts = df['geolocation'].value_counts()
        fig = px.bar(x=geo_counts.index, y=geo_counts.values,
                    labels={'x': 'Country', 'y': 'Attempts'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Attempt Count Distribution")
        fig = px.histogram(df, x='attempt_count', nbins=20,
                          labels={'attempt_count': 'Number of Attempts'},
                          color_discrete_sequence=['#e67e22'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Suspicious IPs
    st.subheader("🚨 Top 10 Suspicious IP Addresses")
    suspicious_df = df[df['auth_result'] == 'UNAUTHENTIC'].groupby('ip_address').size().sort_values(ascending=False).head(10)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(suspicious_df.to_frame('Failed Attempts'), use_container_width=True)
    
    with col2:
        fig = px.bar(x=suspicious_df.values, y=suspicious_df.index, orientation='h',
                    labels={'x': 'Failed Attempts', 'y': 'IP Address'},
                    color_discrete_sequence=['#c0392b'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Profiling
    st.markdown("---")
    if st.button("📊 Show Detailed Profile Report", key="auth_profile"):
        generate_custom_profile(df, "Authentication Attempts Analysis")


# ==================== ANALYSIS 4: SECURITY EVENTS ====================
elif "4️⃣" in analysis_type:
    st.markdown('<p class="sub-header">4️⃣ Security Events Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('4_security_events_log.csv')
    
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
                     color=event_counts.index,
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Severity Distribution")
        severity_counts = df['severity'].value_counts()
        colors_map = {'LOW': '#2ecc71', 'MEDIUM': '#f39c12', 'HIGH': '#e67e22', 'CRITICAL': '#c0392b'}
        fig = px.pie(values=severity_counts.values, names=severity_counts.index,
                    color=severity_counts.index,
                    color_discrete_map=colors_map)
        st.plotly_chart(fig, use_container_width=True)
    
    # Attack Analysis
    st.subheader("🎯 Attack Analysis Details")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Blank Requests Analysis:**")
        blank_df = df[df['event_type'] == 'BLANK_REQUEST']
        st.write(f"- Total: **{len(blank_df)}**")
        st.write(f"- Blocked: **{blank_df['blocked'].sum()}**")
        st.write(f"- Critical: **{(blank_df['severity'] == 'CRITICAL').sum()}**")
        st.write(f"- Block Rate: **{blank_df['blocked'].sum()/len(blank_df)*100:.1f}%**")
    
    with col2:
        st.markdown("**DOS Attacks Analysis:**")
        dos_df = df[df['event_type'] == 'DOS_ATTACK']
        st.write(f"- Total: **{len(dos_df)}**")
        st.write(f"- Blocked: **{dos_df['blocked'].sum()}**")
        st.write(f"- Avg RPS: **{dos_df['requests_per_second'].mean():.0f}**")
        st.write(f"- Max RPS: **{dos_df['requests_per_second'].max()}**")
    
    with col3:
        st.markdown("**Other Threats:**")
        sql_inj = (df['event_type'] == 'SQL_INJECTION').sum()
        xss = (df['event_type'] == 'XSS_ATTEMPT').sum()
        st.write(f"- SQL Injection: **{sql_inj}**")
        st.write(f"- XSS Attempts: **{xss}**")
        st.write(f"- Normal Traffic: **{(df['event_type'] == 'NORMAL').sum()}**")
    
    # Request patterns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Requests Per Second Distribution")
        fig = px.histogram(df, x='requests_per_second', nbins=30,
                          labels={'requests_per_second': 'Requests/Second'},
                          color='event_type')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Blocked vs Allowed")
        blocked_counts = df['blocked'].value_counts()
        fig = px.pie(values=blocked_counts.values, 
                    names=['Blocked' if x else 'Allowed' for x in blocked_counts.index],
                    color_discrete_sequence=['#e74c3c', '#95a5a6'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Top attacking IPs
    st.subheader("🚨 Top 10 Source IPs by Attack Volume")
    attack_df = df[df['event_type'].isin(['BLANK_REQUEST', 'DOS_ATTACK', 'SQL_INJECTION', 'XSS_ATTEMPT'])]
    top_ips = attack_df['source_ip'].value_counts().head(10)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(x=top_ips.index, y=top_ips.values,
                    labels={'x': 'Source IP', 'y': 'Attack Count'},
                    color_discrete_sequence=['#c0392b'])
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(top_ips.to_frame('Attack Count'), use_container_width=True)
    
    # Detailed Profiling
    st.markdown("---")
    if st.button("📊 Show Detailed Profile Report", key="security_profile"):
        generate_custom_profile(df, "Security Events Analysis")


# ==================== ANALYSIS 5: SERVICE SUBSCRIPTIONS ====================
elif "5️⃣" in analysis_type:
    st.markdown('<p class="sub-header">5️⃣ Service Subscription Analysis</p>', unsafe_allow_html=True)
    
    df = load_data('5_service_subscription_log.csv')
    
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
        fig = px.pie(values=service_counts.values, names=service_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Popular Services")
        service_name_counts = df['service_name'].value_counts()
        fig = px.bar(x=service_name_counts.values, y=service_name_counts.index,
                     orientation='h',
                     labels={'x': 'Subscriptions', 'y': 'Service'},
                     color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Revenue Analysis
    st.subheader("💰 Revenue Analysis by Service Type")
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_by_type = df[df['subscription_status'] == 'ACTIVE'].groupby('service_type')['monthly_fee_usd'].sum().sort_values(ascending=False)
        fig = px.bar(x=revenue_by_type.index, y=revenue_by_type.values,
                     labels={'x': 'Service Type', 'y': 'Monthly Revenue ($)'},
                     color=revenue_by_type.index)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue by service name
        revenue_by_service = df[df['subscription_status'] == 'ACTIVE'].groupby('service_name')['monthly_fee_usd'].sum().sort_values(ascending=False)
        fig = px.bar(x=revenue_by_service.values, y=revenue_by_service.index,
                     orientation='h',
                     labels={'x': 'Revenue ($)', 'y': 'Service'},
                     color_discrete_sequence=['#2ecc71'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Subscription Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Subscription Status Breakdown")
        status_counts = df['subscription_status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Auto-Renew Settings")
        auto_renew_counts = df['auto_renew'].value_counts()
        fig = px.pie(values=auto_renew_counts.values, 
                    names=['Enabled' if x else 'Disabled' for x in auto_renew_counts.index],
                    color_discrete_sequence=['#27ae60', '#95a5a6'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown table
    st.subheader("📋 Service Subscription Summary")
    summary = df.groupby(['service_type', 'service_name']).agg({
        'subscription_id': 'count',
        'monthly_fee_usd': 'sum'
    }).rename(columns={
        'subscription_id': 'Total Subscriptions',
        'monthly_fee_usd': 'Total Revenue ($)'
    }).sort_values('Total Revenue ($)', ascending=False)
    st.dataframe(summary, use_container_width=True)
    
    # Detailed Profiling
    st.markdown("---")
    if st.button("📊 Show Detailed Profile Report", key="subscription_profile"):
        generate_custom_profile(df, "Service Subscription Analysis")


# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🖥️ Server Log Analysis Dashboard | Built with Streamlit</p>
        <p>Use the sidebar to navigate between different analyses</p>
    </div>
""", unsafe_allow_html=True)
