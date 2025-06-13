# log_receiver.py
from flask import Flask, request

app = Flask(__name__)

@app.route("/log", methods=["POST"])
def receive_log():
    log = request.json.get("log")
    print(f"[수신된 로그]: {log}")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
