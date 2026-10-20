from flask import Flask, jsonify

app = Flask(__name__)

VERSION = "v2"

@app.route("/")
def home():
    return f"<h1>Task Tracker {VERSION}</h1><p>Deployed via Jenkins + Kubernetes</p>"

@app.route("/health")
def health():
    return jsonify(status="ok", version=VERSION)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
