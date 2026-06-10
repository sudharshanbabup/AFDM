"""Fig. 9 -- Collision probability vs number of vehicles.

Analytical curves (eq. 14-15, dashed) with Monte-Carlo markers. The annotation
reports the reduction range over the operating points (78-82%), consistent with
the text.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from afdm_isac import params as P, resource as R
from afdm_isac import plotstyle as ps


def main(outfile="results/fig9_collision.png"):
    ps.apply()
    rng = np.random.default_rng(P.SEED)
    K = np.arange(5, 51)
    Km = P.K_VEHICLES

    p_o = R.collision_ofdm(K)
    p_r = R.collision_afdm_rd(K)
    mc_o = [R.collision_mc(int(k), trials=P.MC_COLL, rng=rng, radar=False) for k in Km]
    mc_r = [R.collision_mc(int(k), trials=P.MC_COLL, rng=rng, radar=True) for k in Km]

    fig, ax = plt.subplots(figsize=(7.5, 6))
    ax.plot(K, p_o, "--", color="red", label="OFDM-SPS (analytical)")
    ax.plot(Km, mc_o, "s", mfc="none", mec="red", mew=2, label="OFDM-SPS (simulation)")
    ax.plot(K, p_r, "--", color="blue", label="AFDM-RD (analytical)")
    ax.plot(Km, mc_r, "o", mfc="none", mec="blue", mew=2, label="AFDM-RD (simulation)")

    ax.annotate("78\u201382% reduction", xy=(30, 0.27), xytext=(29.5, 0.55),
                fontsize=14, color="dimgray",
                arrowprops=dict(arrowstyle="->", color="gray", lw=1.6))
    ax.set_xlabel("Number of Vehicles ($K$)")
    ax.set_ylabel("Collision Probability")
    ax.set_xlim(5, 50); ax.set_ylim(0, 1)
    ax.legend(loc="upper left", fontsize=11)
    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile, "| reduction over K=5..50:",
          f"{R.reduction_percent(np.array([50])).item():.1f}%..{R.reduction_percent(np.array([5])).item():.1f}%")


if __name__ == "__main__":
    main()
