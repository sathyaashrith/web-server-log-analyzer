class LogAnalyzerError(Exception):
    """Base exception for the Log Analyzer project."""
    pass


class InvalidLogLineError(LogAnalyzerError):
    """Raised when a log line cannot be parsed properly."""
    def __init__(self, message="Invalid log line format", line_content=""):
        super().__init__(message)
        self.line_content = line_content


class FileProcessingError(LogAnalyzerError):
    """Raised when file cannot be read/processed."""
    pass
