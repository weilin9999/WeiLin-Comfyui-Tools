import subprocess
import sys
import os

requset_path = os.path.join(os.path.dirname(__file__), "./requirements.txt")
def install_requirements():
    try:
        # 检查是否已经安装了所有依赖项
        with open(requset_path, 'r') as f:
            requirements = f.read().splitlines()
        
        for requirement in requirements:
            try:
                __import__(requirement.split('==')[0])
            except ImportError:
                print(f"{requirement} 未安装，正在安装...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])
        
        print("WeiLin-Comfyui-Tools ==> 所有依赖项已安装。")
    except Exception as e:
        print(f"WeiLin-Comfyui-Tools ==> 安装依赖项时出错: {e}")