from ..launch import is_installed
import subprocess
import sys


def translateText(text,service,source,target):
    import translators as ts
    result = ts.translate_text(text,translator=service,from_language=source,to_language=target)
    return result



translatePackages =  {
    "translators": {"package": "translators", "version": ">=5.9.9"}
}

def checkHasInstallTranslateApi():
    states = []
    for package_name in translatePackages:
        package_info = translatePackages[package_name]
        item = {
            'name': package_name,
            'package': package_info['package'],
            'state': False
        }
        if is_installed(package_info['package']):
            import pkg_resources
            try:
                installed_version = pkg_resources.get_distribution(package_info['package']).version
                if pkg_resources.parse_version(installed_version) >= pkg_resources.parse_version("5.9.9"):
                    item['state'] = True
            except Exception as e:
                print(f"Error checking {package_name} version: {e}")
                item['state'] = False

        states.append(item)

    return states

def installTranslateApi():
    try:
        # 避免使用 pkg_resources，直接尝试安装
        print("translators包未安装，正在安装...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'translators>=5.9.9'])
        print("WeiLin-Comfyui-Tools ==> translators 已安装成功。")
        return True
    except Exception as e:
        print(f"安装translators时出错: {e}")
        return False

def applyTranslateApi():
    try:
        # 避免使用 pkg_resources，直接尝试导入和简单测试
        import translators
        # 简单测试一下是否能正常工作
        return True
    except ImportError:
        print("translators包未安装")
        return False
    except Exception as e:
        print(f"检查translators时出错: {e}")
        return False