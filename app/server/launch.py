import importlib.util
import sys
import os
import subprocess

python = sys.executable
default_command_live = True
index_url = os.environ.get('INDEX_URL', "")

def is_installed(package):
    try:
        spec = importlib.util.find_spec(package)
    except ModuleNotFoundError:
        return False

    return spec is not None

def run_pip(command, desc=None, live=default_command_live):
    index_url_line = f' --index-url {index_url}' if index_url != '' else ''
    return run(f'"{python}" -m pip {command} --prefer-binary{index_url_line}', desc=f"Installing {desc}", errdesc=f"Couldn't install {desc}", live=live)

def run_pip_noex(command, desc=None, live=default_command_live):
    return run(f'"{python}" -m pip {command} ', desc=f"Installing {desc}", errdesc=f"Couldn't install {desc}", live=live)

def run_get_python():
    result = subprocess.run([python, "--version"], capture_output=True, text=True, check=True)
    # 输出版本信息
    # print("Python version:", result.stdout.strip())
    return result.stdout.strip()

def is_module_installed(module_name):
    try:
        # 尝试运行 "python -c 'import module_name'" 命令
        result = subprocess.run(
            [python, "-c", f"import {module_name}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # 如果没有抛出异常，说明模块已安装
        return True
    except subprocess.CalledProcessError:
        # 如果抛出异常，说明模块未安装
        return False

def run(command, desc=None, errdesc=None, custom_env=None, live: bool = default_command_live) -> str:
    if desc is not None:
        print(desc)

    run_kwargs = {
        "args": command,
        "shell": True,
        "env": os.environ if custom_env is None else custom_env,
        "encoding": 'utf8',
        "errors": 'ignore',
    }

    if not live:
        run_kwargs["stdout"] = run_kwargs["stderr"] = subprocess.PIPE

    result = subprocess.run(**run_kwargs)

    if result.returncode != 0:
        error_bits = [
            f"{errdesc or 'Error running command'}.",
            f"Command: {command}",
            f"Error code: {result.returncode}",
        ]
        if result.stdout:
            error_bits.append(f"stdout: {result.stdout}")
        if result.stderr:
            error_bits.append(f"stderr: {result.stderr}")
        raise RuntimeError("\n".join(error_bits))

    return (result.stdout or "")
