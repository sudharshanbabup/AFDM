"""
3GPP TDL-C (300 ns, reduced to L=6 taps) doubly-selective channel, eq. (2)-(3),
and construction of the effective DAFT-domain channel matrix H_eff, eq. (5).
"""

import numpy as np
from . import params as P


def draw_channel(speed_kmh, rng):
    """Draw one random channel realisation.

    Returns tap gains h_l ~ CN(0, sigma_l^2), integer delays tau_l (samples),
    and normalised Doppler shifts nu_l = nu_max cos(theta_l)   (eq. 2).
    """
    powers = P.tdlc_powers_linear()
    h = (rng.standard_normal(P.L) + 1j * rng.standard_normal(P.L)) * np.sqrt(powers / 2.0)
    tau = P.TDLC_DELAYS_SAMPLES.copy()
    nu_max = P.speed_to_doppler_norm(speed_kmh)
    theta = rng.uniform(0, 2 * np.pi, P.L)
    nu = nu_max * np.cos(theta)
    return h, tau, nu


def apply_channel(s, h, tau, nu, sigma_w, rng):
    """Apply the time-varying multipath channel (eq. 3) to a CP-extended block.

    s is the length-N transmit block; a cyclic prefix of NCP is added and later
    removed, so delays up to NCP are handled without inter-block interference.
    """
    N = s.size
    s_cp = np.concatenate([s[-P.NCP:], s])
    Ncp = s_cp.size
    y = np.zeros(Ncp, dtype=complex)
    n = np.arange(Ncp)
    for hl, tl, nl in zip(h, tau, nu):
        tl = int(round(tl))
        delayed = np.roll(s_cp, tl)
        doppler = np.exp(1j * 2 * np.pi * nl * n / N)
        y += hl * delayed * doppler
    w = (rng.standard_normal(Ncp) + 1j * rng.standard_normal(Ncp)) * (sigma_w / np.sqrt(2.0))
    y += w
    return y[P.NCP:]                       # remove CP


def effective_channel_matrix(h, tau, nu, c1):
    """Effective DAFT-domain channel matrix H_eff (realises eq. 5).

    Constructed directly from the implemented transmit -> channel -> receive
    chain so that it is exactly consistent with the AFDM IDAFT/DAFT pair:

        Y = H_eff @ x ,   H_eff[:,k] = DAFT( channel( IDAFT(e_k) ) )

    where e_k is the k-th unit DAFT symbol and the channel is noiseless. The
    diagonal entries give H_m and the off-diagonal entries give the residual
    inter-bin leakage xi_m that enter the post-MMSE SINR (eq. 10).
    """
    from . import waveforms as wf      # local import avoids any import cycle
    N = P.N
    zero_rng = np.random.default_rng(0)
    H = np.zeros((N, N), dtype=complex)
    for k in range(N):
        e = np.zeros(N, dtype=complex)
        e[k] = 1.0
        s = wf.afdm_mod(e, c1)
        y = apply_channel(s, h, tau, nu, 0.0, zero_rng)   # sigma_w = 0 -> noiseless
        H[:, k] = wf.afdm_demod(y, c1)
    return H
