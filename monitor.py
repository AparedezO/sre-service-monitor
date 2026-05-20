import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from prometheus_client import Counter, Gauge, start_http_server

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "monitor.log"

load_dotenv(dotenv_path=ENV_FILE, override=True)

URL = os.getenv("URL", "https://httpstat.us/200")
INTERVAL = int(os.getenv("INTERVAL", 10))
MAX_CONSECUTIVE_FAILURES = int(os.getenv("MAX_CONSECUTIVE_FAILURES", 3))
METRICS_PORT = int(os.getenv("METRICS_PORT", 8000))

REQUEST_COUNT = Counter("monitor_requests_total", "Total requests made")
FAILURE_COUNT = Counter("monitor_failures_total", "Total failures")
SERVICE_STATUS = Gauge("service_status", "Service status (1=up, 0=down)")

LOG_DIR.mkdir(exist_ok=True)

consecutive_failures = 0


def write_log(message: str) -> None:
    timestamped = f"[{datetime.now().isoformat()}] {message}"
    print(timestamped)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(timestamped + "\n")



def get_health_status(status: int) -> str:
    if status == 200:
        return "HEALTHY"
    if status >= 500:
        return "DOWN"
    return "DEGRADED"



def check_service() -> None:
    global consecutive_failures

    REQUEST_COUNT.inc()

    try:
        response = requests.get(URL, timeout=5)
        status = response.status_code
        state = get_health_status(status)

        if status == 200:
            consecutive_failures = 0
            SERVICE_STATUS.set(1)
            log_message = f"STATUS={state} CODE={status} URL={URL}"
        else:
            consecutive_failures += 1
            FAILURE_COUNT.inc()
            SERVICE_STATUS.set(0)
            log_message = (
                f"STATUS={state} CODE={status} URL={URL} "
                f"FAILURES={consecutive_failures}"
            )

    except requests.RequestException as error:
        consecutive_failures += 1
        FAILURE_COUNT.inc()
        SERVICE_STATUS.set(0)
        log_message = (
            f"STATUS=DOWN URL={URL} ERROR={error} FAILURES={consecutive_failures}"
        )

    write_log(log_message)

    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        write_log(
            f"ALERT=CRITICAL SERVICE_DOWN failures={consecutive_failures}"
        )



def main() -> None:
    start_http_server(METRICS_PORT)
    write_log(f"METRICS_SERVER=STARTED PORT={METRICS_PORT}")

    while True:
        check_service()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
