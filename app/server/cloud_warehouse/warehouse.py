import requests

api_url = "https://api.gitcode.com"
public_token = "?access_token=y7S27_wDHXy1xaSQjupJk-Wy"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json'
}

# 获取仓库的根目录
def get_main_warehouse():
    req_url = api_url + "/api/v5/repos/qq_27627297/WeiLin-Comfyui-Tools-Prompt/git/trees/master"+public_token
    response = requests.get(req_url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_warehouse_tree(path):
    req_url = api_url + "/api/v5/repos/qq_27627297/WeiLin-Comfyui-Tools-Prompt/contents/"+path+public_token
    response = requests.get(req_url, headers=headers)
    response.raise_for_status()
    return response.json()

