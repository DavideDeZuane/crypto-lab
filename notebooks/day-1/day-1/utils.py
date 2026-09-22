"""
viz_utils.py
------------
Funzioni di visualizzazione condivise tra i notebook dell'esercitazione.
Import: `from viz_utils import draw_peer_key_graph, num_pairwise_keys`
"""
import itertools
import hashlib
import secrets
import numpy as np
import matplotlib.pyplot as plt
import math, random, time, itertools
from sympy import factorint, isprime, totient

import os, time, itertools, random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, IntSlider

K = 1024
K_BYTES = 1024 // 8
K0_BYTES = 128 // 8  # 16 byte
K1_BYTES = 128 // 8  # 16 byte
N_MAX = K_BYTES - K0_BYTES - K1_BYTES

def num_pairwise_keys(n):
    """Numero di chiavi simmetriche pairwise necessarie per N peer: C(n, 2)."""
    return n * (n - 1) // 2

def primitive_root(p):
    n = p - 1

    # Fattori primi distinti di p-1
    factors = factorint(n).keys()

    for g in range(2, p):
        if all(pow(g, n // q, p) != 1 for q in factors):
            return g

def primitive_roots_bruteforce(p): 
    g_candidates = []

    for i in range(1, p): 
        generated_elements = set()

        for exp in range(1, p): 
            value = pow(i, exp, p) 
            generated_elements.add(value)

            if len(generated_elements) == p - 1: 
                break

        if len(generated_elements) == p - 1: 
            g_candidates.append(i)

    return g_candidates

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



def mgf1(seed: bytes, length: int, hash_func=hashlib.sha256) -> bytes:
    """Mask Generation Function 1 (RFC 8017)."""
    hlen = hash_func().digest_size
    if length > (2**32) * hlen:
        raise ValueError("Lunghezza mascherata troppo grande")
    
    output = b""
    counter = 0
    while len(output) < length:
        c = counter.to_bytes(4, byteorder='big')
        output += hash_func(seed + c).digest()
        counter += 1
    
    return output[:length]


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

# ==================== G e H ====================
# dato un seed genere uno stream lungo K - K0
def G(seed: bytes, out_len=K_BYTES - K0_BYTES, hash_func=hashlib.sha256) -> bytes:
    return mgf1(seed, out_len, hash_func)


def H(x: bytes, out_len = K0_BYTES, hash_func=hashlib.sha256) -> bytes:
    """H: {0,1}^(k-k0) -> {0,1}^k0. Comprime il blocco mascherato."""
    return mgf1(x, out_len, hash_func)

def compare_primitive_roots(test_primes):
    brute_times = []
    smart_times = []

    print(f"{'p':>6} | {'Brute force (s)':>17} | {'Metodo efficiente (s)':>22}")
    print("-" * 51)

    for p in test_primes:

        # Brute force
        t0 = time.perf_counter()
        primitive_roots_bruteforce(p)
        brute_time = time.perf_counter() - t0

        # Metodo efficiente
        t0 = time.perf_counter()
        primitive_root(p)
        smart_time = time.perf_counter() - t0

        brute_times.append(brute_time)
        smart_times.append(smart_time)

        print(f"{p:6d} | {brute_time:17.6f} | {smart_time:22.6f}")

    # Grafico
    plt.figure(figsize=(6, 4))

    plt.plot(
        test_primes,
        brute_times,
        marker='o',
        label='Brute force'
    )

    plt.plot(
        test_primes,
        smart_times,
        marker='o',
        label='Metodo efficiente'
    )

    plt.xlabel("p")
    plt.ylabel("Tempo (s)")
    plt.title("Confronto dei tempi")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()



def try_open(ct, guess_key_int):
    k = guess_key_int.to_bytes(16, 'big')
    try:
        pt = unpad(AES.new(k, AES.MODE_ECB).decrypt(ct), 16)
    except Exception:
        return None
    return pt if pt.startswith(b"PUZZLE#") else None

def bob_solves(puzzles, key_bits):
    """Bob sceglie UN puzzle a caso e lo rompe per forza bruta: costo atteso O(2^key_bits / 2)."""
    idx = random.randrange(len(puzzles))
    for guess in range(2**key_bits):
        pt = try_open(puzzles[idx], guess)
        if pt is not None:
            return idx, pt[11:], guess + 1
    return None, None, None

def eve_breaks_all(puzzles, key_bits):
    """Eve non sa quale puzzle useranno: nel caso peggiore deve romperli tutti."""
    attempts = 0
    for ct in puzzles:
        for guess in range(2**key_bits):
            attempts += 1
            if try_open(ct, guess) is not None:
                break
    return attempts

def make_puzzles(n_puzzles, key_bits):
    """Alice genera n_puzzles puzzle. Ognuno cela una chiave di sessione dietro
    una chiave-puzzle debole a key_bits bit, cifrata con AES-ECB (va bene per la demo:
    qui vogliamo solo mostrare il costo di brute force, non la sicurezza di AES)."""
    puzzles, session_keys = [], []
    for i in range(n_puzzles):
        weak_key = random.getrandbits(key_bits).to_bytes(16, 'big')
        session_key = os.urandom(16)
        plaintext = pad(b"PUZZLE#" + i.to_bytes(4, 'big') + session_key, 16)
        ct = AES.new(weak_key, AES.MODE_ECB).encrypt(plaintext)
        puzzles.append(ct)
        session_keys.append(session_key)
    return puzzles, session_keys
    

def merkle_puzzles(n_puzzles=6, key_bits=14):
    # Alice genera i puzzle
    puzzles, session_keys = make_puzzles(n_puzzles, key_bits)

    # Bob sceglie e risolve un puzzle
    t0 = time.perf_counter()
    idx, session_key, bob_attempts = bob_solves(puzzles, key_bits)
    bob_time = time.perf_counter() - t0

    # Eve prova a risolvere tutti i puzzle
    t0 = time.perf_counter()
    eve_attempts = eve_breaks_all(puzzles, key_bits)
    eve_time = time.perf_counter() - t0

    print("=== Merkle Puzzles ===")
    print(f"Numero di puzzle:        {n_puzzles}")
    print(f"Chiave-puzzle:           {key_bits} bit")
    print()
    print(f"Bob:")
    print(f"  puzzle scelto:         #{idx}")
    print(f"  tentativi:             {bob_attempts:>10}")
    print(f"  tempo:                 {bob_time:.4f} s")
    print()
    print(f"Eve:")
    print(f"  tentativi:             {eve_attempts:>10}")
    print(f"  tempo:                 {eve_time:.4f} s")
    print()
    print(f"Chiave condivisa:        {session_key == session_keys[idx]}")

    return {
        "bob_attempts": bob_attempts,
        "bob_time": bob_time,
        "eve_attempts": eve_attempts,
        "eve_time": eve_time,
    }

def plot_merkle_cost(Ks, N_values):
    bob_cost = [2**k / 2 for k in Ks]

    plt.figure(figsize=(6, 4))

    # Costo di Bob: un solo puzzle
    plt.plot(
        Ks,
        bob_cost,
        marker='o',
        label="Costo Bob (1 puzzle)"
    )

    # Costo di Eve per ogni N
    for N in N_values:
        eve_cost = [N * (2**k / 2) for k in Ks]

        plt.plot(
            Ks,
            eve_cost,
            marker='o',
            label=f"Costo Eve (N={N} puzzle)"
        )

    plt.yscale('log')
    plt.xlabel("bit della chiave-puzzle (K)")
    plt.ylabel("tentativi attesi (scala log)")
    plt.title("Merkle Puzzles: costo di Bob ed Eve")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.show()