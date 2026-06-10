"""Fig. 3 -- BER vs SNR under TDL-C at 60, 200, and 500 km/h.

AFDM (blue), OFDM (red, ICI floor), OTFS (green, baseline DD-MMSE).
Shaded bands: 95% confidence interval over MC_BER realisations.
Curves are PCHIP-interpolated (monotone).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from afdm_isac import params as P, links
from afdm_isac import plotstyle as ps


def main(outfile="results/fig3_ber_vs_snr.png"):
    ps.apply()
    rng = np.random.default_rng(P.SEED)
    snr = P.SNR_DB
    snr_fine = np.linspace(snr.min(), snr.max(), 300)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
    styles = {"AFDM": ps.AFDM, "OFDM": ps.OFDM, "OTFS": ps.OTFS}

    for ax, v in zip(axes, P.BER_SPEEDS):
        for name, st in styles.items():
            ber, ci = links.ber_waveform(name, v, snr, P.MC_BER, rng)
            ber = np.clip(ber, 1e-6, 1)
            f = PchipInterpolator(snr, np.log10(ber))
            ax.semilogy(snr_fine, 10 ** f(snr_fine), color=st["color"], ls=st["ls"], label=name)
            ax.semilogy(snr, ber, color=st["color"], marker=st["marker"], ls="none")
            lo = np.clip(ber - ci, 1e-7, 1); hi = np.clip(ber + ci, 1e-7, 1)
            ax.fill_between(snr, lo, hi, color=st["color"], alpha=0.18)
        ax.set_title(f"{v} km/h")
        ax.set_xlabel("SNR (dB)")
        ax.set_ylim(1e-5, 1)
        ax.set_xlim(0, 30)
    axes[0].set_ylabel("Bit Error Rate")
    axes[0].legend(loc="lower left", fontsize=11)
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile)


if __name__ == "__main__":
    main()
