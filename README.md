# Service Monitor SRE

This project monitors a web service by sending periodic HTTP requests and logging the results.

## Features
- Checks if a URL is reachable
- Logs results with timestamps
- Detects consecutive failures
- Runs continuously every few seconds

## Tech
- Python
- Requests

## Usage
1. Activate the virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the monitor:
   `python monitor.py`

## Environment variables
`URL=https://example.com`
`INTERVAL=5`

## What this simulates
- Health checks
- Monitoring system behavior
- Basic alerting system

## SRE concepts applied
- Observability
- Logging
- Incident detection
- Failure thresholds
