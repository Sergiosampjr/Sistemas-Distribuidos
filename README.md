# Trabalho Prático – Fundamentos de Sistemas Distribuídos

## Autor

Sergio Nunes
Universidade Estadual do Ceará (UECE)
Disciplina: Fundamentos de Sistemas Distribuídos

---

# Descrição

Este projeto implementa uma rede de drones virtuais utilizando Python, Flask e Mininet.

Foram implementados três algoritmos de consenso distribuído:

* Raft
* PBFT (Practical Byzantine Fault Tolerance)
* Lamport-Shostak-Pease (LSP)

O objetivo é simular diferentes tipos de falhas em sistemas distribuídos:

* falhas de crash;
* falhas por omissão;
* falhas de temporização;
* falhas bizantinas.

---

# Estrutura Principal

```text
drone.py             -> Implementação do Raft
bft_drone.py         -> Implementação do PBFT
lsp_drone.py         -> Implementação do Lamport-Shostak-Pease

topology.py          -> Topologia da rede no Mininet

gerar_raft.py        -> Gera comandos para executar o Raft
gerar_bft.py         -> Gera comandos para executar o PBFT
gerar_lsp.py         -> Gera comandos para executar o LSP

comandos_raft_auto.txt
comandos_bft_auto.txt
comandos_lsp_auto.txt

teste_raft_auto.txt
teste_bft_10.txt
teste_lsp_10.txt
```

---

# Pré-requisitos

Instalar dependências Python:

```bash
pip install flask requests
```

Ativar o ambiente virtual:

```bash
source venv/bin/activate
```

Antes de cada teste, limpar o Mininet:

```bash
sudo mn -c
```

Executar a topologia:

```bash
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Após executar esse comando, o terminal deve entrar no modo:

```text
mininet>
```

Os comandos `source`, `h1`, `h2`, `h3`, etc. devem ser executados dentro do prompt do Mininet.

---

# Cenários Solicitados pelo Professor

O trabalho exige a execução dos seguintes cenários:

1. 5 drones com falhas crash, omissão e temporização, variando de 1 a 3 nós com falha.
2. 10 drones com falhas crash, omissão e temporização, variando de 1 a 6 nós com falha.
3. 5 drones com falhas bizantinas, variando de 1 a 2 nós bizantinos.
4. 10 drones com falhas bizantinas, variando de 1 a 4 nós bizantinos.

Neste projeto:

* os cenários de crash, omissão e temporização foram simulados com Raft;
* os cenários bizantinos foram simulados com PBFT;
* o LSP foi implementado como experimento complementar para falhas bizantinas.

---

# 1. Cenário com 5 drones e falhas crash/omissão/temporização

## Gerar os comandos

No terminal normal:

```bash
python3 gerar_raft.py 5
```

## Iniciar o Mininet

```bash
sudo mn -c
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

## Subir os drones

Dentro do Mininet:

```bash
source comandos_raft_auto.txt
```

Aguardar alguns segundos até que um líder seja eleito.

## Verificar o estado da rede

```bash
source teste_raft_auto.txt
```

O resultado esperado é a eleição de um líder, indicada por mensagens como:

```text
VIROU LÍDER
heartbeat de droneX
```

## Simular falhas

Para simular falha de crash, omissão ou temporização, alguns drones são removidos da rede.

### Falha em 1 nó

```bash
h3 pkill -f "drone.py drone3"
```

### Falha em 2 nós

```bash
h3 pkill -f "drone.py drone3"
h4 pkill -f "drone.py drone4"
```

### Falha em 3 nós

```bash
h3 pkill -f "drone.py drone3"
h4 pkill -f "drone.py drone4"
h5 pkill -f "drone.py drone5"
```

Após cada teste:

```bash
source teste_raft_auto.txt
```

Resultado esperado:

* com maioria ativa, o sistema continua funcionando;
* se o líder falhar, outro drone pode iniciar eleição;
* se não houver quórum suficiente, o consenso deixa de ser garantido.

---

# 2. Cenário com 10 drones e falhas crash/omissão/temporização

## Gerar os comandos

```bash
python3 gerar_raft.py 10
```

## Iniciar o Mininet

```bash
sudo mn -c
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

## Subir os drones

Dentro do Mininet:

```bash
source comandos_raft_auto.txt
```

Aguardar a eleição do líder.

## Verificar a rede

```bash
source teste_raft_auto.txt
```

## Simular falhas de 1 a 6 nós

### Falha em 1 nó

```bash
h3 pkill -f "drone.py drone3"
```

### Falha em 2 nós

```bash
h3 pkill -f "drone.py drone3"
h4 pkill -f "drone.py drone4"
```

### Falha em 3 nós

```bash
h3 pkill -f "drone.py drone3"
h4 pkill -f "drone.py drone4"
h5 pkill -f "drone.py drone5"
```

### Falha em 4 nós

```bash
h3 pkill -f "drone.py drone3"
h4 pkill -f "drone.py drone4"
h5 pkill -f "drone.py drone5"
h6 pkill -f "drone.py drone6"
```

### Falha em 5 nós

```bash
h3 pkill -f "drone.py drone3"
h4 pkill -f "drone.py drone4"
h5 pkill -f "drone.py drone5"
h6 pkill -f "drone.py drone6"
h7 pkill -f "drone.py drone7"
```

### Falha em 6 nós

```bash
h3 pkill -f "drone.py drone3"
h4 pkill -f "drone.py drone4"
h5 pkill -f "drone.py drone5"
h6 pkill -f "drone.py drone6"
h7 pkill -f "drone.py drone7"
h8 pkill -f "drone.py drone8"
```

Após cada teste:

```bash
source teste_raft_auto.txt
```

Resultado esperado:

* até certo limite, o Raft mantém o funcionamento por maioria;
* com perda de maioria, a rede não consegue manter consenso estável.

---

# 3. Cenário com 5 drones e falhas bizantinas

Para falhas bizantinas foi utilizado o PBFT.

## 5 drones com 1 nó bizantino

No terminal normal:

```bash
sudo mn -c
python3 gerar_bft.py 5 3
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_bft_auto.txt
```

Iniciar consenso:

```bash
h1 curl http://10.0.0.1:5001/start_bft
```

Consultar drones honestos:

```bash
h2 curl http://10.0.0.2:5002
h4 curl http://10.0.0.4:5004
h5 curl http://10.0.0.5:5005
```

Resultado esperado:

```text
DECIDIU valor final: leader=drone1
```

ou:

```json
"decided_value":"leader=drone1"
```

## 5 drones com 2 nós bizantinos

```bash
sudo mn -c
python3 gerar_bft.py 5 3,4
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_bft_auto.txt
h1 curl http://10.0.0.1:5001/start_bft
h2 curl http://10.0.0.2:5002
h5 curl http://10.0.0.5:5005
```

Resultado esperado:

```text
Consenso não garantido
```

Isso ocorre porque, para tolerar 2 bizantinos, seriam necessários pelo menos 7 participantes.

---

# 4. Cenário com 10 drones e falhas bizantinas

## 10 drones com 1 nó bizantino

```bash
sudo mn -c
python3 gerar_bft.py 10 3
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_bft_auto.txt
source teste_bft_10.txt
```

Resultado esperado:

```text
DECIDIU valor final: leader=drone1
```

## 10 drones com 2 nós bizantinos

```bash
sudo mn -c
python3 gerar_bft.py 10 3,4
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_bft_auto.txt
source teste_bft_10.txt
```

Resultado esperado:

```text
DECIDIU valor final: leader=drone1
```

## 10 drones com 3 nós bizantinos

```bash
sudo mn -c
python3 gerar_bft.py 10 3,4,5
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_bft_auto.txt
source teste_bft_10.txt
```

Resultado esperado:

```text
QUORUM PREPARE atingido
DECIDIU valor final: leader=drone1
```

## 10 drones com 4 nós bizantinos

```bash
sudo mn -c
python3 gerar_bft.py 10 3,4,5,6
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_bft_auto.txt
source teste_bft_10.txt
```

Resultado esperado:

```json
"decided_value": null
```

ou:

```text
Consenso não garantido
```

Esse cenário ultrapassa o limite teórico do PBFT.

---

# 5. Cenários Complementares com Lamport-Shostak-Pease

O LSP foi utilizado como implementação complementar para demonstrar votação majoritária diante de falhas bizantinas.

## 10 drones com 1 bizantino

```bash
sudo mn -c
python3 gerar_lsp.py 10 3
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_lsp_auto.txt
source teste_lsp_10.txt
```

Resultado esperado:

```text
leader=drone1
```

## 10 drones com 2 bizantinos

```bash
sudo mn -c
python3 gerar_lsp.py 10 3,4
sudo PYTHONPATH=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/mininet-src python3 topology.py
```

Dentro do Mininet:

```bash
source comandos_lsp_auto.txt
source teste_lsp_10.txt
```

Resultado esperado:

```text
leader=drone1
```

---

# Resumo dos Resultados Esperados

| Cenário                                  | Algoritmo | Resultado esperado                       |
| ---------------------------------------- | --------- | ---------------------------------------- |
| 5 drones com crash/omissão/temporização  | Raft      | Consenso mantido enquanto houver maioria |
| 10 drones com crash/omissão/temporização | Raft      | Consenso mantido enquanto houver maioria |
| 5 drones com 1 bizantino                 | PBFT      | Consenso mantido                         |
| 5 drones com 2 bizantinos                | PBFT      | Consenso não garantido                   |
| 10 drones com 1 bizantino                | PBFT      | Consenso mantido                         |
| 10 drones com 2 bizantinos               | PBFT      | Consenso mantido                         |
| 10 drones com 3 bizantinos               | PBFT      | Consenso mantido                         |
| 10 drones com 4 bizantinos               | PBFT      | Consenso não garantido                   |
| 10 drones com 1 bizantino                | LSP       | Consenso mantido                         |
| 10 drones com 2 bizantinos               | LSP       | Consenso mantido                         |

---

# Observações Finais

O Raft utiliza maioria simples para manter consenso. Portanto, enquanto mais da metade dos drones permanecer ativa, o sistema tende a continuar operando.

O PBFT utiliza a condição:

```text
N >= 3m + 1
```

onde `N` é o número total de drones e `m` é o número máximo de participantes bizantinos.

Assim:

```text
10 drones toleram até 3 bizantinos.
5 drones toleram até 1 bizantino.
```

O Lamport-Shostak-Pease foi usado como complemento para mostrar consenso por votação majoritária em cenários bizantinos.
