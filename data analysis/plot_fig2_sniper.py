import numpy as np
import matplotlib.pyplot as plt
import json
import datetime
from qiskit_ibm_runtime import QiskitRuntimeService

# ==========================================
# 🎯 目标任务: The Cosmological Constant Scan
# ==========================================
JOB_ID = "d59q2qjht8fs73a50kpg"
BACKEND_NAME = 'ibm_torino'
DATA_FILENAME = "sniper_evidence_0268.json"
PLOT_FILENAME = "fig_cosmic_match_0268.pdf"

# 必须与你提交时的参数完全一致
# 0.268 是我们要验证的宇宙常数
COOLING_SWEEP = [0.22, 0.23, 0.24, 0.25, 0.26, 0.268, 0.27, 0.28]

def analyze_and_plot():
    print(f"📡 正在连接 IBM Quantum，拉取任务 {JOB_ID} ...")
    
    try:
        service = QiskitRuntimeService()
        job = service.job(JOB_ID)
        
        # 检查状态，如果还在跑会阻塞等待
        status = job.status()
        print(f"   当前状态: {status}")
        
        results = job.result()
        print("✅ 数据包已下载！开始解码视界状态 (Q19)...")
        
    except Exception as e:
        print(f"❌ 拉取失败: {e}")
        return

    # ==========================================
    # 1. 数据解码 (只看 Q19 的沉积率)
    # ==========================================
    q19_probs = []
    
    print("\n🔍 狙击读数 (Sniper Readings):")
    print(f"{'Cooling (γ)':<12} | {'P(Q19=1)':<15} | {'偏差 (Diff)'}")
    print("-" * 50)
    
    min_prob = 1.0
    min_cf = -1.0

    for i, pub_result in enumerate(results):
        # SamplerV2 格式提取
        counts = pub_result.data.meas.get_counts()
        total_shots = sum(counts.values())
        
        excited_shots = 0
        # 统计 Q19 为 '1' 的次数 (bitstring startswith)
        for bitstring, count in counts.items():
            if bitstring.startswith('1'): 
                excited_shots += count
        
        prob = excited_shots / total_shots
        q19_probs.append(prob)
        
        # 寻找最低点 (最冷的沉积点)
        if prob < min_prob:
            min_prob = prob
            min_cf = COOLING_SWEEP[i]
            
        diff = prob - 0.5
        print(f"CF={COOLING_SWEEP[i]:<9} | {prob:.5f}        | {diff:+.5f}")

    # ==========================================
    # 2. 保存原始证据 (JSON)
    # ==========================================
    data_packet = {
        "job_id": JOB_ID,
        "backend": BACKEND_NAME,
        "timestamp": datetime.datetime.now().isoformat(),
        "parameters": COOLING_SWEEP,
        "results": q19_probs,
        "highlight": {"min_prob": min_prob, "min_cf": min_cf}
    }
    
    with open(DATA_FILENAME, 'w') as f:
        json.dump(data_packet, f, indent=4)
    print(f"\n💾 原始证据已封存: {DATA_FILENAME}")

    # ==========================================
    # 3. 绘制宇宙常数验证图 (PDF)
    # ==========================================
    # 设置科学绘图风格
    try:
        plt.style.use('seaborn-v0_8-paper')
    except:
        pass

    fig, ax = plt.subplots(figsize=(9, 6))
    
    # 绘制实验数据曲线
    ax.plot(COOLING_SWEEP, q19_probs, 'o-', color='#191970', 
            linewidth=2, markersize=8, label='Exp. Horizon State P(Q19)')
    
    # 标记最低点
    ax.plot(min_cf, min_prob, 'r*', markersize=18, label=f'Deepest Dip (γ={min_cf})')
    
    # 绘制 0.268 宇宙常数参考线 (垂直线)
    ax.axvline(x=0.268, color='gold', linestyle='--', linewidth=2, alpha=0.8, label='Dark Matter Constant (0.268)')
    
    # 绘制 0.5 热噪声基准线 (水平线)
    ax.axhline(y=0.5, color='gray', linestyle=':', label='Thermal Chaos Limit')

    # 标注
    ax.set_title(f"Sniper Scan: Searching for Cosmological Match\nBackend: {BACKEND_NAME} | Shots: 8192", fontsize=12)
    ax.set_xlabel(r"Cooling Factor $\gamma$ (Geometry)", fontsize=12)
    ax.set_ylabel(r"Horizon Temperature (Probability $P_{1}$)", fontsize=12)
    
    # 如果最低点正好在 0.268 附近，加个特殊注释
    if abs(min_cf - 0.268) < 0.001:
        ax.annotate('MATCH!', xy=(0.268, min_prob), xytext=(0.268, min_prob-0.03),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    fontsize=12, color='red', fontweight='bold', ha='center')

    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(PLOT_FILENAME, format='pdf', dpi=300)
    print(f"📉 最终图表已生成: {PLOT_FILENAME}")
    
    # 直接在终端输出结果判断
    print("\n==========================================")
    print(f"🏆 最低沉积点位置: CF = {min_cf}")
    if min_cf == 0.268:
        print("🚨🚨🚨 警报：完全命中！与宇宙暗物质丰度吻合！ 🚨🚨🚨")
        print("请立即备份数据，准备香槟！")
    elif min_cf == 0.26:
        print("⚠️ 接近命中：落在 0.26。")
    elif min_cf == 0.27:
        print("⚠️ 接近命中：落在 0.27。")
    else:
        print(f"ℹ️ 结果落在 {min_cf}。需要进一步理论解释。")
    print("==========================================")
    
    plt.show()

if __name__ == "__main__":
    analyze_and_plot()
