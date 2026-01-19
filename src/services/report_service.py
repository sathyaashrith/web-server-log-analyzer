import json
import csv
import os


def save_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_status_csv(status_dict, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["status_code", "count"])

        for status_code, count in sorted(status_dict.items()):
            writer.writerow([status_code, count])


def save_cleaned_logs(cleaned_lines, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        for line in cleaned_lines:
            f.write(line + "\n")
