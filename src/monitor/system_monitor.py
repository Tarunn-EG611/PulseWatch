import psutil
import time
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.storage.db import init_db, insert_system_metrics
from src.alerts.slack_alert import send_alert_with_cooldown

CPU_THRESHOLD = 85.0
RAM_THRESHOLD = 85.0
DISK_THRESHOLD = 90.0

CHECK_INTERVAL = 5


def get_system_stats() -> dict:
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": cpu_percent,
        "ram_percent": ram.percent,
        "ram_used_gb": round(ram.used / (1024 ** 3), 2),
        "ram_total_gb": round(ram.total / (1024 ** 3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
    }


def check_thresholds(stats: dict) -> list[str]:
    alerts = []

    if stats["cpu_percent"] > CPU_THRESHOLD:
        alerts.append(f"HIGH CPU USAGE: {stats['cpu_percent']}% (threshold: {CPU_THRESHOLD}%)")

    if stats["ram_percent"] > RAM_THRESHOLD:
        alerts.append(
            f"HIGH RAM USAGE: {stats['ram_percent']}% "
            f"({stats['ram_used_gb']}GB / {stats['ram_total_gb']}GB) "
            f"(threshold: {RAM_THRESHOLD}%)"
        )

    if stats["disk_percent"] > DISK_THRESHOLD:
        alerts.append(
            f"HIGH DISK USAGE: {stats['disk_percent']}% "
            f"({stats['disk_used_gb']}GB / {stats['disk_total_gb']}GB) "
            f"(threshold: {DISK_THRESHOLD}%)"
        )

    return alerts


def main():
    init_db()
    print("Starting system resource monitor... (Ctrl+C to stop)\n")
    while True:
        stats = get_system_stats()

        print(
            f"[{stats['timestamp']}] "
            f"CPU: {stats['cpu_percent']}% | "
            f"RAM: {stats['ram_percent']}% | "
            f"Disk: {stats['disk_percent']}%"
        )

        insert_system_metrics(
            stats["timestamp"],
            stats["cpu_percent"],
            stats["ram_percent"],
            stats["ram_used_gb"],
            stats["disk_percent"],
            stats["disk_used_gb"],
        )

        alerts = check_thresholds(stats)
        for alert in alerts:
            print(f"  🚨 ALERT: {alert}")
            send_alert_with_cooldown(alert[:30], alert)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
