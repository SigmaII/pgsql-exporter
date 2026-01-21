from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.get("/metrics")
def metrics():
    with open("output.json") as f:
        data = json.load(f)
    return jsonify(data)
def start_http():
    app.run(host="0.0.0.0", port=8080)