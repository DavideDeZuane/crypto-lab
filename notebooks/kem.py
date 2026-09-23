
import oqs as oqs
import pandas as pd
from IPython.display import display
 
 
def _kem_summary(name):
    """Restituisce un dizionario con i dettagli di un singolo algoritmo KEM."""
    kem = oqs.KeyEncapsulation(name)
    details = kem.details
    return {
        "Algorithm": name,
        "NIST Level": details.get("claimed_nist_level"),
        "Public key (bytes)": details.get("length_public_key"),
        "Secret key (bytes)": details.get("length_secret_key"),
        "Ciphertext (bytes)": details.get("length_ciphertext"),
        "Shared secret (bytes)": details.get("length_shared_secret"),
    }
 
 
def _build_kem_dataframe(kem_names):
    """Costruisce il DataFrame filtrando solo gli algoritmi effettivamente abilitati."""
    kem_algorithms = oqs.get_enabled_kem_mechanisms()
    data = [
        _kem_summary(name)
        for name in kem_names
        if name in kem_algorithms
    ]
    return pd.DataFrame(data)
 
 
def _style_kem_dataframe(df_kem):
    """Applica lo stile (formattazione numerica, allineamento) al DataFrame."""
    return (
        df_kem.style
        .format({
            "Public key (bytes)": "{:,}",
            "Secret key (bytes)": "{:,}",
            "Ciphertext (bytes)": "{:,}",
            "Shared secret (bytes)": "{:,}",
        })
        .set_properties(
            subset=["Algorithm"],
            **{"text-align": "left"}
        )
        .set_properties(
            subset=[
                "NIST Level",
                "Public key (bytes)",
                "Secret key (bytes)",
                "Ciphertext (bytes)",
                "Shared secret (bytes)",
            ],
            **{"text-align": "right"}
        )
        .hide(axis="index")
    )
 
 
def print_kem_table():
    """
    Genera e visualizza la tabella riepilogativa dei KEM disponibili.
 
    Stampa un'intestazione, quindi mostra (via IPython.display.display)
    la tabella stilizzata con i parametri di ciascun algoritmo abilitato.
    """
    kem_names = [
        "ML-KEM-512",
        "ML-KEM-768",
        "ML-KEM-1024",
        "BIKE-L1",
        "BIKE-L3",
        "BIKE-L5",
        "HQC-1",
        "HQC-3",
        "HQC-5",
        "FrodoKEM-640-AES",
        "FrodoKEM-976-AES",
        "FrodoKEM-1344-AES",
        "sntrup761",
        "Classic-McEliece-348864",
        "Classic-McEliece-460896",
        "Classic-McEliece-6688128",
        "Classic-McEliece-6960119",
        "Classic-McEliece-8192128",
    ]
 
    df_kem = _build_kem_dataframe(kem_names)
    styled_df = _style_kem_dataframe(df_kem)
 
    print("=" * 100)
    print(" AVAILABLE KEMS")
    print("=" * 100)
    display(styled_df)
 
 
if __name__ == "__main__":
    print_kem_table()