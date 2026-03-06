from flask import Flask, request, jsonify
import asyncio
from database.crud import Database

app = Flask(__name__)
db = Database()
asyncio.run(db.connect())


@app.route("/get_version", methods=["GET"])
def get_version():
    return jsonify({"version": "0.0.1"})


@app.route("/check_by_key", methods=["POST"])
def check_by_key():
    data = request.json
    key = data.get("key")
    if not key:
        return jsonify({"status": False, "error": "No key provided"})
    license_data = asyncio.run(db.get_license(key))
    if license_data and license_data["is_active"]:
        return jsonify({"status": True})
    return jsonify({"status": False})


@app.route("/bind_by_hardware", methods=["POST"])
def bind_by_hardware():
    data = request.json
    key = data.get("key")
    pc_id = data.get("pc_id")
    uuid_system = data.get("uuid_system")
    license_data = asyncio.run(db.get_license(key))
    if not license_data or not license_data["is_active"]:
        return jsonify({"status": False})
    current_hardware = license_data.get("hardware_id")
    hardware_id = f"{pc_id}_{uuid_system}"
    if current_hardware and current_hardware != hardware_id:
        return jsonify({"status": False})
    if not current_hardware:
        asyncio.run(db.bind_hardware(key, hardware_id))
    return jsonify({"status": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
