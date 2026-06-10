"""Fig. 5 -- Channel-estimation NMSE vs SNR at 200 km/h.

AFDM with fractional-aware adaptive chirp reaches ~2e-3 at 30 dB; the
integer-only chirp variant floors near 5e-3; OFDM LS saturates near 1e-2.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from afdm_isac import params as P, links
from afdm_isac import plotstyle as ps


def main(outfile="results/fig5_nmse_vs_snr.png"):
    ps.apply()
    snr = P.SNR_DB
    series = [
        ("AFDM (adaptive chirp)", "AFDM", ps.AFDM),
        ("AFDM (integer chirp)", "AFDM-int", dict(color="tab:purple", marker="v", ls="-.")),
        ("OFDM (LS)", "OFDM", ps.OFDM),
    ]
    fig, ax = plt.subplots(figsize=(7, 5))
    for label, kind, st in series:
        nmse = links.nmse_curve(kind, snr)
        ax.semilogy(snr, nmse, color=st["color"], ls=st["ls"], marker=st["marker"], label=label)
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("Channel Estimation NMSE")
    ax.set_xlim(0, 30)
    ax.set_ylim(1e-3, 2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile)


if __name__ == "__main__":
    main()
