from flask import Flask, request, jsonify
import requests
import sys
import random

app = Flask(__name__)

if len(sys.argv) < 5:
    print("Uso: python3 bft_drone.py <id> <porta> <fault_mode> <fault_rate> [nodes...]")
    exit()

DRONE_ID = sys.argv[1]
PORT = int(sys.argv[2])
FAULT_MODE = sys.argv[3]
FAULT_RATE = float(sys.argv[4])
NODES = sys.argv[5:]

prepare_votes = {}
commit_votes = {}
decided_value = None


def is_byzantine():
    return FAULT_MODE == "byzantine" and random.random() < FAULT_RATE


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "drone": DRONE_ID,
        "status": "rodando",
        "fault_mode": FAULT_MODE,
        "decided_value": decided_value
    })


@app.route("/propose", methods=["POST"])
def propose():
    data = request.json
    value = data["value"]
    sender = data["from"]

    print(f"[{DRONE_ID}] recebeu PROPOSE de {sender}: {value}")

    if is_byzantine():
        fake_value = f"leader=fake_{DRONE_ID}"
        print(f"[{DRONE_ID}] BIZANTINO alterou proposta para {fake_value}")
        value = fake_value

    return jsonify({
        "type": "prepare",
        "from": DRONE_ID,
        "value": value
    })


@app.route("/prepare", methods=["POST"])
def prepare():
    global prepare_votes

    data = request.json
    value = data["value"]
    sender = data["from"]

    if value not in prepare_votes:
        prepare_votes[value] = set()

    prepare_votes[value].add(sender)

    print(f"[{DRONE_ID}] recebeu PREPARE de {sender}: {value}")

    total_nodes = len(NODES) + 1
    quorum = (2 * total_nodes) // 3 + 1

    if len(prepare_votes[value]) >= quorum:
        print(f"[{DRONE_ID}] QUORUM PREPARE atingido para {value}")

        return jsonify({
            "type": "commit",
            "from": DRONE_ID,
            "value": value
        })

    return jsonify({
        "type": "wait",
        "from": DRONE_ID,
        "value": value
    })


@app.route("/commit", methods=["POST"])
def commit():
    global commit_votes
    global decided_value

    data = request.json
    value = data["value"]
    sender = data["from"]

    if value not in commit_votes:
        commit_votes[value] = set()

    commit_votes[value].add(sender)

    print(f"[{DRONE_ID}] recebeu COMMIT de {sender}: {value}")

    total_nodes = len(NODES) + 1
    quorum = (2 * total_nodes) // 3 + 1

    if len(commit_votes[value]) >= quorum:
        decided_value = value
        print(f"[{DRONE_ID}] DECIDIU valor final: {value}")

        return jsonify({
            "status": "decided",
            "value": value
        })

    return jsonify({
        "status": "waiting",
        "value": value
    })


@app.route("/start_bft", methods=["GET"])
def start_bft():
    proposal = f"leader={DRONE_ID}"

    print(f"[{DRONE_ID}] iniciando BFT com proposta: {proposal}")

    prepares = []

    for node in NODES:
        try:
            res = requests.post(
                f"{node}/propose",
                json={"from": DRONE_ID, "value": proposal},
                timeout=3
            )
            prepares.append(res.json())
        except Exception as e:
            print(f"[{DRONE_ID}] erro PROPOSE para {node}: {e}")

    prepares.append({
        "type": "prepare",
        "from": DRONE_ID,
        "value": proposal
    })

    commits = []

    for prep in prepares:
        for node in NODES:
            try:
                res = requests.post(
                    f"{node}/prepare",
                    json=prep,
                    timeout=3
                )
                commits.append(res.json())
            except Exception as e:
                print(f"[{DRONE_ID}] erro PREPARE para {node}: {e}")

    for commit_msg in commits:
        if commit_msg.get("type") == "commit":
            for node in NODES:
                try:
                    requests.post(
                        f"{node}/commit",
                        json=commit_msg,
                        timeout=3
                    )
                except Exception as e:
                    print(f"[{DRONE_ID}] erro COMMIT para {node}: {e}")

    return jsonify({
        "status": "bft_started",
        "proposal": proposal
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
