from src.core.parser import parse_log_line


def test_parse_log_line():
    line = '127.0.0.1 - - [10/Oct/2023:14:30:01 +0000] "GET /home HTTP/1.1" 200 1234'
    data = parse_log_line(line)
    assert data["ip"] == "127.0.0.1"
    assert data["status"] == 200
    assert data["size"] == 1234
