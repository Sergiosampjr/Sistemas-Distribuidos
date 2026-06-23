# gerar_teste_raft.py

import sys

N = int(sys.argv[1])

with open("teste_raft_auto.txt", "w") as f:

    for i in range(1, N + 1):
        porta = 5000 + i

        f.write(
            f"h{i} curl http://10.0.0.{i}:{porta}\n"
        )

print(f"Arquivo teste_raft_auto.txt gerado para {N} drones.")