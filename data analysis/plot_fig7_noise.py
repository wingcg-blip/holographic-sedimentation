import numpy as np
import matplotlib.pyplot as plt
import csv
from qiskit_ibm_runtime import QiskitRuntimeService

# ==========================================
# 🎯 配置区域
# ==========================================
JOB_ID = 'd5a9jognsj9s73b7ed3g'  # 你的最新任务ID
CSV_FILENAME = "fig7_final_data.csv"
PDF_FILENAME = "fig7_ultimate_robustness.pdf"

# 实验参数 (需与提交时完全对应)
GAMMA_SWEEP = [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28]
NOISE_LEVELS = [0.0, 0.05, 0.10]

def extract_p1(pub_result, bit_index):
    """从 SamplerV2 结果中提取特定比特的 P(1)"""
    try:
        # 尝试获取所有测量寄存器的数据
        data = pub_result.data
        counts = None
        for attr in dir(data):
            if not attr.startswith('_'):
                val = getattr(data, attr)
                if hasattr(val, 'get_counts'):
                    counts = val.get_counts()
                    break
        
        if counts is None: return 0.0
        
        total = sum(counts.values())
        excited = 0
        for bitstring, count in counts.items():
            # Qiskit bitstring 顺序：从右往左数
            # 我们主要关注视界比特 Q19
            if bitstring[-(bit_index + 1)] == '1':
                excited += count
        return excited / total
    except Exception as e:
        print(f"解析出错: {e}")
        return 0.0

def fetch_and_plot():
    print(f"📡 正在从 IBM Quantum 抓取数据 (Job: {JOB_ID})...")
    service = QiskitRuntimeService()
    job = service.job(JOB_ID)
    results = job.result()

    all_rows = []
    plot_data = {nl: [] for nl in NOISE_LEVELS}
    result_idx = 0

    # 1. 解析数据并存入 CSV
    for nl in NOISE_LEVELS:
        for cf in GAMMA_SWEEP:
            # 提取 Q19 (视界) 的概率
            p1 = extract_p1(results[result_idx], 19) 
            all_rows.append({"noise_level": nl, "gamma": cf, "p1": p1})
            plot_data[nl].append(p1)
            result_idx += 1

    with open(CSV_FILENAME, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["noise_level", "gamma", "p1"])
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"✅ CSV 数据已保存至: {CSV_FILENAME}")

    # 2. 生成 PDF 矢量图 (PRX 投稿标准)
    plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})
    plt.figure(figsize=(8, 6))
    
    colors = ['#1f77b4', '#ff7f0e', '#d62728'] # 经典学术配色
    markers = ['o', 's', '^'] # 圆点、方块、三角

    for i, nl in enumerate(NOISE_LEVELS):
        plt.plot(GAMMA_SWEEP, plot_data[nl], 
                 marker=markers[i], linestyle='-', color=colors[i],
                 linewidth=2, markersize=8, 
                 label=f'Control Noise {nl*100:.0f}%')

    # 标注相变点
    plt.axvline(0.25, color='black', linestyle='--', alpha=0.5, label='$\gamma_c = 0.25$')
    
    # 装饰美化
    plt.xlabel(r'Cooling Factor $\gamma$', fontsize=14)
    plt.ylabel(r'Horizon Excitation $P(1)$', fontsize=14)
    plt.title('Fig 7: Robustness of Holographic Sedimentation', fontsize=16)
    plt.legend(frameon=True, facecolor='white', framealpha=1)
    plt.grid(True, which='both', linestyle=':', alpha=0.6)
    
    # 保存矢量图
    plt.tight_layout()
    plt.savefig(PDF_FILENAME, format='pdf', dpi=600)
    print(f"📉 矢量 PDF 图表已生成: {PDF_FILENAME}")
    plt.show()

if __name__ == "__main__":
    fetch_and_plot()
