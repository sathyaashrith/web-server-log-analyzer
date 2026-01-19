from src.core.analyzer import analyze_log_file


def test_analyze_log_file():
    result = analyze_log_file("data/raw_logs/sample.log")
    assert "stats" in result
    assert "status_codes" in result
