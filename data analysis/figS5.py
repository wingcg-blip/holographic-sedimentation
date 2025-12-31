import numpy as np
import matplotlib.pyplot as plt

# 1. 核心物理参数 (由 IBM Torino 实验锁定)
gamma_bare = 0.25
omega_obs = 0.268
z_eff_final = 0.072
job_id = "d59q7e1smlfc739ksb3g" # 核心溯源 ID

# 生成演化路径: Omega = gamma * (1 + z)
z_axis = np.linspace(0, 0.1, 100)
omega_path = gamma_bare * (1 + z_axis)

fig, ax = plt.subplots(figsize=(8, 6))

# 1. 绘制重整化流路径 (紫线)
ax.plot(z_axis, omega_path, color='#6a0dad', linewidth=3, label='Metric Renormalization Path')

# 2. 标注实验室端点 (z=0)
ax.scatter(0, gamma_bare, color='blue', s=120, zorder=5, label=r'Lab Bare Value ($\gamma_{bare}=0.25$)')

# 3. 标注宇宙学观测点 (Planck 2018)
ax.scatter(z_eff_final, omega_obs, color='red', s=180, marker='*', zorder=5, 
            label=r'Planck 2018 ($\Omega_{obs} \approx 0.268$)')

# 4. 标注 0.018 的红移间隙
ax.annotate('', xy=(z_eff_final, gamma_bare), xytext=(z_eff_final, omega_obs),
             arrowprops=dict(arrowstyle='<->', color='green', lw=2))
ax.text(z_eff_final + 0.005, (gamma_bare + omega_obs)/2, 
         r'$\delta = 0.018$' + '\n' + r'Expansion Gap', 
         color='green', fontsize=11, fontweight='bold', va='center')

# 5. 辅助虚线
ax.axhline(y=gamma_bare, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=z_eff_final, color='gray', linestyle=':', alpha=0.5)

# --- 关键修改：左下角溯源水印 ---
# 使用 transform=ax.transAxes 确保位置固定在绘图区左下角
# (0.02, 0.04) 表示距离左边框 2%, 距离底边框 4%
ax.text(0.02, 0.04, 
         f"Input: $\gamma_{{bare}}=0.250 \pm 0.001$\nVerified by Job: {job_id}", 
         transform=ax.transAxes, # 使用相对坐标
         fontsize=9, color='navy', alpha=0.6, 
         fontstyle='italic',
         verticalalignment='bottom', 
         horizontalalignment='left',
         bbox=dict(facecolor='white', alpha=0.3, edgecolor='none', pad=3))
# -------------------------------

# 6. 图表修饰
ax.set_title("Supplemental Fig S5: Cosmological Scaling & Metric Renormalization", fontsize=14, pad=15)
ax.set_xlabel(r"Effective Cosmological Redshift $z_{eff}$", fontsize=12)
ax.set_ylabel(r"Observed Density Parameter $\Omega_{DM}$", fontsize=12)
ax.set_xlim(-0.01, 0.1) # 稍微加宽左侧，防止文字太挤
ax.set_ylim(0.24, 0.28)
ax.grid(True, linestyle=':', alpha=0.4)
ax.legend(loc='upper left', frameon=True, shadow=True)

plt.tight_layout()
plt.savefig('si_fig_s5_redshift_integration_v2.pdf', dpi=300)
plt.show()

print("Fig S5 V2版生成成功！水印已精准挪位。")
