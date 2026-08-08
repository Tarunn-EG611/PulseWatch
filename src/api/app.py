import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.storage.db import get_connection, init_db

app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    limit = request.args.get("limit", default=50, type=int)

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM system_metrics ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.route("/api/errors", methods=["GET"])
def get_errors():
    limit = request.args.get("limit", default=50, type=int)
    severity = request.args.get("severity")

    with get_connection() as conn:
        if severity:
            rows = conn.execute(
                "SELECT * FROM log_events WHERE severity = ? ORDER BY id DESC LIMIT ?",
                (severity.upper(), limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM log_events ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.route("/api/status", methods=["GET"])
def get_status():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT service_name, status, timestamp
            FROM service_status
            WHERE id IN (
                SELECT MAX(id) FROM service_status GROUP BY service_name
            )
            """
        ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    limit = request.args.get("limit", default=20, type=int)

    with get_connection() as conn:
        errors = conn.execute(
            "SELECT * FROM log_events WHERE severity IN ('ERROR', 'CRITICAL') ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()

        down_services = conn.execute(
            "SELECT * FROM service_status WHERE status = 'DOWN' ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()

    return jsonify({
        "log_alerts": [dict(row) for row in errors],
        "service_alerts": [dict(row) for row in down_services],
    })


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
