"""Fig. 6 -- Spectral efficiency vs velocity at SNR = 20 dB.

AFDM declines gently 6.1 -> 5.7 bps/Hz (retains >93%); OFDM retains ~37%;
OTFS (conv. MMSE) retains ~65%.  SE = log2(1 + SINR), eq. (10).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from afdm_isac import params as P, links
from afdm_isac import plotstyle as ps


def main(outfile="results/fig6_se_vs_velocity.png"):
    ps.apply()
    v = P.SPEEDS_KMH
    series = [("AFDM", ps.AFDM), ("OFDM", ps.OFDM), ("OTFS (conv. MMSE)", ps.OTFS)]
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, st in series:
        se = links.spectral_efficiency(name, v)
        ax.plot(v, se, color=st["color"], ls=st["ls"], marker=st["marker"], label=name)
    ax.set_xlabel("Vehicle Speed (km/h)")
    ax.set_ylabel("Spectral Efficiency (bps/Hz)")
    ax.set_xlim(30, 500)
    ax.set_ylim(1.5, 6.5)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile)


if __name__ == "__main__":
    main()
