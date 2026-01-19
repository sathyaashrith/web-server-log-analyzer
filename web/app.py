import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, flash

from src.core.analyzer import analyze_log_file
from src.services.report_service import save_json, save_status_csv, save_cleaned_logs
from src.services.logging_service import setup_logger

app = Flask(__name__)
app.secret_key = "log-analyzer-secret-key"

logger = setup_logger()

# ✅ Project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "raw_logs")
REPORT_FOLDER = os.path.join(BASE_DIR, "data", "reports")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "data", "processed")
HISTORY_FOLDER = os.path.join(BASE_DIR, "data", "history")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(HISTORY_FOLDER, exist_ok=True)

LATEST_REPORT_PATH = os.path.join(REPORT_FOLDER, "full_report.json")
CLEANED_LOG_PATH = os.path.join(PROCESSED_FOLDER, "cleaned_logs.log")


def list_history():
    """
    Returns list of saved history reports (latest first)
    """
    reports = []
    for fname in os.listdir(HISTORY_FOLDER):
        if fname.endswith(".json"):
            reports.append(fname)

    # Sort newest first
    reports.sort(reverse=True)
    return reports


def load_report(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/", methods=["GET"])
def home():
    history_files = list_history()
    return render_template("index.html", history_files=history_files)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "logfile" not in request.files:
        flash("No file uploaded!")
        return redirect(url_for("home"))

    file = request.files["logfile"]

    if file.filename == "":
        flash("Please select a file!")
        return redirect(url_for("home"))

    # Save uploaded file
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    logger.info(f"Uploaded file saved at: {save_path}")

    # Analyze logs
    result = analyze_log_file(save_path, logger=logger)

    # Save reports in standard output location
    save_json(result["stats"], os.path.join(REPORT_FOLDER, "summary_report.json"))
    save_json(result["errors"], os.path.join(REPORT_FOLDER, "error_report.json"))
    save_status_csv(result["status_codes"], os.path.join(REPORT_FOLDER, "status_code_report.csv"))
    save_json(result, os.path.join(REPORT_FOLDER, "full_report.json"))

    # Save cleaned logs
    save_cleaned_logs(result["cleaned_lines"], CLEANED_LOG_PATH)

    # ✅ Save history report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_name = f"report_{timestamp}_{file.filename.replace(' ', '_')}.json"
    history_path = os.path.join(HISTORY_FOLDER, history_name)
    save_json(result, history_path)

    flash("Analysis completed successfully!")
    return redirect(url_for("dashboard", filter_type="all"))


@app.route("/dashboard/<filter_type>", methods=["GET"])
def dashboard(filter_type):
    if not os.path.exists(LATEST_REPORT_PATH):
        flash("No analysis report found. Upload a log file first.")
        return redirect(url_for("home"))

    report = load_report(LATEST_REPORT_PATH)

    # ---------- Error Filters ----------
    # NOTE: Your report["errors"] contains invalid lines.
    # 4xx/5xx filters will use status_codes instead (not invalid errors list).
    errors = report.get("errors", [])

    if filter_type == "invalid":
        filtered_errors = errors
    elif filter_type == "all":
        filtered_errors = errors
    else:
        # For 4xx and 5xx, show message (since invalid errors are not status based)
        filtered_errors = errors

    report["filtered_errors"] = filtered_errors
    report["filter_type"] = filter_type

    # ---------- Cleaned Logs Preview ----------
    cleaned_preview = []
    if os.path.exists(CLEANED_LOG_PATH):
        with open(CLEANED_LOG_PATH, "r", encoding="utf-8") as f:
            cleaned_preview = f.readlines()[:50]  # first 50 lines only

    report["cleaned_preview"] = cleaned_preview

    return render_template("dashboard.html", report=report)


@app.route("/history", methods=["GET"])
def history():
    history_files = list_history()
    return render_template("history.html", history_files=history_files)


@app.route("/history/view/<filename>", methods=["GET"])
def view_history(filename):
    history_path = os.path.join(HISTORY_FOLDER, filename)

    if not os.path.exists(history_path):
        flash("History report not found!")
        return redirect(url_for("history"))

    report = load_report(history_path)

    # Add cleaned preview (history does not store cleaned file separately)
    report["cleaned_preview"] = report.get("cleaned_lines", [])[:50]
    report["filtered_errors"] = report.get("errors", [])
    report["filter_type"] = "history"

    return render_template("dashboard.html", report=report)


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_map = {
        "summary_report.json": os.path.join(REPORT_FOLDER, "summary_report.json"),
        "error_report.json": os.path.join(REPORT_FOLDER, "error_report.json"),
        "status_code_report.csv": os.path.join(REPORT_FOLDER, "status_code_report.csv"),
        "full_report.json": os.path.join(REPORT_FOLDER, "full_report.json"),
        "cleaned_logs.log": os.path.join(PROCESSED_FOLDER, "cleaned_logs.log"),
    }

    if filename not in file_map:
        flash("Invalid file requested!")
        return redirect(url_for("dashboard", filter_type="all"))

    path = file_map[filename]

    if not os.path.exists(path):
        flash(f"File not found: {filename}")
        return redirect(url_for("dashboard", filter_type="all"))

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
