import sys

if len(sys.argv) < 3:
    print("Uso: python3 gerar_lsp.py <qtd_drones> <bizantinos>")
    print("Exemplo: python3 gerar_lsp.py 10 3,6")
    sys.exit()

N = int(sys.argv[1])

bizantinos = set()

if sys.argv[2].strip():
    bizantinos = set(int(x) for x in sys.argv[2].split(","))

PYTHON = "/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/venv/bin/python3"

with open("comandos_lsp_auto.txt", "w") as f:

    for i in range(1, N + 1):

        port = 6000 + i

        nodes = []

        for j in range(1, N + 1):
            if i != j:
                nodes.append(
                    f"http://10.0.0.{j}:{6000+j}"
                )

        mode = "none"
        rate = "0.0"

        if i in bizantinos:
            mode = "byzantine"
            rate = "1.0"

        cmd = (
            f"h{i} {PYTHON} "
            f"lsp_drone.py "
            f"drone{i} "
            f"{port} "
            f"{mode} "
            f"{rate} "
            f"{' '.join(nodes)} &\n"
        )

        f.write(cmd)

print("Arquivo comandos_lsp_auto.txt gerado.")
print(f"Drones: {N}")
print(f"Bizantinos: {sorted(bizantinos)}")
