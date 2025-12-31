import json
import matplotlib.pyplot as plt
import numpy as np

# 文件名要和你刚才生成的一样
DATA_FILENAME = "sediment_data_torino.json"

def reanalyze_sediment():
    print(f"📂 Loading data from {DATA_FILENAME}...")
    
    try:
        with open(DATA_FILENAME, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ 找不到文件！请确认 json 文件在当前目录下。")
        return

    cooling_sweep = data["parameters"]["cooling_sweep"]
    chain_length = data["parameters"]["chain_length"]
    # 注意：这里我们需要原始 counts，但上一版代码只存了 signal_intensities。
    # 如果你刚才运行的是我给的 'Project_Sediment_Final.py'，
    # 抱歉，老哥，那一版为了省空间只存了归一化结果... 
    
    # === 补救措施 ===
    # 如果此时 job 对象还在内存里（你没关 Python 窗口），直接用 job.result()。
    # 如果窗口关了，我们需要用 Job ID 去 IBM 云端把原始 Counts 拉回来。
    
    job_id = data["job_id"]
    print(f"☁️ Re-fetching RAW data from IBM Cloud for Job: {job_id}")
    
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService()
    job = service.job(job_id)
    results = job.result()
    
    # === 新的分析逻辑：计算“沉积密度” (Hamming Weight) ===
    sediment_densities = []
    
    print("\n🔍 Mining for Dark Matter Density (Average Zeros)...")
    for i, pub_result in enumerate(results):
        counts = pub_result.data.meas.get_counts()
        total_shots = sum(counts.values())
        
        total_zeros = 0
        for bitstring, count in counts.items():
            # 计算这个 bitstring 里有多少个 '0'
            num_zeros = bitstring.count('0')
            total_zeros += num_zeros * count
            
        # 计算平均每个 qubit 上的 '0' 的概率
        # 结果范围 0.0 (全1) ~ 1.0 (全0)
        # 随机混沌应该在 0.5 左右
        avg_density = total_zeros / (total_shots * chain_length)
        sediment_densities.append(avg_density)
        
        print(f"   > CF={cooling_sweep[i]}: Density={avg_density:.4f} (Random ~0.5)")

    # === 画新图 ===
    plt.style.use('seaborn-v0_8-paper')
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 绘制实验数据
    ax.plot(cooling_sweep, sediment_densities, 'D-', color='#2E8B57', 
            linewidth=2, markersize=8, label='Sediment Density (Avg Zeros)')
    
    # 绘制随机基准线 (0.5)
    ax.axhline(y=0.5, color='red', linestyle='--', label='Thermal Chaos limit (0.5)')
    
    # 标注预期沉积区
    ax.axvspan(0.15, 0.30, color='gold', alpha=0.2, label='Sediment Zone')

    ax.set_title(f"Sediment Density Analysis (Re-mined)\nJob ID: {job_id[-6:]}", fontsize=12)
    ax.set_xlabel(r"Cooling Factor $\gamma$", fontsize=12)
    ax.set_ylabel(r"Matter Density ($\rho_{0}$)", fontsize=12)
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig("fig_sediment_density_remined.pdf", format='pdf', dpi=300)
    print("✅ New chart generated: fig_sediment_density_remined.pdf")
    plt.show()

if __name__ == "__main__":
    reanalyze_sediment()
