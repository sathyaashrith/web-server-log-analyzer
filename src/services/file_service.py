import os
from src.exceptions.custom_exceptions import FileProcessingError


def validate_file_exists(file_path: str):
    if not os.path.exists(file_path):
        raise FileProcessingError(f"File not found: {file_path}")


def ensure_folder(folder_path: str):
    os.makedirs(folder_path, exist_ok=True)
