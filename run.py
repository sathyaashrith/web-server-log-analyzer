import argparse

from src.core.analyzer import analyze_log_file
from src.services.report_service import save_json, save_status_csv, save_cleaned_logs
from src.services.logging_service import setup_logger


def main():
    parser = argparse.ArgumentParser(
        description="Web Server Log Analyzer - Generate JSON + CSV reports from server logs"
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input log file (example: data/raw_logs/sample.log)"
    )

    parser.add_argument(
        "--report-dir",
        type=str,
        default="data/reports",
        help="Folder to save output reports (default: data/reports)"
    )

    args = parser.parse_args()

    logger = setup_logger()
    logger.info(f"Starting analysis for: {args.input}")

    result = analyze_log_file(args.input, logger=logger)

    # Save reports
    save_json(result["stats"], f"{args.report_dir}/summary_report.json")
    save_json(result["errors"], f"{args.report_dir}/error_report.json")
    save_status_csv(result["status_codes"], f"{args.report_dir}/status_code_report.csv")

    # Full report
    save_json(result, f"{args.report_dir}/full_report.json")

    # Cleaned logs
    save_cleaned_logs(result["cleaned_lines"], "data/processed/cleaned_logs.log")

    logger.info("Analysis completed successfully!")
    logger.info(f"Reports generated inside {args.report_dir}/")
    logger.info("Cleaned logs saved inside data/processed/cleaned_logs.log")


if __name__ == "__main__":
    main()
