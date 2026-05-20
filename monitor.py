import os
import time
from datetime import datetime

import requests

URL = os.getenv("URL", "https://httpstat.us/500")
INTERVAL = int(os.getenv("INTERVAL", 10))
LOG_FILE = "logs/monitor.log"
MAX_CONSECUTIVE_FAILURES = 3

consecutive_failures = 0


def write_log(message: str) -> None:
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(message + "\n")


def check_service() -> None:
    global consecutive_failures

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.get(URL, timeout=5)
        status = response.status_code

        if status == 200:
            consecutive_failures = 0
            print("SERVICE HEALTHY")
            log_message = f"[{timestamp}] STATUS=OK CODE={status} URL={URL}"
        else:
            consecutive_failures += 1
            print("SERVICE DEGRADED")
            log_message = (
                f"[{timestamp}] STATUS=ERROR CODE={status} URL={URL} "
                f"CONSECUTIVE_FAILURES={consecutive_failures}"
            )

    except requests.RequestException as error:
        consecutive_failures += 1
        print("SERVICE DEGRADED")
        log_message = (
            f"[{timestamp}] STATUS=FAIL URL={URL} ERROR={error} "
            f"CONSECUTIVE_FAILURES={consecutive_failures}"
        )

    write_log(log_message)

    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        alert_message = (
            f"[{timestamp}] ALERT Service has failed {consecutive_failures} times in a row"
        )
        write_log(alert_message)


def main() -> None:
    while True:
        check_service()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
