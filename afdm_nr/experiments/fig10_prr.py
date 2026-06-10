"""Fig. 10 -- Packet Reception Ratio vs vehicle speed at SNR = 20 dB.

OFDM-SPS degrades sharply above 200 km/h (ICI-limited link); AFDM-SPS and
AFDM-RD maintain high PRR, with AFDM-RD highest thanks to radar-aided
collision avoidance.  PRR = (1 - P_collision) * (1 - PER_link).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from afdm_isac import params as P, resource as R
from afdm_isac import plotstyle as ps


def main(outfile="results/fig10_prr.png"):
    ps.apply()
    curves, K = R.prr_curves()
    v = P.SPEEDS_KMH
    styles = {
        "OFDM-SPS": dict(color="tab:red", marker="s", ls="--"),
        "AFDM-SPS": dict(color="tab:orange", marker="^", ls="-."),
        "AFDM-RD": dict(color="tab:blue", marker="o", ls="-"),
    }
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for name, st in styles.items():
        ax.plot(v, curves[name], **st, label=name)
    ax.set_xlabel("Vehicle Speed (km/h)")
    ax.set_ylabel("Packet Reception Ratio (PRR)")
    ax.set_xlim(30, 500); ax.set_ylim(0, 1)
    ax.legend()
    ax.set_title(f"$K={K}$ vehicles, $N_R={P.NR}$, SNR $=20$ dB")
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile)


if __name__ == "__main__":
    main()
