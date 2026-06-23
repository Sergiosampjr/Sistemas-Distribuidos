# gerar_raft.py

import sys

N = int(sys.argv[1])

with open("comandos_raft_auto.txt", "w") as f:

    for i in range(1, N + 1):

        port = 5000 + i

        nodes = ""

        for j in range(1, N + 1):
            if i != j:
                nodes += f" http://10.0.0.{j}:{5000+j}"

        linha = (
            f"h{i} "
            f"/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/venv/bin/python3 "
            f"drone.py "
            f"drone{i} "
            f"{port} "
            f"none "
            f"0.0 "
            f"{nodes} &\n"
        )

        f.write(linha)

print(f"Arquivo gerado para {N} drones.")   