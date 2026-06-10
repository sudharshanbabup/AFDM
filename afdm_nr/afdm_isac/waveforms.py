"""
Waveform front-ends used in the paper.

* AFDM  (Affine Frequency Division Multiplexing) -- IDAFT / DAFT, eq. (1).
* OFDM  (CP-OFDM baseline).
* OTFS  (delay-Doppler baseline, M x Nd grid with ISFFT/SFFT).

The AFDM IDAFT/DAFT pair is implemented exactly as a chirp pre/de-multiplication
around an N-point (I)DFT, which is the operational definition behind eq. (1):

    IDAFT:  s[n] = (1/sqrt(N)) sum_m x_m e^{ j 2 pi m n / N } e^{ -j 2 pi c1 n^2 }
    DAFT :  Y_m = (1/sqrt(N)) sum_n y[n] e^{ +j 2 pi c1 n^2 } e^{ -j 2 pi m n / N }

so that DAFT(IDAFT(x)) = x in the absence of a channel.
"""

import numpy as np
from . import params as P


# ----------------------------------------------------------------- QPSK
def qpsk_mod(bits):
    b = bits.reshape(-1, 2)
    s = (1 - 2 * b[:, 0]) + 1j * (1 - 2 * b[:, 1])
    return s / np.sqrt(2.0)


def qpsk_demod(sym):
    b0 = (sym.real < 0).astype(int)
    b1 = (sym.imag < 0).astype(int)
    return np.column_stack([b0, b1]).reshape(-1)


# ----------------------------------------------------------------- AFDM
def afdm_chirp(N, c1):
    n = np.arange(N)
    return np.exp(-1j * 2 * np.pi * c1 * (n ** 2))


def afdm_mod(x, c1):
    """IDAFT of the symbol vector x (length N)."""
    N = x.size
    chirp = afdm_chirp(N, c1)
    # (1/sqrt(N)) sum_m x_m e^{j2pi m n/N} = sqrt(N) * ifft(x)
    base = np.sqrt(N) * np.fft.ifft(x)
    return base * chirp


def afdm_demod(y, c1):
    """DAFT of the received time-domain vector y (length N)."""
    N = y.size
    chirp = afdm_chirp(N, c1)
    return (1.0 / np.sqrt(N)) * np.fft.fft(y * np.conj(chirp))


# ----------------------------------------------------------------- OFDM
def ofdm_mod(x):
    N = x.size
    return np.sqrt(N) * np.fft.ifft(x)


def ofdm_demod(y):
    N = y.size
    return (1.0 / np.sqrt(N)) * np.fft.fft(y)


# ----------------------------------------------------------------- OTFS
def otfs_mod(X, M, Nd):
    """OTFS modulator. X is the M(delay) x Nd(Doppler) DD-domain symbol grid.

    ISFFT -> time-frequency, then Heisenberg transform -> time-domain vector
    of length M*Nd.
    """
    # ISFFT: FFT along Doppler, IFFT along delay
    Xtf = np.fft.fft(np.fft.ifft(X, axis=0), axis=1)        # M x Nd
    # Heisenberg (OFDM per column with M subcarriers)
    s = np.sqrt(M) * np.fft.ifft(Xtf, axis=0)               # M x Nd
    return s.reshape(-1, order="F")                          # serialise columns


def otfs_demod(r, M, Nd):
    Y = r.reshape(M, Nd, order="F")
    Ytf = (1.0 / np.sqrt(M)) * np.fft.fft(Y, axis=0)        # Wigner
    Xdd = np.fft.ifft(np.fft.fft(Ytf, axis=0), axis=1)      # SFFT
    return Xdd


# ----------------------------------------------------------------- PAPR
def papr_db(time_signal, oversample=4):
    """Peak-to-average power ratio of a time-domain block, in dB.

    Zero-padding in frequency provides oversampling so that the continuous-time
    peak is well approximated.
    """
    N = time_signal.size
    Sf = np.fft.fft(time_signal)
    Sf_os = np.zeros(N * oversample, dtype=complex)
    Sf_os[:N // 2] = Sf[:N // 2]
    Sf_os[-(N // 2):] = Sf[-(N // 2):]
    s_os = np.fft.ifft(Sf_os) * oversample
    p = np.abs(s_os) ** 2
    return 10 * np.log10(p.max() / p.mean())
