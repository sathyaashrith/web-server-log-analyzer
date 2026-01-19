from src.core.analyzer import analyze_log_file
from src.services.logging_service import setup_logger


def run_analysis(input_file: str):
    logger = setup_logger()
    logger.info(f"Running analysis for {input_file}")

    result = analyze_log_file(input_file, logger=logger)
    return result
