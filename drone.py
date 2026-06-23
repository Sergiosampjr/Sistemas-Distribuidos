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
NODES = sys.argv[5:]




FAILURE_TYPE = sys.argv[3]
FAILURE_RATE = float(sys.argv[4])

# parâmetros de falha
FAILURE_MODE = sys.argv[3] if len(sys.argv) > 3 else "none"
FAILURE_RATE = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3

# agora os nodes começam depois
NODES = sys.argv[5:] if len(sys.argv) > 5 else []



# 🔥 RAFT
state = "follower"
voted_for = None
votes = 0
last_heartbeat = time.time()
current_term = 0


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "drone": DRONE_ID,
        "state": state,
        "term": current_term,
        "voted_for": voted_for,
        "nodes": len(NODES)
    })



@app.route("/vote", methods=["POST"])
def vote():
    global current_term
    global voted_for
    global state
    global last_heartbeat

    data = request.json

    candidate = data["candidate"]
    term = data["term"]

    print(f"[{DRONE_ID}] recebeu pedido de voto de {candidate}")

    if FAILURE_MODE == "omission":
        if random.random() < FAILURE_RATE:
            print(f"[{DRONE_ID}] OMITIU voto")
            return jsonify({
                "vote_granted": False,
                "term": current_term
            })

    if FAILURE_MODE == "delay":
        print(f"[{DRONE_ID}] atrasando voto...")
        time.sleep(3)

    if term > current_term:
        current_term = term
        voted_for = None
        state = "follower"

    if voted_for is None or voted_for == candidate:
        voted_for = candidate
        last_heartbeat = time.time()

        print(f"[{DRONE_ID}] votou em {candidate}")

        return jsonify({
            "vote_granted": True,
            "term": current_term
        })

    print(f"[{DRONE_ID}] rejeitou voto para {candidate}. Já votou em {voted_for}")

    return jsonify({
        "vote_granted": False,
        "term": current_term
    })





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
        print(f"[{DRONE_ID}] pedindo voto para {node}")
        try:
            res = requests.post(
                f"{node}/vote",
                json={"candidate": DRONE_ID, "term": current_term}
            )

            data = res.json()

            if data.get("vote_granted") == True:
                votes += 1
                print(f"[{DRONE_ID}] recebeu voto de {node}")
            else:
                print(f"[{DRONE_ID}] voto negado por {node}")    

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

    fail = simulate_failure()

    if fail == "omit":
        return jsonify({"status": "ignored"})

    leader = request.json["leader"]
    term = request.json["term"]

    if fail == "byzantine":
        print(f"[{DRONE_ID}] ignorando heartbeat (bizantino)")
        return jsonify({"status": "fake"})

    if term >= current_term:
        current_term = term
        state = "follower"
        last_heartbeat = time.time()
        voted_for = None

        print(f"[{DRONE_ID}] heartbeat de {leader} (term {term})")

    return jsonify({"status": "ok"})

def send_heartbeat():
    global state, current_term

    while True:
        if state == "leader":
            for node in NODES:
                try:
                    if FAILURE_MODE == "byzantine":
                        fake_leader = f"fake_{DRONE_ID}"
                        requests.post(
                            f"{node}/heartbeat",
                            json={"leader": fake_leader, "term": current_term},
                            timeout=1
                        )
                    else:
                        requests.post(
                            f"{node}/heartbeat",
                            json={"leader": DRONE_ID, "term": current_term},
                            timeout=1
                        )
                except:
                    pass
        time.sleep(1)


def simulate_failure():
    if FAILURE_MODE == "omission" and random.random() < FAILURE_RATE:
        print(f"[{DRONE_ID}] OMITIU mensagem")
        return "omit"

    if FAILURE_MODE == "delay":
        delay = random.uniform(2, 5)
        print(f"[{DRONE_ID}] DELAY de {delay:.2f}s")
        time.sleep(delay)

    if FAILURE_MODE == "byzantine":
        return "byzantine"

    return "ok"




if __name__ == "__main__":
    threading.Thread(target=election_timer, daemon=True).start()
    threading.Thread(target=send_heartbeat, daemon=True).start()  # 🔥 FALTAVA ISSO

    app.run(host="0.0.0.0", port=PORT)