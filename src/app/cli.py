import argparse
from src.app.main import run_analysis


def start_cli():
    parser = argparse.ArgumentParser(description="Web Server Log Analyzer CLI")
    parser.add_argument("--input", required=True, help="Path to log file")
    args = parser.parse_args()

    result = run_analysis(args.input)
    print(result)
