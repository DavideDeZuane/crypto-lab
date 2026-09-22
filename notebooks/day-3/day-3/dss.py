"""
dss_table.py

Modulo per la generazione e visualizzazione della tabella riepilogativa
degli schemi di firma digitale (DSS - Digital Signature Scheme) disponibili
tramite liboqs.

Uso:
    from dss_table import print_dss_table
    print_dss_table()
"""

import oqs
import pandas as pd
from IPython.display import display


def _dss_summary(name):
    """Restituisce un dizionario con i dettagli di un singolo schema di firma."""
    sig = oqs.Signature(name)
    details = sig.details
    return {
        "Algorithm": name,
        "NIST Level": details.get("claimed_nist_level"),
        "Public key (bytes)": details.get("length_public_key"),
        "Secret key (bytes)": details.get("length_secret_key"),
        "Signature (bytes)": details.get("length_signature"),
    }


def _build_dss_dataframe(dss_names):
    """Costruisce il DataFrame filtrando solo gli algoritmi effettivamente abilitati."""
    sig_algorithms = oqs.get_enabled_sig_mechanisms()
    data = [
        _dss_summary(name)
        for name in dss_names
        if name in sig_algorithms
    ]
    return pd.DataFrame(data)


def _style_dss_dataframe(df_dss):
    """Applica lo stile (formattazione numerica, allineamento) al DataFrame."""
    return (
        df_dss.style
        .format({
            "Public key (bytes)": "{:,}",
            "Secret key (bytes)": "{:,}",
            "Signature (bytes)": "{:,}",
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
                "Signature (bytes)",
            ],
            **{"text-align": "right"}
        )
        .hide(axis="index")
    )


def print_dss_table():
    """
    Genera e visualizza la tabella riepilogativa degli schemi di firma
    digitale disponibili.

    Stampa un'intestazione, quindi mostra (via IPython.display.display)
    la tabella stilizzata con i parametri di ciascun algoritmo abilitato.
    """
    dss_names = [
        # ML-DSA
        "ML-DSA-44",
        "ML-DSA-65",
        "ML-DSA-87",
        # MAYO
        "MAYO-1",
        "MAYO-2",
        "MAYO-3",
        "MAYO-5",
        "SLH_DSA_PURE_SHA2_128S",
        "SLH_DSA_PURE_SHA2_192S",
        "SLH_DSA_PURE_SHA2_256S",
        "cross-rsdp-128-balanced",
        "cross-rsdp-192-balanced",
        "cross-rsdp-256-balanced",
        # Falcon
        "Falcon-512",
        "Falcon-1024",
        # SPHINCS+ (se disponibile nella tua versione di liboqs)
        "SPHINCS+-SHA2-128s-simple",
        "SPHINCS+-SHA2-128f-simple",
        "SPHINCS+-SHA2-192s-simple",
        "SPHINCS+-SHA2-192f-simple",
        "SPHINCS+-SHA2-256s-simple",
        "SPHINCS+-SHA2-256f-simple",
    ]

    df_dss = _build_dss_dataframe(dss_names)
    styled_df = _style_dss_dataframe(df_dss)

    print("=" * 100)
    print(" AVAILABLE DIGITAL SIGNATURE SCHEMES")
    print("=" * 100)
    display(styled_df)


if __name__ == "__main__":
    print_dss_table()