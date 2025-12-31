import numpy as np
import datetime
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# ==========================================
# 🎯 FIG 7: THE FINAL STRESS TEST (ULTIMATE)
# ==========================================

BACKEND_NAME = 'ibm_torino'
L = 20                       # 保持与 Fig. 5 一致
N_SHOTS = 8192               # 高精度采样
GAMMA_SWEEP = [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28]
NOISE_LEVELS = [0.0, 0.05, 0.10] # 0%, 5%, 10% 噪声注入

def create_fig7_circuit(gamma, noise_injection=0.0):
    """
    基于 shengbei2.py 的黄金电路，并加入主动噪声注入
    """
    qc = QuantumCircuit(L)
    
    # 1. 黄金混沌源 (Chaos Source) - 严格保持一致
    qc.h(0); qc.cx(0, 1); qc.rx(np.pi/1.3, 0); qc.rz(np.pi/2.5, 1); qc.cx(1, 0)
    qc.barrier()
    
    # 2. 沉积演化 (10 步 Trotter)
    for _ in range(10):
        for i in range(L - 1):
            # 基础参数
            j_val = 2.0
            g_val = gamma
            
            # 主动注入系统噪声 (模拟控制不精准)
            if noise_injection > 0:
                j_val *= (1 + np.random.uniform(-noise_injection, noise_injection))
                g_val *= (1 + np.random.uniform(-noise_injection, noise_injection))
            
            # Ising 相互作用
            qc.cx(i, i+1)
            qc.rz(j_val, i+1)
            qc.cx(i, i+1)
            
            # 沉积冷却项 (关键比例 1 : 0.5)
            qc.rz(g_val * np.pi, i+1)
            qc.rx(0.5 * g_val * np.pi, i+1)
    
    # 3. 测量视界及其邻居 (Q17, Q18, Q19) - 对应最后三个比特
    # Qiskit 测量到 classical bits [0, 1, 2]
    qc.measure_all() 
    return qc

def run_experiment():
    service = QiskitRuntimeService()
    backend = service.backend(BACKEND_NAME)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    
    all_circuits = []
    metadata = []

    print(f"🛠️  正在构建 Fig. 7 实验矩阵 (3 噪声级 x 7 采样点)...")
    for nl in NOISE_LEVELS:
        for g in GAMMA_SWEEP:
            qc = create_fig7_circuit(g, noise_injection=nl)
            transpiled = pm.run(qc)
            all_circuits.append(transpiled)
            metadata.append({"gamma": g, "noise": nl})

    print(f"🛫 提交至 {BACKEND_NAME} (Job ID 将在稍后显示)...")
    sampler = Sampler(mode=backend)
    sampler.options.default_shots = N_SHOTS
    job = sampler.run(all_circuits)
    
    print(f"✅ 任务已锁定: {job.job_id()}")
    return job.job_id()
# 在你文件的最底部添加：
if __name__ == "__main__":
    job_id = run_experiment()
    print(f"🚀 任务已成功发射！请前往 IBM Quantum 官网查看 Job ID: {job_id}")

# 等明天下午额度恢复，直接执行 run_experiment()
