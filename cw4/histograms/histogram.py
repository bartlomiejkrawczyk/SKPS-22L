import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

for subdir in Path("histograms").glob("?_?_?"):
    clients = []

    for client in sorted(subdir.glob("cli_?.txt"), key=lambda f: f.name):
        with client.open(mode="r") as f:
            clients.append([int(line.rpartition(" ")[2]) for line in f if line])

    if subdir.name[0] == "5":
        additional_args = {"bins": 20, "range": (0, 400)}
    else:
        additional_args = {"bins": 20}

    plt.clf()
    plt.hist(clients, label=[f"Klient {idx}" for idx, _ in enumerate(clients)],
             **additional_args)
    plt.legend()
    plt.xlabel("czas dostarczenia [us]")
    plt.ylabel("liczba wystąpień")
    plt.savefig(subdir / "hist.png")

# servers = []
# for idx in ("0", "1"):
#     server_path = f"histograms/6/server_var{idx}.txt"
#     with open(server_path, mode="r") as f:
#         servers.append([int(line.rpartition(" ")[2]) for line in f if line][1:])
# plt.clf()
# plt.hist(servers, label=["Wariant 0", "Wariant 1"], bins=20)
# plt.legend()
# plt.xlabel("czas między pobraniem próbek [us]")
# plt.ylabel("liczba wystąpień")
# plt.savefig(Path("histograms") / "6" / "hist.png")
