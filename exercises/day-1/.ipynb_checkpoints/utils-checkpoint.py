"""
viz_utils.py
------------
Funzioni di visualizzazione condivise tra i notebook dell'esercitazione.
Import: `from viz_utils import draw_peer_key_graph, num_pairwise_keys`
"""
import itertools
import numpy as np
import matplotlib.pyplot as plt


def num_pairwise_keys(n):
    """Numero di chiavi simmetriche pairwise necessarie per N peer: C(n, 2)."""
    return n * (n - 1) // 2


def draw_peer_key_graph(n=8):
    """Disegna il grafo dei peer con tutte le chiavi pairwise (sinistra)
    e la curva di crescita del numero di chiavi (destra), con il punto
    corrente evidenziato."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # --- Pannello sinistro: grafo dei peer con tutte le chiavi pairwise ---
    ax = axes[0]
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    xs, ys = np.cos(angles), np.sin(angles)
    for i, j in itertools.combinations(range(n), 2):
        ax.plot([xs[i], xs[j]], [ys[i], ys[j]], color='tab:blue', alpha=0.3, linewidth=0.8, zorder=1)
    ax.scatter(xs, ys, s=250, color='tab:orange', zorder=2, edgecolor='black')
    for i in range(n):
        label = f"P{i+1}" if n <= 20 else ""
        ax.annotate(label, (xs[i], ys[i]), ha='center', va='center', fontsize=8, zorder=3)
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_aspect('equal'); ax.axis('off')
    n_keys = num_pairwise_keys(n)
    ax.set_title(f"N = {n} peer  ->  {n_keys} chiavi\n(ogni arco = una chiave simmetrica pre-condivisa)")

    # --- Pannello destro: curva di crescita, con il punto corrente evidenziato ---
    ax2 = axes[1]
    n_range = np.arange(2, 61)
    keys_range = n_range * (n_range - 1) // 2
    ax2.plot(n_range, keys_range, color='tab:blue', label="C(N,2) = N(N-1)/2")
    ax2.scatter([n], [n_keys], color='tab:red', zorder=5, s=80, label=f"N={n} -> {n_keys} chiavi")
    ax2.set_xlabel("numero di peer N"); ax2.set_ylabel("numero di chiavi necessarie")
    ax2.set_title("Crescita del numero di chiavi pre-condivise")
    ax2.legend(); ax2.grid(True, alpha=0.3)

    plt.tight_layout(); plt.show()


def openssl_hex(value, bytes_per_line=16):
    """Format an integer like OpenSSL: 16 bytes per line."""

    data = value.to_bytes(
        (value.bit_length() + 7) // 8,
        byteorder="big"
    )

    # Aggiungi 00 se necessario per rappresentare
    # l'INTEGER come valore positivo.
    if data and data[0] & 0x80:
        data = b"\x00" + data

    lines = []

    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i + bytes_per_line]

        line = ":".join(f"{byte:02x}" for byte in chunk)

        lines.append(line)

    return lines


def print_openssl_hex(name, value):
    lines = openssl_hex(value)

    # "n =  "
    first_prefix = f"{name} =  "

    # Allinea le righe successive esattamente
    # sotto l'inizio del valore esadecimale.
    continuation_prefix = " " * len(first_prefix)

    print(first_prefix + lines[0])

    for line in lines[1:]:
        print(continuation_prefix + line)