import json
import matplotlib.pyplot as plt

# 1. 加载真机扫描数据
with open('sniper_evidence_0268.json', 'r') as f:
    data = json.load(f)

gamma_vals = data['parameters']
p1_probs = data['results']
min_cf = data['highlight']['min_cf']
min_prob = data['highlight']['min_prob']

plt.figure(figsize=(9, 6))

# 2. 绘制实验测量曲线
plt.plot(gamma_vals, p1_probs, 'o-', color='black', linewidth=2, markersize=8, label='Exp. Horizon State ($Q_{19}$)')

# 3. 标注实验发现的沉积点 (0.25)
plt.scatter(min_cf, min_prob, color='red', s=150, marker='*', zorder=5, label=f'Deepest Dip ($\gamma=0.25$)')

# 4. 标注宇宙学暗物质常数 (0.268) 作为对比
plt.axvline(x=0.268, color='green', linestyle=':', linewidth=2, alpha=0.7)
plt.text(0.269, 0.50, 'Dark Matter Constant (0.268)', color='green', rotation=90, verticalalignment='center', fontweight='bold')

# 5. 标注热混沌极限 (0.5)
plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
plt.text(0.22, 0.505, 'Thermal Chaos Limit', color='gray', fontsize=10)

# 6. 图表装饰 (带上真实 Job ID)
plt.title(f"Supplemental Fig S2: High-Resolution Sniper Scan\nJob ID: {data['job_id']}", fontsize=14, pad=15)
plt.xlabel(r"Cooling Factor $\gamma$ (Geometry)", fontsize=12)
plt.ylabel(r"Horizon Temperature (Probability $P_1$)", fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.savefig('si_fig_s2_sniper_scan.pdf')
plt.show()
