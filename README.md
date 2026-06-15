# Sistemas Distribuídos – Consenso entre Drones

## Descrição

Projeto desenvolvido para a disciplina de Sistemas Distribuídos utilizando Python, Flask e Mininet.

O objetivo é simular uma rede de drones distribuídos e implementar algoritmos de consenso capazes de tolerar diferentes tipos de falhas:

* Falhas de Crash
* Falhas de Omissão
* Falhas de Temporização
* Falhas Bizantinas

---

# Tecnologias Utilizadas

* Python 3
* Flask
* Requests
* Mininet
* Ubuntu 20.04+

---

# Estrutura do Projeto

```text
Sistemas-Distribuidos/
│
├── drone.py
├── topology.py
│
├── bft_drone.py
├── gerar_bft.py
├── comandos_bft_auto.txt
├── teste_bft_10.txt
│
├── lsp_drone.py
├── gerar_lsp.py
├── comandos_lsp_auto.txt
├── teste_lsp_10.txt
│
├── README.md
└── venv/
```

---

# Instalação

## 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd Sistemas-Distribuidos
```

---

## 2. Criar Ambiente Virtual

```bash
python3 -m venv venv
```

Ativar:

```bash
source venv/bin/activate
```

---

## 3. Instalar Dependências

```bash
pip install flask requests
```

Verificar:

```bash
pip list
```

---

## 4. Instalar o Mininet

Remover versões antigas:

```bash
sudo apt remove mininet
```

Instalar versão oficial:

```bash
git clone https://github.com/mininet/mininet.git mininet-src

cd mininet-src

sudo ./util/install.sh -a
```

---

# Topologia

A topologia utilizada cria uma rede com até 10 drones.

Executar:

```bash
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Teste de conectividade:

```text
mininet> pingall
```

Resultado esperado:

```text
*** Results: 0% dropped
```

---

# Algoritmo 1 – Raft

Arquivo:

```text
drone.py
```

Objetivo:

* Eleição de líder
* Tolerância a falhas de crash
* Tolerância a falhas de omissão
* Tolerância a falhas de temporização

Exemplo:

```bash
python3 drone.py drone1 5001
```

---

# Algoritmo 2 – BFT/PBFT

Arquivo:

```text
bft_drone.py
```

Objetivo:

* Consenso Bizantino
* Fases PRE-PREPARE
* PREPARE
* COMMIT

---

## Gerar Cenário

Exemplo:

```bash
python3 gerar_bft.py 10 3
```

Resultado:

```text
10 drones
1 bizantino (drone3)
```

Arquivo gerado:

```text
comandos_bft_auto.txt
```

---

## Executar Cenário

Dentro do Mininet:

```text
source comandos_bft_auto.txt
```

---

## Executar Teste

```text
source teste_bft_10.txt
```

---

## Regra de Tolerância

Para tolerar m nós bizantinos:

```text
N ≥ 3m + 1
```

Exemplos:

```text
1 bizantino -> mínimo 4 nós
2 bizantinos -> mínimo 7 nós
3 bizantinos -> mínimo 10 nós
```

---

# Algoritmo 3 – Lamport-Shostak-Pease

Arquivo:

```text
lsp_drone.py
```

Objetivo:

Resolver o problema dos Generais Bizantinos utilizando votação majoritária.

---

## Gerar Cenário

Exemplo:

```bash
python3 gerar_lsp.py 10 3
```

Resultado:

```text
Drones: 10
Bizantinos: [3]
```

Arquivo gerado:

```text
comandos_lsp_auto.txt
```

---

## Executar Cenário

Dentro do Mininet:

```text
source comandos_lsp_auto.txt
```

---

## Executar Teste

```text
source teste_lsp_10.txt
```

---

## Exemplo de Resultado

Drone bizantino:

```text
drone3 -> leader=fake_drone3
```

Resultado final:

```json
{
  "decided_value": "leader=drone1",
  "votes": {
    "leader=drone1": 8,
    "leader=fake_drone3": 1
  }
}
```

Decisão correta:

```text
leader=drone1
```

---

# Cenários Testados

## BFT

### Cenário 1

```text
5 drones
1 bizantino
```

### Cenário 2

```text
10 drones
1 bizantino
```

### Cenário 3

```text
10 drones
3 bizantinos
```

### Cenário 4

```text
10 drones
4 bizantinos
```

Resultado esperado:

```text
Violação da condição N ≥ 3m + 1
```

---

## Lamport-Shostak-Pease

### Cenário 1

```text
10 drones
1 bizantino
```

Resultado:

```text
Consenso alcançado
```

---

# Limpeza do Ambiente

Antes de iniciar novos testes:

```bash
sudo mn -c
```

---

# Autor

Sergio Nunes

Curso de Ciência da Computação – UECE

Disciplina: Sistemas Distribuídos
