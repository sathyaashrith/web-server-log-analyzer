
# 📊 Web Server Log Analyzer 

A professional **Web Server Log Analyzer** built using **Python** that can analyze large server log files efficiently, handle corrupted/malformed logs safely, generate reports, and display results in a **Flask-based interactive dashboard with charts**.

This project demonstrates real-world concepts like:
- File Operations (large file handling)
- Exception Handling
- Context Managers
- Logging & Debugging
- Report Generation (JSON + CSV)
- Web Dashboard using Flask + Chart.js

---

## 🚀 Project Highlights

### ✅ Core Features
- Reads huge log files **line-by-line** (memory efficient)
- Extracts log details:
  - IP Address
  - Timestamp
  - HTTP Method
  - Endpoint
  - Status Code
  - Response Size
- Calculates:
  - Total Requests
  - Total Bytes
  - Status Code Counts
  - Top Endpoints
  - Top IPs
  - Server Errors (>= 500)
- Handles corrupted/malformed logs safely (no crash)

### 🛡️ Error Handling
- Custom exception: `InvalidLogLineError`
- Invalid lines are stored in JSON report with:
  - line number
  - error message
  - preview of invalid line

### 📁 Reports Generated
- `summary_report.json` → overall stats
- `error_report.json` → invalid lines report
- `status_code_report.csv` → status code frequency
- `full_report.json` → everything combined in one file
- `cleaned_logs.log` → only valid log lines

### 🌐 Flask Website Dashboard
- Upload `.log` file from browser
- Visual dashboard with:
  - Summary cards
  - Status code charts (Bar + Pie)
  - Top endpoints chart
  - Top IPs chart
  - Errors table
  - Cleaned logs preview
- Download reports directly
- Upload history (stores old reports)

---

## 🧠 Problem Statement

A startup’s web server generates massive log files (GBs). They need to analyze them but:
- Files are huge → cannot load into memory
- Some logs are corrupted → analysis should not crash
- Need accurate statistics and reports
- Need visualization/dashboard for monitoring

This project solves all these problems.

---
## 📊 OUTPUT
<img width="1919" height="945" alt="Screenshot 2026-01-19 151110" src="https://github.com/user-attachments/assets/b2eb2f95-d6fd-4896-9453-0c6720262c3b" />
<img width="1910" height="837" alt="Screenshot 2026-01-19 151012" src="https://github.com/user-attachments/assets/6190e139-86df-4773-894f-a07675cc32f4" />
<img width="1919" height="823" alt="Screenshot 2026-01-19 151023" src="https://github.com/user-attachments/assets/b845839f-6c9d-486f-bc6f-32f917f21669" />
<img width="1919" height="935" alt="Screenshot 2026-01-19 151053" src="https://github.com/user-attachments/assets/f83552ee-3c16-430e-90d3-b02eb04363ce" />

