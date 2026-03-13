import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys

# ── Load data from generated file ──────────────────────────────────────────────
if len(sys.argv) < 2:
    print("Usage: python draw_heat_map.py <partition_counts.py>")
    sys.exit(1)

exec(open(sys.argv[1]).read())   # defines `data`

columns = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
L_max = data.max()               # or replace with a fixed value, e.g. 101866

# ── Normalise to saturation 0~1 ────────────────────────────────────────────────
saturation_matrix = data / L_max

# ── Plot ───────────────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 8))
sns.heatmap(saturation_matrix,
            cmap="YlOrRd",
            xticklabels=columns,
            yticklabels=50,
            vmin=0, vmax=1,      # fix scale so 1.0 = fully saturated
            cbar_kws={'label': 'Saturation Level (Current Size / L_max)'})

plt.title("Partition Saturation Heatmap")
plt.xlabel("Streaming Progress (%)")
plt.ylabel("Partition ID")
plt.tight_layout()

out_path = sys.argv[1].replace('.py', '_heatmap.png')
plt.savefig(out_path, dpi=150)
print(f"Saved: {out_path}")
plt.show()