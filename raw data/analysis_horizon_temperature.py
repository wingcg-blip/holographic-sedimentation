import matplotlib.pyplot as plt
from qiskit_ibm_runtime import QiskitRuntimeService

# ==========================================
# 🎯 你的目标 Job ID
# ==========================================
JOB_ID = "d59pm5vp3tbc73asembg"

def analyze_horizon_temperature():
    print(f"🕵️‍♂️ 正在连接 IBM Cloud 拉取任务: {JOB_ID} ...")
    
    # 1. 获取数据
    try:
        service = QiskitRuntimeService()
        job = service.job(JOB_ID)
        results = job.result()
        print("✅ 数据拉取成功！开始对 Q19 (视界末端) 进行热力学分析...")
    except Exception as e:
        print(f"❌ 拉取失败: {e}")
        return

    # 参数列表 (对应之前的实验设置)
    cooling_sweep = [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    
    # 存储结果
    q19_excitation_probs = []

    print("\n📊 视界温度读数 (Horizon Temperature Readings):")
    print(f"{'Cooling (γ)':<12} | {'P(Q19=1) [激发率]':<20} | {'物理状态'}")
    print("-" * 60)

    # 2. 遍历每一个 Cooling Factor 的实验结果
    for i, pub_result in enumerate(results):
        # SamplerV2 获取 counts
        counts = pub_result.data.meas.get_counts()
        total_shots = sum(counts.values())
        
        excited_shots = 0
        
        # 3. 核心逻辑：只盯着 Q19 看
        # Qiskit 的 bitstring 是 "Q19 Q18 ... Q0"
        # 所以 Q19 对应的是字符串的第 0 位 (startswith)
        for bitstring, count in counts.items():
            if bitstring.startswith('1'):  # Q19 是 1
                excited_shots += count
        
        prob = excited_shots / total_shots
        q19_excitation_probs.append(prob)
        
        # 简单判断状态
        status = "🔥 HOT (Random)"
        if prob < 0.48: status = "❄️ COLD (Sediment?)"
        if prob > 0.52: status = "💥 EJECTED (Entropy Dump)"
        if 0.48 <= prob <= 0.52: status = "〰️ Noise/Thermal"
        
        print(f"CF={cooling_sweep[i]:<9} | {prob:.5f}              | {status}")

    # ==========================================
    # 📈 自动画图 (这是给审稿人看的关键证据)
    # ==========================================
    plt.style.use('seaborn-v0_8-paper')
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 绘制曲线
    ax.plot(cooling_sweep, q19_excitation_probs, 'o-', color='#C71585', 
            linewidth=2, markersize=8, label='Horizon Excitation P(Q19=1)')
    
    # 绘制 0.5 随机线 (热混沌基准)
    ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=1.5, label='Thermal Chaos Limit (0.5)')
    
    # 高亮之前的信号区域 (MI Spike Zone)
    ax.axvspan(0.15, 0.30, color='gold', alpha=0.2, label='Correlation Zone (from MI)')

    # 标注
    ax.set_title(f"Thermodynamics of the Horizon (Q19)\nJob ID: {JOB_ID[-6:]}", fontsize=12)
    ax.set_xlabel(r"Cooling Factor $\gamma$", fontsize=12)
    ax.set_ylabel(r"Excitation Probability $P(1)$", fontsize=12)
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # 保存
    filename = "fig_horizon_q19.pdf"
    plt.tight_layout()
    plt.savefig(filename, format='pdf')
    print(f"\n📉 矢量图已生成: {filename}")
    plt.show()

if __name__ == "__main__":
    analyze_horizon_temperature()
