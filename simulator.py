import requests
import subprocess
import json

class BankerExecutor:
    def __init__(self, c_bin_path):
        self.c_bin = c_bin_path
    
    def check_safety(self, state_data):
        input_str = ""
        input_str += f"{state_data['proc_num']} {state_data['res_num']} "
        for row in state_data['Max']:
            for val in row:
                input_str += f"{val} "
        for row in state_data['Allocation']:
            for val in row:
                input_str += f"{val} "
        for val in state_data['Available']:
            input_str += f"{val} "
        
        result = subprocess.run(
            [self.c_bin], 
            input=input_str.encode(),
            capture_output=True
        )
        output = result.stdout.decode().strip().split()
        is_safe = int(output[0])
        if is_safe:
            safe_seq = [int(x) for x in output[1:]]
        else:
            safe_seq = []
        return {'is_safe': is_safe, 'safe_seq': safe_seq}
class DeadlockAdvisor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        
    def analyze_deadlock(self, state_info):
        """
        分析系统状态信息中的死锁情况并获取解决方案
        
        参数:
            state_info (dict): 包含系统状态的字典，应包含以下键:
                - proc_num: 进程数
                - res_num: 资源类型数
                - Max: 各进程的最大资源需求
                - Allocation: 各进程已分配的资源
                - Available: 可用资源
                
        返回:
            str: DeepSeek-R1模型提供的死锁分析和解决方案
        """
        # 构建提示词
        prompt = f"""当前系统状态：
进程数：{state_info['proc_num']}
资源类型数：{state_info['res_num']}
各进程最大需求：{state_info['Max']}
已分配资源：{state_info['Allocation']}
可用资源：{state_info['Available']}

请分析死锁原因，并给出具体解决建议："""
        
        # 请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 请求体
        data = {
            "model": "deepseek-ai/DeepSeek-R1",  # 使用DeepSeek-R1模型
            "messages": [
                {"role": "system", "content": "你是一位专业的操作系统死锁分析专家。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,  # 较低的温度值使输出更确定性
            "max_tokens": 1000
        }
        
        try:
            # 发送请求
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=120  # 设置超时时间为60秒
            )
            
            # 检查响应状态码
            response.raise_for_status()
            
            # 解析响应JSON并返回结果
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except requests.exceptions.RequestException as e:
            # 处理请求错误
            print(f"API请求错误: {e}")
            return "抱歉，API请求过程中发生错误，请检查API密钥和网络连接。"
        except (KeyError, json.JSONDecodeError) as e:
            # 处理响应解析错误
            print(f"响应解析错误: {e}")
            return "抱歉，无法解析API响应，请检查API返回格式。"
        except Exception as e:
            # 处理其他错误
            print(f"发生未知错误: {e}")
            return "抱歉，分析过程中发生未知错误。"
        
    def analyze_banker_process(self, state_info):
        prompt = f"""当前系统状态：
进程数：{state_info['proc_num']}
资源类型数：{state_info['res_num']}
各进程最大需求：{state_info['Max']}
已分配资源：{state_info['Allocation']}
可用资源：{state_info['Available']}

请分析银行家算法执行过程，并给出具体解释："""
        
        # 请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 请求体
        data = {
            "model": "deepseek-ai/DeepSeek-R1",  # 使用DeepSeek-R1模型
            "messages": [
                {"role": "system", "content": "你是一位专业的操作系统算法分析专家。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,  # 较低的温度值使输出更确定性
            "max_tokens": 1000
        }
        
        try:
            # 发送请求
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=120  # 设置超时时间为60秒
            )
            
            # 检查响应状态码
            response.raise_for_status()
            
            # 解析响应JSON并返回结果
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except requests.exceptions.RequestException as e:
            # 处理请求错误
            print(f"API请求错误: {e}")
            return "抱歉，API请求过程中发生错误，请检查API密钥和网络连接。"
        except (KeyError, json.JSONDecodeError) as e:
            # 处理响应解析错误
            print(f"响应解析错误: {e}")
            return "抱歉，无法解析API响应，请检查API返回格式。"
        except Exception as e:
            # 处理其他错误
            print(f"发生未知错误: {e}")
            return "抱歉，分析过程中发生未知错误。"
        
class BankerSimulator:
    def __init__(self, api_token, c_bin_path):
        self.advisor = DeadlockAdvisor(api_token)
        self.executor = BankerExecutor(c_bin_path)

    def run_simulation(self, state_data):
        # 调用 C 程序进行安全检查
        result = self.executor.check_safety(state_data)
        is_safe = result.get('is_safe', False)
        safe_seq = result.get('safe_seq', [])

        if not is_safe:
            print("⚠️ 系统处于不安全状态！")
            # 调用大模型分析
            analysis = self.advisor.analyze_deadlock(state_data)
            print("🧠 智能诊断建议：")
            print(analysis)
        else:
            print(f"✅ 安全序列：{safe_seq}")
            analysis = self.advisor.analyze_banker_process(state_data)
            print("🧠 银行家算法执行过程解释：")
            print(analysis)


if __name__ == "__main__":
    # 示例输入数据
#   不安全状态
#     sample_state = {
#     "proc_num": 4,
#     "res_num": 2,
#     "Max": [[4, 2], [3, 3], [2, 2], [1, 1]],
#     "Allocation": [[2, 1], [2, 2], [1, 1], [0, 0]],
#     "Available": [0, 0]
# }
#   安全状态
    sample_state = {
        "proc_num": 5,
        "res_num": 3,
        "Max": [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
        "Allocation": [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
        "Available": [3, 3, 2]
    }
#   使用硅基流动的apikey
    api_token = "apikey"
    c_bin_path = "banker.exe"
    simulator = BankerSimulator(api_token, c_bin_path)
    simulator.run_simulation(sample_state)