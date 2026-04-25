from flask import Flask, Response
import socket
import logging
from prometheus_client import Counter, generate_latest
from ai_analyzer import analyze_logs
from flask import jsonify

app = Flask(__name__)   # ✅ Initialize FIRST

# -----------------------------
# 🔹 Setup Logging
# -----------------------------
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -----------------------------
# 🔹 Prometheus Metric
# -----------------------------
REQUEST_COUNT = Counter('http_requests_total', 'Total number of requests')

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
        logging.info("Analyze endpoint called")
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Analyzer failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500   # ✅ return JSON

# -----------------------------
# 🔹 Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)