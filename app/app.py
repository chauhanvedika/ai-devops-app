from flask import Flask, Response
import socket
import logging
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# -----------------------------
# 🔹 Setup Logging
# Logs will be stored in app.log
# -----------------------------
logging.basicConfig(
    filename='app.log',                # log file name
    level=logging.INFO,                # log level (INFO, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -----------------------------
# 🔹 Prometheus Metric
# Counts number of incoming requests
# -----------------------------
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')

# -----------------------------
# 🔹 Home Route
# Increments request count + logs access
# -----------------------------
@app.route("/")
def home():
    REQUEST_COUNT.inc()                # increase request counter
    logging.info("Home endpoint hit")  # log request
    return f"Hello from AI DevOps Platform 🚀 - Host: {socket.gethostname()}"

# -----------------------------
# 🔹 Health Check Endpoint
# Used for monitoring system health
# -----------------------------
@app.route("/health")
def health():
    logging.info("Health check called")
    return {"status": "healthy"}, 200

# -----------------------------
# 🔹 Metrics Endpoint
# Prometheus scrapes this endpoint
# -----------------------------
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

# -----------------------------
# 🔹 Failure Simulation Endpoint
# Used to generate errors for AI analysis
# -----------------------------
@app.route("/fail")
def fail():
    REQUEST_COUNT.inc()
    logging.error("Simulated failure triggered!")  # log error
    return "Failure simulated!", 500

# -----------------------------
# 🔹 Run Application
# Accessible from outside (EC2)
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)