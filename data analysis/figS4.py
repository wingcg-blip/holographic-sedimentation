import json
import matplotlib.pyplot as plt
import numpy as np

# 1. 加载真机 FSS 实验数据
with open('fss_scaling_data.json', 'r') as f:
    fss_data = json.load(f)

# 2. 设定 2D Ising 理论临界指数 (这是咱们的核心物理结论)
gamma_c = 0.25
nu = 1.0      # 关联长度指数 (Correlation length exponent)
beta = 0.125  # 序参量指数 (Order parameter exponent)

plt.figure(figsize=(9, 7))

# 定义不同尺寸的颜色
colors = {'L16': '#1f77b4', 'L20': '#ff7f0e', 'L24': '#2ca02c', 'L28': '#d62728'}

# 3. 处理每个尺寸的数据并进行标度变换
for L_key in ['L16', 'L20', 'L24', 'L28']:
    L_val = int(L_key[1:])
    cfs = np.array(fss_data['raw'][L_key]['cfs'])
    probs = np.array(fss_data['raw'][L_key]['probs'])
    
    # 序参量 m = 1 - 2*P(1)
    # 将激发概率转化为类似“磁化强度”的几何序参量
    m = 1 - 2 * probs
    
    # 进行重整化缩放 (Data Collapse Transformation)
    # 横轴: (gamma - gamma_c) * L^(1/nu)
    # 纵轴: m * L^(beta/nu)
    rescaled_x = (cfs - gamma_c) * (L_val ** (1/nu))
    rescaled_y = m * (L_val ** (beta/nu))
    
    plt.plot(rescaled_x, rescaled_y, 'o-', label=f'Size $L={L_val}$', 
             color=colors[L_key], markersize=8, linewidth=2, alpha=0.8)

# 4. 辅助线与图表美化
plt.axvline(x=0, color='black', linestyle='--', alpha=0.3)
plt.xlabel(r'Rescaled Coupling $(\gamma - \gamma_c) L^{1/\nu}$', fontsize=14)
plt.ylabel(r'Rescaled Order Parameter $m L^{\beta/\nu}$', fontsize=14)
plt.title("Supplemental Fig S4: Universal Data Collapse (2D Ising Class)\n" + 
          f"Job ID: {fss_data['job_id']}", fontsize=15, pad=15)

plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=12, frameon=True, shadow=True)
plt.tight_layout()

# 5. 保存为 PDF
plt.savefig('si_fig_s4_data_collapse.pdf')
plt.show()
