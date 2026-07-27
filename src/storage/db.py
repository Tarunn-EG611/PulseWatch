import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "pulsewatch.db"


@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                hostname TEXT,
                process TEXT,
                pid TEXT,
                message TEXT,
                severity TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL,
                ram_percent REAL,
                ram_used_gb REAL,
                disk_percent REAL,
                disk_used_gb REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                service_name TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

    print(f"Database initialized at: {DB_PATH}")


def insert_log_event(timestamp, hostname, process, pid, message, severity):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO log_events (timestamp, hostname, process, pid, message, severity)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (timestamp, hostname, process, pid, message, severity),
        )


def insert_system_metrics(timestamp, cpu_percent, ram_percent, ram_used_gb, disk_percent, disk_used_gb):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO system_metrics (timestamp, cpu_percent, ram_percent, ram_used_gb, disk_percent, disk_used_gb)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (timestamp, cpu_percent, ram_percent, ram_used_gb, disk_percent, disk_used_gb),
        )


def insert_service_status(timestamp, service_name, status):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO service_status (timestamp, service_name, status)
               VALUES (?, ?, ?)""",
            (timestamp, service_name, status),
        )


if __name__ == "__main__":
    init_db()
