"""Fig. 4 -- PAPR CCDF for N=128 QPSK subcarriers.

Genuine waveform-level simulation: build many AFDM / OFDM / OTFS time-domain
blocks from random QPSK symbols and measure the (oversampled) PAPR. AFDM and
OFDM coincide because the DAFT chirp is a unit-modulus rotation; OTFS is similar.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from afdm_isac import params as P, waveforms as wf
from afdm_isac import plotstyle as ps


def main(outfile="results/fig4_papr_ccdf.png", n_blocks=4000):
    ps.apply()
    rng = np.random.default_rng(P.SEED)
    nu_max = P.speed_to_doppler_norm(200)
    c1 = P.optimal_chirp(nu_max)
    M, Nd = 16, 8  # OTFS grid, M*Nd = 128

    papr = {"AFDM": [], "OFDM": [], "OTFS": []}
    for _ in range(n_blocks):
        bits = rng.integers(0, 2, 2 * P.N)
        x = wf.qpsk_mod(bits)
        papr["AFDM"].append(wf.papr_db(wf.afdm_mod(x, c1)))
        papr["OFDM"].append(wf.papr_db(wf.ofdm_mod(x)))
        Xdd = x.reshape(M, Nd, order="F")
        papr["OTFS"].append(wf.papr_db(wf.otfs_mod(Xdd, M, Nd)))

    grid = np.linspace(2, 12, 200)
    styles = {"AFDM": ps.AFDM, "OFDM": ps.OFDM, "OTFS": ps.OTFS}
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, st in styles.items():
        vals = np.sort(np.array(papr[name]))
        ccdf = 1.0 - np.searchsorted(vals, grid) / vals.size
        ax.semilogy(grid, np.clip(ccdf, 1e-4, 1), color=st["color"], ls=st["ls"], label=name)
    ax.set_xlabel("PAPR$_0$ (dB)")
    ax.set_ylabel(r"CCDF  $\Pr(\mathrm{PAPR} > \mathrm{PAPR}_0)$")
    ax.set_ylim(1e-4, 1)
    ax.set_xlim(4, 12)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile)


if __name__ == "__main__":
    main()
