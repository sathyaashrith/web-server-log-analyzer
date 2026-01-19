# Web Server Log Analyzer

## Overview
This project analyzes web server log files and generates reports.

## Features
- Line-by-line processing (memory efficient)
- Handles malformed log lines safely
- Generates JSON + CSV reports
- Saves cleaned valid logs

## Run
```powershell
python run.py --input data/raw_logs/sample.log
