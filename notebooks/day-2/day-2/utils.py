import mpmath as mp
import sys

# Options for large parameters
sys.set_int_max_str_digits(10000)
mp.mp.dps = 2600 

def generate_modp_prime(bits, c):
    """
    Generate the RFC 3526 MODP prime:

    p = 2^bits - 2^(bits-64) - 1 + 2^64 * floor(2^(bits-130) * pi) + 2^64 * c
    """

    k = bits - 130

    # High-precision pi
    pi = mp.pi

    # floor(2^k * pi)
    floor_pi = int(mp.floor(mp.power(2, k) * pi))

    p = (
        2**bits
        - 2**(bits - 64)
        - 1
        + 2**64 * (floor_pi + c)
    )

    return p


def describe_group(name):
    params = DH_PARAMS[name]
    p = params["p"]

    print(f"[Selected group]: {name}")
    print(f"\tRFC group: {params['rfc_group']}")
    print(f"\tBits: {p.bit_length()}")
    print(f"\tDecimal digits: {len(str(p))}")
    print(f"\tGenerator: {params['g']}")

#########################################################################################
# Real parameters used in IKE protocol: https://www.rfc-editor.org/rfc/rfc3526.txt
#########################################################################################
DH_PARAMS = {
    
    "MODP-1536": {
        "bits": 1536,
        "p": generate_modp_prime(1536, 741804),
        "g": 2,
        "rfc_group": 5,
    },

    "MODP-2048": {
        "bits": 2048,
        "p": generate_modp_prime(2048, 124476),
        "g": 2,
        "rfc_group": 14,
    },

    "MODP-3072": {
        "bits": 3072,
        "p": generate_modp_prime(3072, 1690314),
        "g": 2,
        "rfc_group": 15,
    },

    "MODP-4096": {
        "bits": 4096,
        "p": generate_modp_prime(4096, 240904),
        "g": 2,
        "rfc_group": 16,
    },

    "MODP-6144": {
        "bits": 6144,
        "p": generate_modp_prime(6144, 929484),
        "g": 2,
        "rfc_group": 17,
    },

    "MODP-8192": {
        "bits": 8192,
        "p": generate_modp_prime(8192, 4743158),
        "g": 2,
        "rfc_group": 18,
    },

}