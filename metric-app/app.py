import os
import random
import threading
import time

from flask import Flask, jsonify, request
from prometheus_client import Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)

TRAFFIC_BYTES = Counter(
    "network_traffic_bytes_total",
    "Total simulated network traffic in bytes.",
    ["direction", "protocol"],
)
PACKETS = Counter(
    "network_packets_total",
    "Total simulated network packets.",
    ["direction", "protocol"],
)
PACKET_LOSS = Gauge(
    "network_packet_loss_percent",
    "Current simulated packet loss percentage.",
)
LATENCY = Gauge(
    "network_latency_ms",
    "Current simulated network latency in milliseconds.",
)
ACTIVE_CONNECTIONS = Gauge(
    "network_active_connections",
    "Current simulated active network connections.",
)
BANDWIDTH = Gauge(
    "network_bandwidth_mbps",
    "Current simulated bandwidth usage in Mbps.",
)
REQUEST_LATENCY = Histogram(
    "network_monitor_request_duration_seconds",
    "Metric app request duration in seconds.",
    ["endpoint"],
)
ALERT_SCENARIO = Gauge(
    "network_alert_scenario_enabled",
    "1 when the high-traffic alert demo scenario is enabled.",
)

state = {
    "scenario": "normal",
    "latency_ms": 24.0,
    "packet_loss_percent": 0.2,
    "active_connections": 40,
    "bandwidth_mbps": 35.0,
}


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def simulate_network():
    protocols = ["tcp", "udp", "icmp"]
    while True:
        scenario = state["scenario"]

        if scenario == "alert":
            latency = random.uniform(160, 260)
            packet_loss = random.uniform(6.0, 13.0)
            active_connections = random.randint(650, 1100)
            bandwidth = random.uniform(850, 1250)
            byte_multiplier = random.randint(600_000, 1_400_000)
        elif scenario == "degraded":
            latency = random.uniform(80, 150)
            packet_loss = random.uniform(2.0, 5.0)
            active_connections = random.randint(220, 520)
            bandwidth = random.uniform(250, 650)
            byte_multiplier = random.randint(250_000, 650_000)
        else:
            latency = random.uniform(15, 55)
            packet_loss = random.uniform(0.0, 1.2)
            active_connections = random.randint(20, 180)
            bandwidth = random.uniform(20, 180)
            byte_multiplier = random.randint(40_000, 230_000)

        protocol = random.choice(protocols)
        inbound_packets = random.randint(120, 850)
        outbound_packets = random.randint(80, 650)

        PACKETS.labels(direction="inbound", protocol=protocol).inc(inbound_packets)
        PACKETS.labels(direction="outbound", protocol=protocol).inc(outbound_packets)
        TRAFFIC_BYTES.labels(direction="inbound", protocol=protocol).inc(byte_multiplier)
        TRAFFIC_BYTES.labels(direction="outbound", protocol=protocol).inc(int(byte_multiplier * random.uniform(0.45, 0.9)))

        state["latency_ms"] = round(clamp(latency, 0, 500), 2)
        state["packet_loss_percent"] = round(clamp(packet_loss, 0, 100), 2)
        state["active_connections"] = active_connections
        state["bandwidth_mbps"] = round(bandwidth, 2)

        LATENCY.set(state["latency_ms"])
        PACKET_LOSS.set(state["packet_loss_percent"])
        ACTIVE_CONNECTIONS.set(state["active_connections"])
        BANDWIDTH.set(state["bandwidth_mbps"])
        ALERT_SCENARIO.set(1 if scenario == "alert" else 0)

        time.sleep(2)


@app.before_request
def start_timer():
    request._start_time = time.time()


@app.after_request
def record_latency(response):
    endpoint = request.path
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - request._start_time)
    return response


@app.get("/")
def home():
    return jsonify(
        {
            "service": "cloud-native-network-monitoring metric app",
            "metrics": "/metrics",
            "scenario": state["scenario"],
            "scenario_control": "POST /scenario with JSON {\"mode\":\"normal|degraded|alert\"}",
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/status")
def status():
    return jsonify(state)


@app.post("/scenario")
def scenario():
    payload = request.get_json(silent=True) or {}
    mode = payload.get("mode", "normal").lower()
    if mode not in {"normal", "degraded", "alert"}:
        return jsonify({"error": "mode must be normal, degraded, or alert"}), 400

    state["scenario"] = mode
    return jsonify({"message": f"scenario changed to {mode}", "state": state})


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; version=0.0.4"}


if __name__ == "__main__":
    threading.Thread(target=simulate_network, daemon=True).start()
    port = int(os.getenv("APP_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
