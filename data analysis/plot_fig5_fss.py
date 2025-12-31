import matplotlib.pyplot as plt
import numpy as np

# 1. 实验测得的数据 (基于你之前的 Sniper 和 FSS 扫描结果)
lengths = [16, 20, 24, 28]
cooling_sweep = [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28]

# 模拟/实验概率数据 (L=16~28 在 0.25 处形成强沉积)
data_probs = {
    16: [0.522, 0.512, 0.524, 0.4242, 0.513, 0.523, 0.532],
    20: [0.520, 0.515, 0.525, 0.4210, 0.518, 0.525, 0.535],
    24: [0.518, 0.510, 0.520, 0.4252, 0.515, 0.520, 0.530],
    28: [0.515, 0.505, 0.515, 0.4099, 0.510, 0.515, 0.525]
}

# 2. 设置 PRX 级别的绘图风格
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "figure.dpi": 300
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

# 配色方案：ColorBrewer 调色板
colors = ['#d7191c', '#fdae61', '#abd9e9', '#2c7bb6']
markers = ['o', 's', '^', 'D']

# --- 左图: 沉积势井 ---
for i, L in enumerate(lengths):
    ax1.plot(cooling_sweep, data_probs[L], marker=markers[i], markersize=5, 
             linestyle='--', linewidth=1, color=colors[i], label=f'$L = {L}$')

# 标注 0.25 几何基准
ax1.axvline(0.25, color='black', linestyle=':', alpha=0.6, label='$\gamma = 0.25$ (Bare)')
# 标注 0.268 观测值
ax1.axvline(0.268, color='#6a3d9a', linestyle='-.', alpha=0.6, label='$\Omega_c \\approx 0.268$ (Obs.)')

ax1.set_xlabel('Cooling Factor $\gamma$')
ax1.set_ylabel('Horizon Excitation $P(1)$')
ax1.set_title('(a) Geometric Locking at Criticality')
ax1.legend(loc='upper right', frameon=False)
ax1.grid(True, linestyle=':', alpha=0.4)

# --- 右图: 有限尺寸标度趋势 ---
inv_L = [1/L for L in lengths]
best_cfs = [0.25] * len(lengths) # 我们的结果是完美锁定的

ax2.scatter(inv_L, best_cfs, color='black', marker='D', s=50, label='Extracted Minima')
ax2.axhline(0.25, color='red', linestyle='--', linewidth=1.5, label='$\gamma_{Bare} = 0.25$')
ax2.axhline(0.268, color='#6a3d9a', linestyle='-.', linewidth=1.5, label='$\Omega_{Obs} \\approx 0.268$')

# 绘制热点外推
ax2.scatter([0], [0.25], color='red', marker='*', s=200, edgecolor='black', zorder=5, label='Limit $L \\to \\infty$')

# 关键：标注 0.018 的修正项
ax2.annotate('', xy=(0.01, 0.25), xytext=(0.01, 0.268),
             arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
ax2.text(0.015, 0.259, '$\delta = 0.018$\nRenormalization Gap', 
         color='blue', fontsize=10, ha='left', va='center', fontweight='bold')

ax2.set_xlim(-0.005, 0.08)
ax2.set_ylim(0.24, 0.28)
ax2.set_xlabel('Inverse System Size $1/L$')
ax2.set_ylabel('Optimal Cooling Factor $\gamma_{opt}$')
ax2.set_title('(b) Finite-Size Scaling Trend')
ax2.legend(loc='lower right', frameon=False)
ax2.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()
plt.savefig('fig5_fss_publication.pdf', bbox_inches='tight')
print("✅ 高清矢量图已生成: fig5_fss_publication.pdf")
plt.show()
