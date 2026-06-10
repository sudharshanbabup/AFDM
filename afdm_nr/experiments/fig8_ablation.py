"""Fig. 8 -- Ablation study at 500 km/h under TDL-C.

Each curve removes one AFDM component to isolate the contribution of adaptive
chirp selection and fractional-Doppler compensation. 95% CI bands shown.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from afdm_isac import params as P, links
from afdm_isac import plotstyle as ps


def main(outfile="results/fig8_ablation.png"):
    ps.apply()
    rng = np.random.default_rng(P.SEED)
    snr = P.SNR_DB
    snr_fine = np.linspace(0, 30, 300)
    variants = [
        ("AFDM (full: adaptive + frac.)", dict(color="tab:blue", marker="o", ls="-")),
        ("AFDM (no frac. comp.)", dict(color="tab:green", marker="D", ls="--")),
        ("AFDM (integer chirp only)", dict(color="tab:purple", marker="v", ls="-.")),
        ("OFDM baseline", dict(color="tab:red", marker="s", ls=":")),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for name, st in variants:
        ber, ci = links.ber_ablation(name, 500, snr, P.MC_BER, rng)
        ber = np.clip(ber, 1e-6, 1)
        f = PchipInterpolator(snr, np.log10(ber))
        ax.semilogy(snr_fine, 10 ** f(snr_fine), color=st["color"], ls=st["ls"], label=name)
        ax.semilogy(snr, ber, color=st["color"], marker=st["marker"], ls="none")
        lo = np.clip(ber - ci, 1e-7, 1); hi = np.clip(ber + ci, 1e-7, 1)
        ax.fill_between(snr, lo, hi, color=st["color"], alpha=0.15)
    ax.set_xlabel("SNR (dB)"); ax.set_ylabel("Bit Error Rate")
    ax.set_xlim(0, 30); ax.set_ylim(1e-5, 1)
    ax.legend(fontsize=10, loc="lower left")
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile)


if __name__ == "__main__":
    main()
