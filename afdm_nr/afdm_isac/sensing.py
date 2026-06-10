"""
AFDM-ISAC sensing: delay-Doppler estimation via the periodogram (eq. 11) and
the Cramer-Rao bounds for range and velocity (eq. 12-13).
"""

import numpy as np
from . import params as P


# ----------------------------------------------------------- CRB (eq. 12,13)
def crb_range(snr_lin):
    return 3 * P.C ** 2 / (8 * np.pi ** 2 * P.B ** 2 * snr_lin * (P.N ** 2 - 1))


def crb_velocity(snr_lin):
    return 3 * P.C ** 2 * P.DF ** 2 / (32 * np.pi ** 2 * P.FC ** 2 * snr_lin * (P.N ** 2 - 1))


# ----------------------------------------------------------- echo + estimator
def make_echo(R, v, snr_lin, Nsym, c1, rng):
    """Generate a frame of Nsym AFDM echo symbols from one target.

    Fast time (within a symbol) carries delay; slow time (across symbols) carries
    Doppler, which is what lets AFDM-ISAC resolve velocity from the frame.
    """
    tau = 2 * R / P.C / P.TS               # round-trip delay in samples
    fd = 2 * v * P.FC / P.C                # round-trip Doppler [Hz]
    m = np.arange(P.N)
    p = np.arange(Nsym)
    # phase: fast-time delay term + slow-time Doppler term + chirp term
    delay_ph = np.exp(-1j * 2 * np.pi * m[None, :] * tau / P.N)
    dopp_ph = np.exp(1j * 2 * np.pi * fd * (p[:, None] * (P.N + P.NCP) * P.TS))
    chirp_ph = np.exp(1j * 2 * np.pi * c1 * tau ** 2)
    Y = delay_ph * dopp_ph * chirp_ph
    noise = (rng.standard_normal(Y.shape) + 1j * rng.standard_normal(Y.shape)) / np.sqrt(2.0)
    return Y / np.sqrt(snr_lin) ** 0 + noise / np.sqrt(snr_lin)


def _parab(ym1, y0, yp1):
    """3-point parabolic peak offset (sub-grid refinement)."""
    denom = ym1 - 2 * y0 + yp1
    return 0.0 if denom == 0 else 0.5 * (ym1 - yp1) / denom


def estimate_range_velocity(Y, c1, Rgrid, vgrid):
    """2-D periodogram peak search (eq. 11) with parabolic sub-grid refinement.

    Vectorised: build delay and Doppler steering matrices and evaluate the whole
    ambiguity surface with two matrix products, then refine the peak to sub-grid
    accuracy so the estimator can approach the Cramer-Rao bound at high SNR.
    """
    Nsym, N = Y.shape
    m = np.arange(N)
    p = np.arange(Nsym)
    tau = 2 * Rgrid / P.C / P.TS                       # (nR,)
    A = np.exp(1j * 2 * np.pi * np.outer(tau, m) / N)  # (nR, N) matched delay
    fd = 2 * vgrid * P.FC / P.C                        # (nv,)
    Bm = np.exp(-1j * 2 * np.pi * np.outer(fd, p) * (N + P.NCP) * P.TS)  # (nv, Nsym)
    Sm = A @ Y.T                                       # (nR, Nsym)
    surf = np.abs(Sm @ Bm.T) ** 2                      # (nR, nv)
    iR, iv = np.unravel_index(np.argmax(surf), surf.shape)
    Rhat, vhat = Rgrid[iR], vgrid[iv]
    if 0 < iR < len(Rgrid) - 1:
        Rhat += _parab(surf[iR - 1, iv], surf[iR, iv], surf[iR + 1, iv]) * (Rgrid[1] - Rgrid[0])
    if 0 < iv < len(vgrid) - 1:
        vhat += _parab(surf[iR, iv - 1], surf[iR, iv], surf[iR, iv + 1]) * (vgrid[1] - vgrid[0])
    return Rhat, vhat
