"""
Central simulation parameters for

  "AFDM-Based Integrated Sensing and Communication for Asynchronous
   NR-V2X Mode 2 Sidelink with Fractional Doppler Compensation"

All values are taken directly from Table 3 (Simulation Parameters) of the
manuscript. Keeping every constant in one place guarantees that every figure
script uses identical settings.
"""

import numpy as np

# ---------------------------------------------------------------- physical
FC      = 5.9e9        # carrier frequency  f_c  [Hz]
B       = 10e6         # bandwidth          B    [Hz]
N       = 128          # number of subcarriers / DAFT bins
DF      = B / N        # subcarrier spacing  Delta f = B/N = 78.125 kHz
NCP     = 32           # cyclic-prefix length [samples]
TS      = 1.0 / B      # sample period [s]
C       = 3e8          # speed of light [m/s]
LAMBDA  = C / FC       # wavelength [m]

# ---------------------------------------------------------------- channel
L       = 6            # number of resolvable taps (3GPP TDL-C 300 ns, reduced)
# 3GPP TDL-C-like reduced profile (normalised so sum(power)=1).
# Delays in samples (Ts=100 ns) span the 300 ns rms / ~ up to ~0.7 us range.
TDLC_DELAYS_SAMPLES = np.array([0, 1, 2, 3, 4, 6], dtype=float)
TDLC_POWERS_DB      = np.array([0.0, -2.2, -4.0, -6.0, -8.2, -10.0])

# ---------------------------------------------------------------- modulation
MOD          = "QPSK"   # uncoded
BITS_PER_SYM = 2

# ---------------------------------------------------------------- sweeps
SNR_DB      = np.arange(0, 31, 2.5)         # 0 .. 30 dB
SPEEDS_KMH  = np.array([30, 60, 100, 150, 200, 250, 300, 350, 400, 450, 500])
BER_SPEEDS  = np.array([60, 200, 500])      # Fig. 3 velocities
SE_SNR_DB   = 20.0                           # Fig. 6 / Fig. 10 operating SNR

# ---------------------------------------------------------------- resource grid
NR          = 50        # SPS candidate resources  N_R
K_VEHICLES  = np.arange(5, 51, 5)            # 5 .. 50 vehicles
PD          = 0.85      # radar detection probability  p_d

# ---------------------------------------------------------------- Monte Carlo
MC_BER      = 10_000    # trials for BER / NMSE
MC_COLL     = 5_000     # trials for collision / PRR
SEED        = 2024

# ---------------------------------------------------------------- helpers
def speed_to_doppler_norm(speed_kmh, two_way=False):
    """Normalised maximum Doppler nu = v f_c /(c Delta f) (eq. 2).

    two_way=True returns the round-trip (sensing) normalisation used in
    the optimal-chirp expression (eq. 9).
    """
    v = speed_kmh / 3.6                       # m/s
    factor = 2.0 if two_way else 1.0
    return factor * v * FC / (C * DF)

def optimal_chirp(nu_max):
    """Diversity-optimal chirp parameter c1* (eq. 9)."""
    return (1.0 / (2.0 * N)) * (1.0 + 1.0 / (2.0 * nu_max + 1.0))

def tdlc_powers_linear():
    p = 10.0 ** (TDLC_POWERS_DB / 10.0)
    return p / p.sum()
