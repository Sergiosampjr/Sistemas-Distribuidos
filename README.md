# 🚀 Sistema Distribuído com RAFT + Flask + Mininet

Este projeto implementa um sistema distribuído baseado no algoritmo de consenso **RAFT**, utilizando **Python** e **Flask**, com suporte para execução local e em rede simulada com **Mininet**.

---

# 📌 Requisitos

## 🔹 Windows / Linux

* Python 3.8+
* pip
* Git (opcional)

## 🔹 Linux (para Mininet)

* Ubuntu 20.04+ (ou WSL2)
* Mininet instalado

---

# ⚙️ Instalação

## 1. Clonar o projeto

```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>
```

## 2. Criar ambiente virtual

### ▶️ Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### ▶️ Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install flask requests
```

---

# 🖥️ Execução LOCAL (sem Mininet)

## ▶️ Passo 1: Abrir 3 terminais

---

## ▶️ Passo 2: Executar os drones

### Terminal 1

```bash
python drone.py drone1 5001 http://127.0.0.1:5002 http://127.0.0.1:5003
```

### Terminal 2

```bash
python drone.py drone2 5002 http://127.0.0.1:5001 http://127.0.0.1:5003
```

### Terminal 3

```bash
python drone.py drone3 5003 http://127.0.0.1:5001 http://127.0.0.1:5002
```

---

## ✅ Resultado esperado

* Um drone será eleito líder:

```
VIROU LÍDER 🚀
```

* Os outros receberão heartbeat:

```
heartbeat de droneX
```

---

## 🧪 Teste de falha

1. Pare o líder (CTRL + C)
2. Observe:

```
novo líder será eleito automaticamente
```

---

# 🌐 Execução com Mininet (Linux)

---

## ▶️ 1. Instalar Mininet

```bash
sudo apt update
sudo apt install mininet
```

---

## ▶️ 2. Criar arquivo `network.py`

```python
from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI

topo = SingleSwitchTopo(3)
net = Mininet(topo)
net.start()

CLI(net)
net.stop()
```

---

## ▶️ 3. Iniciar o Mininet

```bash
sudo python3 network.py
```

---

## ▶️ 4. Testar conectividade

```bash
mininet> pingall
```

Resultado esperado:

```
0% packet loss
```

---

## ▶️ 5. Abrir terminais dos hosts

```bash
mininet> xterm h1 h2 h3
```

---

## ▶️ 6. Executar os drones

### h1

```bash
python3 drone.py drone1 5000 http://10.0.0.2:5000 http://10.0.0.3:5000
```

### h2

```bash
python3 drone.py drone2 5000 http://10.0.0.1:5000 http://10.0.0.3:5000
```

### h3

```bash
python3 drone.py drone3 5000 http://10.0.0.1:5000 http://10.0.0.2:5000
```

---

## ✅ Resultado esperado

* Eleição de líder automática
* Comunicação entre nós via rede simulada
* Heartbeats funcionando corretamente

---

## 💥 Teste de falha de rede

No Mininet:

```bash
mininet> link h1 s1 down
```

Resultado esperado:

* Novo líder será eleito automaticamente

---

# 🧠 Tecnologias utilizadas

* Python
* Flask
* RAFT (Leader Election + Heartbeat)
* Mininet

---

# 📌 Funcionalidades

* Eleição de líder (RAFT)
* Comunicação entre nós via HTTP
* Heartbeat para manutenção do líder
* Tolerância a falhas
* Simulação de rede com Mininet

---

# 👨‍💻 Autor

Desenvolvido para disciplina de Sistemas Distribuídos.
