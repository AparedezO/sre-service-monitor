# ?? Service Monitor SRE

> Lightweight SRE-style service monitoring in Python with health checks, alerting, Prometheus metrics, and Docker support.

## ?? Overview

This project simulates a practical monitoring workflow used in real SRE environments.
It periodically checks a target service, classifies its health, records logs, detects repeated failures, raises alerts, and exposes Prometheus-compatible metrics.

## ? Key Features

- HTTP health checks against a configurable target URL
- Health classification: `HEALTHY`, `DEGRADED`, `DOWN`
- Structured logs with ISO 8601 timestamps
- Consecutive failure tracking and critical alerting
- Prometheus metrics exposed at `/metrics`
- Environment-based configuration with `.env`
- Docker-ready runtime

## ??? Architecture

```text
Monitor Loop
    |
    +-- Send HTTP request
    +-- Evaluate response code
    +-- Classify service state
    +-- Update counters and gauge
    +-- Write structured log
    +-- Trigger alert if threshold is reached
    +-- Sleep for INTERVAL seconds
```

## ??? Tech Stack

- `Python`
- `requests`
- `python-dotenv`
- `prometheus_client`
- `Docker`

## ?? Project Structure

```text
sre-service-monitor/
+-- monitor.py
+-- requirements.txt
+-- Dockerfile
+-- .dockerignore
+-- .gitignore
+-- .env.example
+-- README.md
+-- logs/
    +-- monitor.log
```

## ?? Configuration

Create a local configuration file from the example:

```bash
copy .env.example .env
```

Example `.env`:

```env
URL=https://httpstat.us/500
INTERVAL=10
MAX_CONSECUTIVE_FAILURES=3
METRICS_PORT=8000
```

### ?? Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `URL` | Target endpoint to monitor | `https://httpstat.us/500` |
| `INTERVAL` | Seconds between checks | `10` |
| `MAX_CONSECUTIVE_FAILURES` | Alert threshold | `3` |
| `METRICS_PORT` | Port for Prometheus metrics | `8000` |

## ?? Local Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the monitor:

```bash
python monitor.py
```

## ?? Docker Setup

Build the image:

```bash
docker build -t sre-service-monitor .
```

Run the container:

```bash
docker run --rm -p 8000:8000 --env-file .env --name sre-monitor sre-service-monitor
```

## ?? Metrics Endpoint

Once the monitor is running, Prometheus-style metrics are available at:

```text
http://localhost:8000/metrics
```

### ?? Exported Metrics

- `monitor_requests_total`: total number of checks executed
- `monitor_failures_total`: total number of failed checks
- `service_status`: service state gauge where `1=up` and `0=down`

## ?? Health Model

| HTTP Result | Health State |
|-------------|--------------|
| `200` | `HEALTHY` |
| `4xx` or non-200 below `500` | `DEGRADED` |
| `5xx` or request exception | `DOWN` |

## ?? Example Log Output

```text
[2026-05-20T14:00:00.000000] STATUS=HEALTHY CODE=200 URL=https://httpstat.us/200
[2026-05-20T14:00:10.000000] STATUS=DOWN CODE=500 URL=https://httpstat.us/500 FAILURES=1
[2026-05-20T14:00:30.000000] ALERT=CRITICAL SERVICE_DOWN failures=3
```

## ?? SRE Concepts Implemented

- Health checks
- Observability through logs and metrics
- Failure detection
- Alert thresholds
- Environment-based configuration
- Service state modeling
- Containerized execution

## ?? Why This Project Matters

This project is a strong junior SRE portfolio example because it demonstrates:

- practical monitoring logic
- operational observability
- alert-driven thinking
- metrics exposure for Prometheus scraping
- portable deployment using Docker

## ??? Roadmap

- JSON structured logging
- Alert integrations such as Slack or email
- Docker Compose support
- Prometheus scrape configuration
- Grafana dashboards

## ?? Visual Summary

- `HEALTHY`: service responds with `200`
- `DEGRADED`: service responds but not with `200`
- `DOWN`: service fails or returns `5xx`
- `ALERT=CRITICAL`: repeated failure threshold reached
- `/metrics`: ready for Prometheus scraping

## ?? Repository Notes

- Use `.env.example` as the starting point for local configuration.
- Keep `.env` and generated logs out of version control.
- The monitor is designed to be simple, readable, and interview-friendly.
