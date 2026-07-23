import re
import time
from pathlib import Path
from datetime import datetime

SYSLOG_PATH = Path("/var/log/syslog")

                                                           
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+)\s+"                       
    r"(?P<hostname>\S+)\s+"                    
    r"(?P<process>[\w\-\.]+)"                      
    r"(?:\[(?P<pid>\d+)\])?:\s+"                     
    r"(?P<message>.*)$"                                       
)

                                                         
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m|#033\[[0-9;]*m")

                                       
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
        f.seek(0, 2)                               
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
            continue                                                   

        if parsed["severity"] in ("ERROR", "CRITICAL", "WARNING"):
            print(f"[{parsed['severity']}] {parsed['process']} — {parsed['message']}")


if __name__ == "__main__":
    main()
