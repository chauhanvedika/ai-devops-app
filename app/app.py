from flask import Flask, Response
import socket
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Metric: count number of requests
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return f"Hello from AI DevOps Platform 🚀 - Host: {socket.gethostname()}"

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)