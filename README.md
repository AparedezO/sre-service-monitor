# Service Monitor SRE

A Python-based SRE monitoring project that performs periodic health checks against a target URL, writes structured logs, tracks consecutive failures, triggers critical alerts, and exposes Prometheus metrics for observability.

## Overview

This project simulates a lightweight production-style monitoring workflow:

- Sends periodic HTTP requests to a monitored service
- Classifies service health as `HEALTHY`, `DEGRADED`, or `DOWN`
- Writes ISO 8601 timestamped logs
- Detects repeated failures and raises critical alerts
- Exposes Prometheus-compatible metrics on `/metrics`
- Loads runtime configuration from environment variables
- Can run locally or inside Docker

## Features

- Continuous URL monitoring
- Structured timestamped logging
- Consecutive failure tracking
- Critical alert thresholds
- Environment-based configuration
- Prometheus metrics endpoint
- Docker-ready deployment

## Tech Stack

- Python
- `requests`
- `python-dotenv`
- `prometheus_client`
- Docker

## Project Structure

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

## Configuration

Create your local environment file from the example:

```bash
copy .env.example .env
```

Example `.env` values:

```env
URL=https://httpstat.us/500
INTERVAL=10
MAX_CONSECUTIVE_FAILURES=3
METRICS_PORT=8000
```

### Environment Variables

- `URL`: target endpoint to monitor
- `INTERVAL`: number of seconds between checks
- `MAX_CONSECUTIVE_FAILURES`: alert threshold
- `METRICS_PORT`: port used to expose Prometheus metrics

## Installation

```bash
pip install -r requirements.txt
```

## Local Usage

Run the monitor:

```bash
python monitor.py
```

Once started, the script will:

- monitor the configured endpoint continuously
- write logs to `logs/monitor.log`
- expose metrics at `http://localhost:8000/metrics`

## Docker Usage

Build the image:

```bash
docker build -t sre-service-monitor .
```

Run the container:

```bash
docker run --rm -p 8000:8000 --env-file .env --name sre-monitor sre-service-monitor
```

This will:

- start the monitor inside a container
- expose Prometheus metrics on port `8000`
- load runtime configuration from `.env`

## Example Log Output

```text
[2026-05-20T14:00:00.000000] STATUS=HEALTHY CODE=200 URL=https://httpstat.us/200
[2026-05-20T14:00:10.000000] STATUS=DOWN CODE=500 URL=https://httpstat.us/500 FAILURES=1
[2026-05-20T14:00:30.000000] ALERT=CRITICAL SERVICE_DOWN failures=3
```

## Prometheus Metrics

The monitor exposes these custom metrics:

- `monitor_requests_total`: total number of checks executed
- `monitor_failures_total`: total number of failed checks
- `service_status`: current service state where `1=up` and `0=down`

Metrics are available at:

```text
http://localhost:8000/metrics
```

## Health Model

The monitor classifies responses using a simple service health model:

- `HEALTHY`: HTTP `200`
- `DEGRADED`: non-200 responses below `500`
- `DOWN`: HTTP `500+` or request exceptions

## SRE Concepts Implemented

- Health checks
- Observability through logs and metrics
- Failure detection
- Consecutive failure thresholds
- Critical alerting
- Environment-based configuration
- Basic service state modeling
- Containerized execution

## Why This Project Matters

This project demonstrates practical foundations expected in a junior SRE portfolio:

- monitoring and health validation
- operational logging
- failure handling
- alert threshold logic
- metrics exposure for Prometheus scraping
- portable deployment with Docker

## Future Improvements

- JSON structured logging
- Slack or email alert integration
- Docker Compose setup
- Prometheus scrape configuration
- Grafana dashboard visualization
