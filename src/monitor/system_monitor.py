import psutil
import time
from datetime import datetime

# Thresholds — adjust these based on what counts as "concerning" for your setup
CPU_THRESHOLD = 85.0      # percent
RAM_THRESHOLD = 85.0      # percent
DISK_THRESHOLD = 90.0     # percent

CHECK_INTERVAL = 5        # seconds between checks


def get_system_stats() -> dict:
    """Collect current CPU, RAM, and disk usage."""
    cpu_percent = psutil.cpu_percent(interval=1)  # measured over 1 second for accuracy
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
    """Return a list of alert messages for any metric exceeding its threshold."""
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
    print("Starting system resource monitor... (Ctrl+C to stop)\n")
    while True:
        stats = get_system_stats()

        print(
            f"[{stats['timestamp']}] "
            f"CPU: {stats['cpu_percent']}% | "
            f"RAM: {stats['ram_percent']}% | "
            f"Disk: {stats['disk_percent']}%"
        )

        alerts = check_thresholds(stats)
        for alert in alerts:
            print(f"  🚨 ALERT: {alert}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
