# 🖥️ Server Log Analysis - Streamlit Application

This project provides comprehensive analysis of server logs using **Pandas Profiling** and **Streamlit**.

## 📋 Features

### 5 Analysis Modules:

1. **User Login Analysis** - Tracks login attempts, success rates, and authentication methods
2. **Session Duration Analysis** - Monitors user session times and server access patterns  
3. **Authentication Attempts** - Identifies authentic vs unauthentic access attempts
4. **Security Events** - Detects blank requests, DOS attacks, and security threats
5. **Service Subscriptions** - Analyzes user service subscriptions and revenue

Each module includes:
- ✅ Interactive visualizations (Plotly charts)
- ✅ Key performance metrics
- ✅ Detailed Pandas Profiling HTML reports
- ✅ Data exploration tools

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📊 Generate Standalone HTML Profiling Reports

If you want to generate all 5 profiling reports as separate HTML files:

```bash
python generate_profiling_reports.py
```

This creates:
- `1_profiling_report.html` - User Login Analysis
- `2_profiling_report.html` - Session Duration Analysis  
- `3_profiling_report.html` - Authentication Attempts Analysis
- `4_profiling_report.html` - Security Events Analysis
- `5_profiling_report.html` - Service Subscription Analysis

Reports are saved in: `profiling_reports/` directory

---

## 📁 Project Structure

```
.
├── streamlit_app.py                    # Main Streamlit application
├── generate_profiling_reports.py       # Script to generate HTML reports
├── generate_logs.py                    # Script that generated the CSV files
├── requirements.txt                    # Python dependencies
├── 1_user_login_log.csv               # User login data
├── 2_session_duration_log.csv         # Session duration data
├── 3_authentication_attempts_log.csv  # Authentication attempts data
├── 4_security_events_log.csv          # Security events data
└── 5_service_subscription_log.csv     # Service subscription data
```

---

## 💡 Usage Tips

### In the Streamlit App:
1. Use the **sidebar** to navigate between different analyses
2. Click **"Generate Full Profiling Report"** button in any section to see comprehensive Pandas Profiling analysis
3. Hover over charts for interactive data exploration
4. Each section shows key metrics at the top

### Pandas Profiling Reports Include:
- Overview statistics
- Variable analysis (distributions, missing values)
- Correlations between variables
- Missing values analysis
- Sample data preview
- And much more!

---

## 🔧 Troubleshooting

**Issue**: "No module named 'streamlit'"
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Profiling report takes too long to generate
- **Solution**: This is normal for large datasets. Wait for completion or use the pre-generated HTML files.

**Issue**: Cannot access CSV files
- **Solution**: Ensure all CSV files are in the same directory as `streamlit_app.py`

---

## 📈 Key Insights You'll Get

### 1. User Login Analysis
- Total login attempts and success rates
- Most used authentication methods
- Device and browser statistics
- Failed login patterns

### 2. Session Duration Analysis  
- Average session duration
- Data transfer patterns
- Session completion rates
- User engagement metrics

### 3. Authentication Attempts
- **Number of unauthentic users trying to access**
- Suspicious IP addresses
- Common failure reasons
- Geographic attack patterns

### 4. Security Events
- **Number of blank requests**
- **Number of DOS attacks**
- Attack severity distribution
- Blocked vs allowed events
- Requests per second during attacks

### 5. Service Subscriptions
- **Which services users subscribe to**
- Revenue analysis by service type
- Subscription status breakdown
- Auto-renewal rates

---

## 🎯 Data Summary

Each CSV file contains **500 rows** with synthetic data:

| File | Records | Key Columns |
|------|---------|-------------|
| User Login | 500 | timestamp, user_id, ip_address, login_status, login_method |
| Session Duration | 500 | session_id, user_id, duration_minutes, pages_accessed |
| Auth Attempts | 500 | timestamp, attempted_username, auth_result, failure_reason |
| Security Events | 500 | timestamp, event_type, requests_per_second, blocked, severity |
| Subscriptions | 500 | subscription_id, user_id, service_type, service_name, monthly_fee |

---

## 🛠️ Requirements

- Python 3.8+
- streamlit
- pandas
- ydata-profiling (formerly pandas-profiling)
- plotly
- streamlit-pandas-profiling

---

## 📞 Support

For issues or questions:
1. Check the CSV files are in the correct location
2. Ensure all dependencies are installed
3. Try regenerating the log files with `generate_logs.py`

---

## 🎉 Enjoy Analyzing Your Server Logs!
