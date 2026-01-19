def is_valid_log_line(line: str) -> bool:
    """
    Basic validator: checks if line contains required log markers.
    """
    return '"' in line and "[" in line and "]" in line
