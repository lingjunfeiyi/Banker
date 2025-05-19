# Banker🤖

一个集成了经典银行家算法和AI智能分析的死锁检测工具，可自动判断系统安全状态并提供专业解决方案，可使用自然语言解释当前状态下银行家算法的执行过程。

## 功能特性 🌟

- **双重检测机制**
  - ✅ 原生C语言实现的银行家算法核心
  - 🧠 DeepSeek-R1大模型智能分析
- **智能诊断**
  - 🔍 死锁原因深度分析
  - 💡 提供专业解决方案建议
  - 📚 算法执行过程自然语言解释

## 快速开始 🚀

### 环境要求

- Python 3.8+
- requests库 (`pip install requests`)

### 使用步骤

1. **编译 C 程序（已编译banker.exe）**：

	```bash
	gcc main.c safety.c request.c -o banker
	```

	

2. **运行 Python 大模型分析（需配置 API Key）**：

	```python
	# simulator.py
	sample_state = {
	        "proc_num": 5,
	        "res_num": 3,
	        "Max": [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
	        "Allocation": [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
	        "Available": [3, 3, 2]
	    }
	
	    api_token = "your-api-key"
	    c_bin_path = "banker.exe"
	    simulator = BankerSimulator(api_token, c_bin_path)
	    simulator.run_simulation(sample_state)
	```

## 输入格式示例 📝

```python
sample_state = {
    "proc_num": 5,
    "res_num": 3,
    "Max": [[7,5,3], [3,2,2], [9,0,2], [2,2,2], [4,3,3]],
    "Allocation": [[0,1,0], [2,0,0], [3,0,2], [2,1,1], [0,0,2]],
    "Available": [3,3,2]
}
```

## 输出示例 📊

### 安全状态

```bash
✅ 安全序列：[1, 3, 4, 0, 2]
🧠 银行家算法执行过程解释：
根据银行家算法，系统当前处于安全状态，存在安全执行序列，以下是详细分析过程:
1. **计算各进程剩余需求**...
```

### 不安全状态

```bash
⚠️ 系统处于不安全状态！
🧠 智能诊断建议：
当前系统处于死锁状态，原因如下：
**死锁原因分析**...
```
