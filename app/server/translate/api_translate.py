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
        import pkg_resources
        try:
            installed_version = pkg_resources.get_distribution("translators").version
            if pkg_resources.parse_version(installed_version) < pkg_resources.parse_version("5.9.9"):
                print("translators版本过低，正在升级...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'translators>=5.9.9'])
        except pkg_resources.DistributionNotFound:
            print("translators包未安装，正在安装...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'translators>=5.9.9'])
    except Exception as e:
        print(f"安装translators时出错: {e}")
        return False
    print("WeiLin-Comfyui-Tools ==> translators 已安装成功。")
    return True

def applyTranslateApi():
    if is_installed("translators"):
        import pkg_resources
        try:
            installed_version = pkg_resources.get_distribution("translators").version
            if pkg_resources.parse_version(installed_version) >= pkg_resources.parse_version("5.9.9"):
                return True
            else:
                print(f"当前translators版本({installed_version})过低，需要>=5.9.9")
                return False
        except pkg_resources.DistributionNotFound:
            print("translators包未找到，请先安装")
            return False
        except Exception as e:
            print(f"检查translators版本时出错: {e}")
            return False
    else:
        print("translators包未安装")
        return False