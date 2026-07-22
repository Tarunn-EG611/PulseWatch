import re
import time
from pathlib import Path
from datetime import datetime

SYSLOG_PATH = Path("/var/log/syslog")

# Regex to break apart each syslog line into its core parts
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+)\s+"        # ISO timestamp
    r"(?P<hostname>\S+)\s+"          # hostname
    r"(?P<process>[\w\-\.]+)"        # process name
    r"(?:\[(?P<pid>\d+)\])?:\s+"     # optional [PID]
    r"(?P<message>.*)$"              # the rest of the message
)

# Strips ANSI color escape codes like \033[36m or \033[0m
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m|#033\[[0-9;]*m")

# Keyword-based severity classification
SEVERITY_RULES = [
    ("CRITICAL", ["panic", "fatal", "critical"]),
    ("ERROR", ["error", "failed", "could not", "denied", "unable to"]),
    ("WARNING", ["warning", "deprecated", "retry"]),
]


def clean_message(message: str) -> str:
    """Remove ANSI color codes from a log message."""
    return ANSI_ESCAPE.sub("", message).strip()


def classify_severity(message: str) -> str:
    """Return a severity level based on keywords found in the message."""
    lower_message = message.lower()
    for level, keywords in SEVERITY_RULES:
        if any(keyword in lower_message for keyword in keywords):
            return level
    return "INFO"


def parse_line(raw_line: str) -> dict | None:
    """Parse a raw syslog line into a structured dictionary."""
    match = LOG_PATTERN.match(raw_line)
    if not match:
        return None

    data = match.groupdict()
    clean_msg = clean_message(data["message"])

    return {
        "timestamp": data["timestamp"],
        "hostname": data["hostname"],
        "process": data["process"],
        "pid": data["pid"],
        "message": clean_msg,
        "severity": classify_severity(clean_msg),
    }


def follow(file_path: Path):
    """Generator that yields new lines appended to a file, like `tail -f`."""
    with open(file_path, "r") as f:
        f.seek(0, 2)  # jump to the end of the file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.rstrip("\n")


def main():
    print(f"Watching {SYSLOG_PATH} for new log entries...\n")
    for raw_line in follow(SYSLOG_PATH):
        parsed = parse_line(raw_line)
        if parsed is None:
            continue  # skip lines that don't match the expected format

        if parsed["severity"] in ("ERROR", "CRITICAL", "WARNING"):
            print(f"[{parsed['severity']}] {parsed['process']} — {parsed['message']}")


if __name__ == "__main__":
    main()
