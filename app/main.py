import logging
import time
from flask import Flask, jsonify, request

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)
START_TIME = time.time()
REQUEST_COUNT = 0

@app.before_request
def count_requests():
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    logging.info(f"Incoming request: {request.method} {request.path}")

@app.route("/")
def home():
    return jsonify({"status": "success", "message": "Welcome to the End-to-End DevOps Mini Project!", "version": "1.1.0"}), 200

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "uptime_seconds": int(time.time() - START_TIME), "total_requests": REQUEST_COUNT}), 200

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json() or {}
    a, b, operation = data.get("a"), data.get("b"), data.get("operation", "add")

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return jsonify({"error": "Fields 'a' and 'b' must be numbers"}), 400

    if operation == "add": result = a + b
    elif operation == "subtract": result = a - b
    elif operation == "multiply": result = a * b
    elif operation == "divide":
        if b == 0: return jsonify({"error": "Division by zero"}), 400
        result = a / b
    else: return jsonify({"error": f"Unsupported operation: {operation}"}), 400

    return jsonify({"operation": operation, "a": a, "b": b, "result": result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
