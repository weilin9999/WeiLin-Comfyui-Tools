from ..launch import is_installed
import subprocess
import sys


def translateText(text,service,source,target):
    import translators as ts
    result = ts.translate_text(text,translator=service,from_language=source,to_language=target)
    return result



translatePackages =  {
    "translators": "translators"
}

def checkHasInstallTranslateApi():
    states = []
    for package_name in translatePackages:
        package = translatePackages[package_name]
        item = {
            'name': package_name,
            'package': package,
            'state': False
        }
        if is_installed("translators"):
            item['state'] = True

        states.append(item)

    return states


def installTranslateApi():
    try:
        __import__("translators")
    except ImportError:
        print("translators包未安装，正在安装...")
        print("translators package is not install，is install...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'translators'])
    print("WeiLin-Comfyui-Tools ==> translators 已安装成功。")

def applyTranslateApi():
    if is_installed("translators"):
        return True
    return False