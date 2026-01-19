from collections import defaultdict, Counter
from src.core.parser import parse_log_line
from src.exceptions.custom_exceptions import InvalidLogLineError


def analyze_log_file(file_path: str, logger=None):
    stats = defaultdict(int)
    status_counter = Counter()
    endpoint_counter = Counter()
    ip_counter = Counter()

    errors = []
    cleaned_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            raw_line = line.strip()

            if not raw_line:
                continue

            try:
                parsed = parse_log_line(raw_line)

                cleaned_lines.append(raw_line)

                stats["total_requests"] += 1
                stats["total_bytes"] += parsed["size"]

                status_counter[parsed["status"]] += 1
                endpoint_counter[parsed["endpoint"]] += 1
                ip_counter[parsed["ip"]] += 1

                if parsed["status"] >= 500:
                    stats["server_errors"] += 1

            except InvalidLogLineError as e:
                stats["invalid_lines"] += 1
                errors.append({
                    "line_number": line_num,
                    "error": str(e),
                    "line_preview": e.line_content
                })

                if logger:
                    logger.warning(f"Invalid line {line_num}: {e.line_content}")

    return {
        "stats": dict(stats),
        "status_codes": dict(status_counter),
        "top_endpoints": endpoint_counter.most_common(5),
        "top_ips": ip_counter.most_common(5),
        "errors": errors,
        "cleaned_lines": cleaned_lines
    }
