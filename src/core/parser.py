import re
from src.exceptions.custom_exceptions import InvalidLogLineError


LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+-\s+-\s+\[(?P<timestamp>[^\]]+)\]\s+"(?P<method>[A-Z]+)\s+(?P<endpoint>\S+)\s+HTTP\/[0-9.]+"\s+(?P<status>\d{3})\s+(?P<size>\d+|-)\s*$'
)


def parse_log_line(line: str) -> dict:
    line = line.strip()

    match = LOG_PATTERN.match(line)
    if not match:
        raise InvalidLogLineError("Could not parse log line", line)

    data = match.groupdict()

    data["status"] = int(data["status"])
    data["size"] = int(data["size"]) if data["size"].isdigit() else 0

    return data
