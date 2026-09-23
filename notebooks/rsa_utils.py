
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


def inverso_moltiplicativo(a, p):
    old_r, r = a, p
    old_x, x = 1, 0
    # old_y, y = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        #old_y, y = y, old_y - q * y

    if old_r != 1:
        raise ValueError(f"L'inverso non esiste: gcd({a}, {p}) = {old_r} != 1")

    return old_x % p



def verifica_firma(public_key, message, signature, titolo="Verifica"):
    """
    Verifica una firma RSA-PSS/SHA256 e stampa messaggio, firma ed esito
    in modo leggibile.

    Parametri:
        public_key : chiave pubblica RSA da usare per la verifica
        message    : bytes del messaggio
        signature  : bytes della firma da verificare
        titolo     : etichetta da stampare per identificare il caso
    """
    print()
    print("=" * 100)
    print(f"{titolo}")
    print("-" * 100)
    print(f"Messaggio : {message}")
    print(f"Firma     : {signature.hex()[:60]}...{signature.hex()[-20:]}")

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("Risultato : ✅ Firma VALIDA")
    except InvalidSignature:
        print("Risultato : ❌ Firma NON valida")
    print("=" * 100)


