from flask import Flask, request, jsonify
import requests
import sys
import random
from collections import Counter

app = Flask(__name__)

if len(sys.argv) < 5:
    print("Uso: python3 lsp_drone.py <id> <porta> <fault_mode> <fault_rate> [nodes...]")
    sys.exit()

DRONE_ID = sys.argv[1]
PORT = int(sys.argv[2])
FAULT_MODE = sys.argv[3]
FAULT_RATE = float(sys.argv[4])
NODES = sys.argv[5:]

commander_value = None
received_messages = {}
decided_value = None


def is_byzantine():
    return FAULT_MODE == "byzantine" and random.random() < FAULT_RATE


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "drone": DRONE_ID,
        "algorithm": "Lamport-Shostak-Pease",
        "fault_mode": FAULT_MODE,
        "commander_value": commander_value,
        "received_messages": received_messages,
        "decided_value": decided_value,
        "status": "rodando"
    })


@app.route("/lsp_message", methods=["POST"])
def lsp_message():
    global commander_value
    global received_messages

    data = request.json
    sender = data["from"]
    value = data["value"]
    origin = data.get("origin", sender)

    if is_byzantine():
        value = f"leader=fake_{DRONE_ID}"
        print(f"[{DRONE_ID}] BIZANTINO alterou mensagem de {sender} para {value}")

    received_messages[sender] = value

    if origin == "commander":
        commander_value = value

    print(f"[{DRONE_ID}] recebeu de {sender}: {value}")

    return jsonify({
        "status": "received",
        "from": sender,
        "value": value
    })


@app.route("/start_lsp", methods=["GET"])
def start_lsp():
    global commander_value
    global received_messages

    proposal = f"leader={DRONE_ID}"

    commander_value = proposal
    received_messages[DRONE_ID] = proposal

    print(f"[{DRONE_ID}] COMANDANTE propôs: {proposal}")

    for node in NODES:
        try:
            requests.post(
                f"{node}/lsp_message",
                json={
                    "from": DRONE_ID,
                    "origin": "commander",
                    "value": proposal
                },
                timeout=3
            )
        except Exception as e:
            print(f"[{DRONE_ID}] erro enviando proposta para {node}: {e}")

    return jsonify({
        "status": "lsp_started",
        "proposal": proposal
    })


@app.route("/broadcast_lsp", methods=["GET"])
def broadcast_lsp():
    if commander_value is None:
        return jsonify({
            "status": "no_commander_value",
            "message": "Este drone ainda não recebeu valor do comandante"
        })

    value = commander_value

    if is_byzantine():
        value = f"leader=fake_{DRONE_ID}"
        print(f"[{DRONE_ID}] BIZANTINO retransmitiu valor falso: {value}")

    print(f"[{DRONE_ID}] retransmitindo valor do comandante: {value}")

    for node in NODES:
        try:
            requests.post(
                f"{node}/lsp_message",
                json={
                    "from": DRONE_ID,
                    "origin": "relay",
                    "value": value
                },
                timeout=3
            )
        except Exception as e:
            print(f"[{DRONE_ID}] erro no broadcast para {node}: {e}")

    return jsonify({
        "status": "broadcast_done",
        "value": value
    })


@app.route("/decide_lsp", methods=["GET"])
def decide_lsp():
    global decided_value

    if not received_messages:
        return jsonify({
            "status": "no_decision",
            "reason": "nenhum valor recebido"
        })

    votes = Counter(received_messages.values())
    decided_value = votes.most_common(1)[0][0]

    print(f"[{DRONE_ID}] mensagens recebidas: {received_messages}")
    print(f"[{DRONE_ID}] votos: {dict(votes)}")
    print(f"[{DRONE_ID}] DECIDIU: {decided_value}")

    return jsonify({
        "status": "decided",
        "decided_value": decided_value,
        "votes": dict(votes),
        "messages": received_messages
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
