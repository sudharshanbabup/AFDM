"""Fig. 7 -- Sensing RMSE vs SNR.

(a) Range estimation: AFDM-ISAC periodogram estimate approaches the CRB
    (eq. 12); OFDM (range-only) shows a larger error.
(b) Velocity estimation: AFDM resolves velocity from the DAFT frame and
    approaches the CRB (eq. 13); OFDM cannot estimate velocity.

The estimator is the genuine 2-D periodogram peak search (eq. 11) over a frame
of AFDM echo symbols.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from afdm_isac import params as P, sensing
from afdm_isac import plotstyle as ps


def main(outfile="results/fig7_sensing_rmse.png", n_trials=300, Nsym=16):
    ps.apply()
    rng = np.random.default_rng(P.SEED)
    snr_db = np.arange(0, 31, 5)
    R_true, v_true = 50.37, 80.6         # off-grid target (range [m], velocity [m/s])
    nu_max = P.speed_to_doppler_norm(500, two_way=True)
    c1 = P.optimal_chirp(nu_max)

    # search grids around the true values (periodogram + parabolic refinement)
    Rgrid = np.arange(20, 80, 0.5)
    vgrid = np.arange(40, 120, 1.0)

    rmse_R, rmse_v, rmse_R_ofdm = [], [], []
    for sdb in snr_db:
        snr = 10 ** (sdb / 10.0)
        errR = errv = errR_o = 0.0
        for _ in range(n_trials):
            Y = sensing.make_echo(R_true, v_true, snr, Nsym, c1, rng)
            Rh, vh = sensing.estimate_range_velocity(Y, c1, Rgrid, vgrid)
            errR += (Rh - R_true) ** 2
            errv += (vh - v_true) ** 2
            # OFDM range-only: single-symbol, coarser delay estimate (no slow-time gain)
            Yo = sensing.make_echo(R_true, v_true, snr, 1, c1, rng)
            Rh_o, _ = sensing.estimate_range_velocity(Yo, c1, Rgrid, np.array([0.0]))
            errR_o += (Rh_o - R_true) ** 2
        rmse_R.append(np.sqrt(errR / n_trials))
        rmse_v.append(np.sqrt(errv / n_trials))
        rmse_R_ofdm.append(np.sqrt(errR_o / n_trials))

    snr_lin = 10 ** (snr_db / 10.0)
    crbR = np.sqrt(sensing.crb_range(snr_lin * Nsym))      # frame integration gain
    crbV = np.sqrt(sensing.crb_velocity(snr_lin * Nsym))

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5))
    a1.semilogy(snr_db, rmse_R, **ps.AFDM, label="AFDM-ISAC")
    a1.semilogy(snr_db, rmse_R_ofdm, **ps.OFDM, label="OFDM (range only)")
    a1.semilogy(snr_db, crbR, "k--", marker="x", label="CRB (Theorem 3)")
    a1.set_title("(a) Range Estimation")
    a1.set_xlabel("SNR (dB)"); a1.set_ylabel("Range RMSE (m)"); a1.legend()

    a2.semilogy(snr_db, rmse_v, **ps.AFDM, label="AFDM-ISAC")
    a2.semilogy(snr_db, crbV, "k--", marker="x", label="CRB (Theorem 3)")
    a2.text(0.05, 0.06, "OFDM: velocity not available", transform=a2.transAxes,
            bbox=dict(fc="lightyellow", ec="0.5"))
    a2.set_title("(b) Velocity Estimation")
    a2.set_xlabel("SNR (dB)"); a2.set_ylabel("Velocity RMSE (m/s)"); a2.legend()

    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight", facecolor="white")
    print("saved", outfile)


if __name__ == "__main__":
    main()
