"""
Pandas Profiling Report Generator
Generates HTML profiling reports for all 5 server log files
"""

import pandas as pd
from ydata_profiling import ProfileReport
import os

# Create output directory for HTML reports
os.makedirs('/mnt/user-data/outputs/profiling_reports', exist_ok=True)

print("="*70)
print("GENERATING PANDAS PROFILING REPORTS")
print("="*70)

# File configurations
files_config = [
    {
        'file': '/mnt/user-data/outputs/1_user_login_log.csv',
        'title': 'User Login Analysis',
        'description': 'Analysis of user login attempts on the server'
    },
    {
        'file': '/mnt/user-data/outputs/2_session_duration_log.csv',
        'title': 'Session Duration Analysis',
        'description': 'Analysis of user session durations and server access patterns'
    },
    {
        'file': '/mnt/user-data/outputs/3_authentication_attempts_log.csv',
        'title': 'Authentication Attempts Analysis',
        'description': 'Analysis of authenticated and unauthenticated access attempts'
    },
    {
        'file': '/mnt/user-data/outputs/4_security_events_log.csv',
        'title': 'Security Events Analysis',
        'description': 'Analysis of blank requests, DOS attacks, and security threats'
    },
    {
        'file': '/mnt/user-data/outputs/5_service_subscription_log.csv',
        'title': 'Service Subscription Analysis',
        'description': 'Analysis of user service subscriptions'
    }
]

# Generate profiling reports
for idx, config in enumerate(files_config, 1):
    print(f"\n[{idx}/5] Generating report: {config['title']}...")
    
    # Read CSV
    df = pd.read_csv(config['file'])
    
    # Generate profile report
    profile = ProfileReport(
        df,
        title=config['title'],
        dataset={
            "description": config['description'],
            "creator": "Server Log Analysis System",
        },
        explorative=True,
        minimal=False
    )
    
    # Save HTML report
    output_file = f"/mnt/user-data/outputs/profiling_reports/{idx}_profiling_report.html"
    profile.to_file(output_file)
    
    print(f"   ✓ Report saved: {idx}_profiling_report.html")
    print(f"   ✓ Records analyzed: {len(df)}")

print("\n" + "="*70)
print("✓ ALL PROFILING REPORTS GENERATED SUCCESSFULLY!")
print("="*70)
print("\nReports saved in: /mnt/user-data/outputs/profiling_reports/")
print("\n5 HTML files created:")
print("  1. 1_profiling_report.html - User Login Analysis")
print("  2. 2_profiling_report.html - Session Duration Analysis")
print("  3. 3_profiling_report.html - Authentication Attempts Analysis")
print("  4. 4_profiling_report.html - Security Events Analysis")
print("  5. 5_profiling_report.html - Service Subscription Analysis")
