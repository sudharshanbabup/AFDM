"""Regenerate every figure and table in the paper.

Usage:
    python run_all.py            # all figures + table
Outputs are written to results/.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.makedirs("results", exist_ok=True)

from experiments import (fig3_ber_vs_snr, fig4_papr_ccdf, fig5_nmse_vs_snr,
                         fig6_se_vs_velocity, fig7_sensing_rmse, fig8_ablation,
                         fig9_collision, fig10_prr, table2_pd_sensitivity)

STEPS = [
    ("Fig. 3  BER vs SNR",            fig3_ber_vs_snr.main),
    ("Fig. 4  PAPR CCDF",             fig4_papr_ccdf.main),
    ("Fig. 5  NMSE vs SNR",           fig5_nmse_vs_snr.main),
    ("Fig. 6  SE vs velocity",        fig6_se_vs_velocity.main),
    ("Fig. 7  Sensing RMSE + CRB",    fig7_sensing_rmse.main),
    ("Fig. 8  Ablation @500 km/h",    fig8_ablation.main),
    ("Fig. 9  Collision probability", fig9_collision.main),
    ("Fig. 10 PRR three-way",         fig10_prr.main),
    ("Table 2 p_d sensitivity",       table2_pd_sensitivity.main),
]

if __name__ == "__main__":
    t0 = time.time()
    for label, fn in STEPS:
        print(f"\n=== {label} ===")
        fn()
    print(f"\nAll results regenerated in {time.time()-t0:.1f}s -> results/")
