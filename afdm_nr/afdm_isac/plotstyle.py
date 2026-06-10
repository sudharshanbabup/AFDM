"""Shared Matplotlib style so every figure has a consistent IEEE-like look."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def apply():
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "dejavuserif",
        "font.size": 13,
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.alpha": 0.5,
        "lines.linewidth": 2.0,
        "lines.markersize": 7,
        "legend.framealpha": 0.95,
        "figure.dpi": 150,
    })

# consistent colours/markers
AFDM = dict(color="tab:blue",  marker="o", ls="-")
OFDM = dict(color="tab:red",   marker="s", ls="--")
OTFS = dict(color="tab:green", marker="^", ls=":")
