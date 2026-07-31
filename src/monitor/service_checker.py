
import psutil
import time
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.storage.db import init_db, insert_service_status
from src.alerts.slack_alert import send_alert_with_cooldown

WATCHED_SERVICES = [
    "systemd",
    "cron",
    "dbus-daemon",
]

CHECK_INTERVAL = 5


def is_process_running(name: str) -> bool:
    for proc in psutil.process_iter(["name"]):
        try:
            if name.lower() in proc.info["name"].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def check_services(service_list: list[str]) -> dict:
    return {service: is_process_running(service) for service in service_list}


def main():
    init_db()
    print("Starting service health checker... (Ctrl+C to stop)\n")
    previous_state = {service: True for service in WATCHED_SERVICES}

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_state = check_services(WATCHED_SERVICES)

        for service, is_running in current_state.items():
            status = "UP" if is_running else "DOWN"
            print(f"[{timestamp}] {service}: {status}")

            insert_service_status(timestamp, service, status)

            if is_running != previous_state[service]:
                if not is_running:
                    print(f"  🚨 ALERT: {service} has STOPPED!")
                    send_alert_with_cooldown(
                        f"service_down_{service}",
                        f"Service *{service}* has STOPPED at {timestamp}!"
                    )
                else:
                    print(f"  ✅ RECOVERED: {service} is back UP.")
                    send_alert_with_cooldown(
                        f"service_up_{service}",
                        f"Service *{service}* has RECOVERED at {timestamp}."
                    )

        previous_state = current_state
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
