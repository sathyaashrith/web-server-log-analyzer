from datetime import datetime


def parse_timestamp(ts: str):
    """
    Example timestamp: 10/Oct/2023:14:30:01 +0000
    """
    try:
        return datetime.strptime(ts.split()[0], "%d/%b/%Y:%H:%M:%S")
    except Exception:
        return None
