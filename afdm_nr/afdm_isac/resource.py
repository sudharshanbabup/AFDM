"""
Resource-selection results: collision probability (Proposition 2, eq. 14-15),
its Monte-Carlo validation, the p_d sensitivity table, and the three-way PRR
comparison.
"""

import numpy as np
from scipy.special import erfc
from . import params as P
from . import links


# ------------------------------------------- analytical collision (eq. 14,15)
def collision_ofdm(K, NR=P.NR):
    return 1.0 - (1.0 - 1.0 / NR) ** (K - 1)


def collision_afdm_rd(K, NR=P.NR, pd=P.PD):
    return 1.0 - (1.0 - (1.0 - pd) / NR) ** (K - 1)


def reduction_percent(K, NR=P.NR, pd=P.PD):
    po = collision_ofdm(K, NR)
    pr = collision_afdm_rd(K, NR, pd)
    return 100.0 * (1.0 - pr / po)


# ------------------------------------------- Monte-Carlo validation
def collision_mc(K, NR=P.NR, pd=P.PD, trials=P.MC_COLL, rng=None, radar=False):
    """Empirical per-vehicle collision probability.

    OFDM-SPS (radar=False): each of K vehicles selects a slot uniformly; a
    vehicle collides if any other vehicle shares its slot.
    AFDM-RD  (radar=True): a neighbour is detected (and its slot avoided) with
    probability pd; only undetected neighbours can cause collisions.
    """
    rng = rng or np.random.default_rng(P.SEED)
    coll = 0
    for _ in range(trials):
        slots = rng.integers(0, NR, size=K)
        ego = slots[0]
        others = slots[1:]
        if radar:
            detected = rng.random(K - 1) < pd          # detected -> avoided
            others = others[~detected]
        coll += int(np.any(others == ego))
    return coll / trials


# ------------------------------------------- p_d sensitivity table (Table 2)
def pd_sensitivity_table(pd_list=(0.6, 0.75, 0.85, 0.95), K_list=(20, 35, 50)):
    return {pd: [reduction_percent(K, pd=pd) for K in K_list] for pd in pd_list}


# ------------------------------------------- PRR three-way (Fig. 10)
def _per_link(name, speed_kmh, snr_db=P.SE_SNR_DB, pkt_bits=256):
    """Packet error rate from the link BER at the operating SNR and speed.

    PRR is dominated by the velocity-dependent ICI ceiling (eq. 10) rather than
    flat-fading diversity, so we evaluate the BER at the mean channel gain
    (|H|^2 = 1) with the speed-dependent leakage ceiling. This reproduces the
    reported behaviour: OFDM-SPS is reliable at low speed and degrades sharply
    above 200 km/h, while AFDM stays reliable across the whole range.
    """
    if name == "OFDM":
        ici = links._ici(speed_kmh, links.ICI_REF_OFDM)
    else:  # AFDM (adaptive chirp keeps the leakage ceiling negligible, eq. 7)
        ici = links.XI_AFDM
    snr = 10 ** (snr_db / 10.0)
    sinr_eff = snr / (1.0 + ici * snr)
    ber = 0.5 * erfc(np.sqrt(sinr_eff) / np.sqrt(2.0))
    return 1.0 - (1.0 - ber) ** pkt_bits


def prr_curves(speeds=P.SPEEDS_KMH, K=10, snr_db=P.SE_SNR_DB):
    """PRR = (1 - collision) * (1 - PER_link) for the three strategies."""
    coll_sps = collision_ofdm(K)                 # SPS (no radar) shared by both SPS schemes
    coll_rd = collision_afdm_rd(K)               # radar-aided
    out = {"OFDM-SPS": [], "AFDM-SPS": [], "AFDM-RD": []}
    for v in speeds:
        per_o = _per_link("OFDM", v, snr_db)
        per_a = _per_link("AFDM", v, snr_db)
        out["OFDM-SPS"].append((1 - coll_sps) * (1 - per_o))
        out["AFDM-SPS"].append((1 - coll_sps) * (1 - per_a))
        out["AFDM-RD"].append((1 - coll_rd) * (1 - per_a))
    return {k: np.array(v) for k, v in out.items()}, K
