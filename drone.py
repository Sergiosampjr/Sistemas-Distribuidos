from flask import Flask, request, jsonify
import requests
import sys
import threading
import time
import random

state = "follower"
voted_for = None
votes = 0
election_in_progress = False




app = Flask(__name__)

if len(sys.argv) < 3:
    print("Uso: python drone.py <id> <porta> [nodes...]")
    exit()

DRONE_ID = sys.argv[1]
PORT = int(sys.argv[2])
NODES = sys.argv[3:]


# 🔥 RAFT
state = "follower"
voted_for = None
votes = 0
last_heartbeat = time.time()
current_term = 0

@app.route("/", methods=["GET"])
def home():
    return f"{DRONE_ID} rodando!"



@app.route("/vote", methods=["POST"])
def vote():
    global voted_for, current_term, last_heartbeat, state

    candidate = request.json["candidate"]
    term = request.json["term"]

    # 🚫 NÃO vota se recebeu heartbeat recente (existe líder)
    if time.time() - last_heartbeat < 5:
        return jsonify({"vote": False, "term": current_term})

    # ignora termos antigos
    if term < current_term:
        return jsonify({"vote": False, "term": current_term})

    # atualiza termo
    if term > current_term:
        current_term = term
        voted_for = None
        state = "follower"

    if voted_for is None:
        voted_for = candidate
        print(f"[{DRONE_ID}] votou em {candidate} (term {term})")
        return jsonify({"vote": True, "term": current_term})

    return jsonify({"vote": False, "term": current_term})


def start_election():
    global state, votes, voted_for, current_term, election_in_progress

    # 🚫 evita múltiplas eleições ao mesmo tempo
    if election_in_progress:
        return

    election_in_progress = True

    current_term += 1
    state = "candidate"
    voted_for = DRONE_ID
    votes = 1

    print(f"[{DRONE_ID}] iniciou eleição (term {current_term})")

    for node in NODES:
        try:
            res = requests.post(
                f"{node}/vote",
                json={"candidate": DRONE_ID, "term": current_term}
            )

            data = res.json()

            if data.get("vote") and data.get("term") == current_term:
                votes += 1

        except:
            pass

    print(f"[{DRONE_ID}] votos: {votes}")

    if votes > (len(NODES) + 1) // 2:
        become_leader()
    else:
        state = "follower"
        voted_for = None

    election_in_progress = False  # 🔥 libera novamente

def become_leader():
    global state, last_heartbeat
    state = "leader"
    last_heartbeat = time.time()
    print(f"[{DRONE_ID}] VIROU LÍDER 🚀")

def election_timer():
    global state, last_heartbeat, election_in_progress

    while True:
        time.sleep(1)

        timeout = random.uniform(8, 12)

        if (
            state != "leader"
            and not election_in_progress
            and (time.time() - last_heartbeat) > timeout
        ):
            print(f"[{DRONE_ID}] timeout → iniciando eleição")
            start_election()

  


@app.route("/message", methods=["POST"])
def receive_message():
    data = request.json
    print(f"[{DRONE_ID}] recebeu:", data)
    return jsonify({"status": "ok"})

@app.route("/send", methods=["GET"])
def send():
    for node in NODES:
        try:
            requests.post(f"{node}/message", json={"from": DRONE_ID})
        except Exception as e:
            print("Erro:", e)
    return "mensagens enviadas"


@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    global state, last_heartbeat, current_term, voted_for

    leader = request.json["leader"]
    term = request.json["term"]

    if term >= current_term:
        current_term = term
        state = "follower"
        last_heartbeat = time.time()
        voted_for = None  # 🔥 ESSENCIAL

        print(f"[{DRONE_ID}] heartbeat de {leader} (term {term})")

    return jsonify({"status": "ok"})


def send_heartbeat():
    global state, current_term

    while True:
        if state == "leader":
            for node in NODES:
                try:
                    requests.post(
                        f"{node}/heartbeat",
                        json={"leader": DRONE_ID, "term": current_term}
                    )
                except:
                    pass
        time.sleep(1)  # antes era 2

if __name__ == "__main__":
    threading.Thread(target=election_timer, daemon=True).start()
    threading.Thread(target=send_heartbeat, daemon=True).start()  # 🔥 FALTAVA ISSO

    app.run(host="0.0.0.0", port=PORT)