import sys

if len(sys.argv) < 3:
    print("Uso: python3 gerar_bft.py <qtd_drones> <bizantinos separados por virgula>")
    print("Exemplo: python3 gerar_bft.py 10 3,6,8")
    sys.exit()

N = int(sys.argv[1])
bizantinos = set()

if sys.argv[2].strip():
    bizantinos = set(int(x) for x in sys.argv[2].split(","))

PYTHON = "/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/venv/bin/python3"

with open("comandos_bft_auto.txt", "w") as f:
    for i in range(1, N + 1):
        port = 5000 + i

        nodes = []
        for j in range(1, N + 1):
            if i != j:
                nodes.append(f"http://10.0.0.{j}:{5000+j}")

        mode = "byzantine" if i in bizantinos else "none"
        rate = "1.0" if i in bizantinos else "0.0"

        cmd = (
            f"h{i} {PYTHON} bft_drone.py drone{i} {port} "
            f"{mode} {rate} {' '.join(nodes)} &\n"
        )

        f.write(cmd)

print("Arquivo comandos_bft_auto.txt gerado com sucesso.")
print(f"Drones: {N}")
print(f"Bizantinos: {sorted(bizantinos)}")
