from flask import Flask, Response, jsonify
import socket
import logging
from prometheus_client import Counter, Gauge, generate_latest
from ai_analyzer import analyze_logs

app = Flask(__name__)

# -----------------------------
# 🔹 Setup Logging
# -----------------------------
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -----------------------------
# 🔹 Prometheus Metrics
# -----------------------------
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of requests'
)

AI_STATUS = Gauge(
    'ai_system_status',
    'AI detected system health (0=healthy,1=warning,2=critical)'
)

# -----------------------------
# 🔹 Home Route
# -----------------------------
@app.route("/")
def home():
    REQUEST_COUNT.inc()
    logging.info("Home endpoint hit")
    return f"Hello from AI DevOps Platform 🚀 - Host: {socket.gethostname()}"

# -----------------------------
# 🔹 Health Check
# -----------------------------
@app.route("/health")
def health():
    logging.info("Health check called")
    return {"status": "healthy"}, 200

# -----------------------------
# 🔹 Metrics
# -----------------------------
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

# -----------------------------
# 🔹 Failure Simulation
# -----------------------------
@app.route("/fail")
def fail():
    REQUEST_COUNT.inc()
    logging.error("Simulated failure triggered!")
    return "Failure simulated!", 500

# -----------------------------
# 🔹 AI Log Analyzer
# -----------------------------
@app.route("/analyze")
def analyze():
    try:
        result = analyze_logs()

        # map status → numeric
        status_map = {
            "healthy": 0,
            "warning": 1,
            "critical": 2
        }

        AI_STATUS.set(status_map.get(result.get("status"), 0))

        logging.info(f"AI Analysis: {result}")

        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Analyzer failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# -----------------------------
# 🔹 Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)