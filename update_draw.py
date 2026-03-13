import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys

# ── 1. Load data from generated file ───────────────────────────────────────────
if len(sys.argv) < 2:
    print("Usage: python draw_heat_map.py <partition_counts.py>")
    sys.exit(1)

# 執行外部檔案並讀取 data 變數
exec(open(sys.argv[1]).read())   

# 確保 data 是 numpy array，方便後續的矩陣運算與切片
data_np = np.array(data)         
L_max = data_np.max()

columns_str = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
columns_num = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# ── 核心邏輯：找出誰是黑洞？ ────────────────────────────────────────────────────
# 我們計算每個分區在所有時間點的「大小總和」。
# 越早撞到 L_max 的分區，其總和越大。利用這個特性來做降冪排序。
sort_indices = np.argsort(data_np.sum(axis=1))[::-1]


# ── 圖表一：改造後的排序瀑布熱力圖 (Sorted Waterfall Heatmap) ────────────────────
sorted_matrix = data_np[sort_indices] / L_max

plt.figure(figsize=(12, 8))
sns.heatmap(sorted_matrix,
            cmap="YlOrRd",
            xticklabels=columns_str,
            yticklabels=False,   # 隱藏無意義的 Partition ID，避免畫面雜亂
            vmin=0, vmax=1,      
            cbar_kws={'label': 'Saturation Level (Current Size / L_max)'})

plt.title("Sorted Partition Saturation Heatmap (Fastest Saturating on Top)")
plt.xlabel("Streaming Progress (%)")
plt.ylabel("Partitions (Sorted by Saturation Speed)")
plt.tight_layout()

# 儲存第一張圖
out_path_heatmap = sys.argv[1].replace('.txt', '').replace('.py', '') + '_sorted_heatmap.png'
plt.savefig(out_path_heatmap, dpi=150)
print(f"Saved: {out_path_heatmap}")
plt.close()


# ── 圖表二：分叉軌跡折線圖 (Bifurcation Trajectory Plot) - 證明定理專用 ──────────
plt.figure(figsize=(10, 6))

# 1. 畫出前 3 名「瞬間暴衝的黑洞分區」
colors = ['#b30000', '#e34a33', '#fc8d59'] # 深紅到橘紅
for i in range(3):
    idx = sort_indices[i]
    plt.plot(columns_num, data_np[idx], marker='o', linewidth=2.5, color=colors[i],
             label=f'Blackhole (Original ID: {idx})')

# 2. 畫出 1 個「中位數分區 (正常增長)」
median_idx = sort_indices[len(sort_indices)//2]
plt.plot(columns_num, data_np[median_idx], marker='s', linestyle='--', color='gray',
         label=f'Median Partition (Original ID: {median_idx})')

# 3. 畫出 1 個「最慢的分區 (難民分區，撿別人剩下的)」
slowest_idx = sort_indices[-1]
plt.plot(columns_num, data_np[slowest_idx], marker='^', linestyle=':', color='green',
         label=f'Slowest Partition (Original ID: {slowest_idx})')

# 4. 畫出 L_max 天花板 (Capacity Limit)
plt.axhline(y=L_max, color='black', linestyle='-', alpha=0.5, 
            label=f'Capacity Limit (L_max = {L_max})')

plt.title("Dynamical Bifurcation: Partition Size Trajectories")
plt.xlabel("Streaming Progress (%)")
plt.ylabel("Partition Size (Nodes)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# 儲存第二張圖
out_path_trajectory = sys.argv[1].replace('.txt', '').replace('.py', '') + '_trajectory.png'
plt.savefig(out_path_trajectory, dpi=150)
print(f"Saved: {out_path_trajectory}")

# 一次展示出來
plt.show()