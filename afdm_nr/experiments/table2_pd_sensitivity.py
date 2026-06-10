"""Table 2 -- Analytical collision-probability reduction (%) versus radar
detection probability p_d and vehicle density K (eq. 14-15, N_R = 50).

Prints the table and writes it to results/table2_pd_sensitivity.csv.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csv
from afdm_isac import resource as R


def main(outfile="results/table2_pd_sensitivity.csv"):
    pd_list = (0.6, 0.75, 0.85, 0.95)
    K_list = (20, 35, 50)
    table = R.pd_sensitivity_table(pd_list, K_list)

    header = ["p_d"] + [f"K={k}" for k in K_list]
    print("  ".join(f"{h:>8}" for h in header))
    rows = []
    for pd in pd_list:
        vals = table[pd]
        rows.append([pd] + [round(x, 1) for x in vals])
        print("  ".join([f"{pd:>8.2f}"] + [f"{x:>8.1f}" for x in vals]))

    with open(outfile, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("saved", outfile)


if __name__ == "__main__":
    main()
