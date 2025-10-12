# 硅基AI对接
import requests
from ..user_init.user_init import get_ai_info_setting

_LANG_NAME = {
    "zh": "Chinese ", "zh_CN": " Chinese ", "zh_TW": "Chinese (traditional) ",
    "en": "English ", "ja": " Japanese ", "ko": "Korean ",
    "fr": "French ", "de": " German ", "es": "Spanish ",
    "ru": "Russian ", "it": " Italian ", "pt": "Portuguese"
}


def _lang_to_name(code: str) -> str:
    if not code:
        return "Chinese"
    return _LANG_NAME.get(code, code)


# 硅基AI翻译接口
async def translateObject(objectData: str, target_lang_code: str = "zh") -> str:
    ai_info_setting = get_ai_info_setting()
    api_key = ai_info_setting.get("api_key", "")
    base_url = ai_info_setting.get(
        "base_url", "https://api.siliconflow.cn/v1").rstrip("/")
    model = ai_info_setting.get("model", "THUDM/glm-4-9b-chat")

    print("💡[WeiLin-Comfyui-Tools] 硅基AI翻译接口-使用模型：",  model, " 目标语种：", target_lang_code, " 正在翻译中...")

    url = f"{base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert in data translation processing. translate the text field of the JSON string data passed by the user into {_lang_to_name(target_lang_code)} and fill it in the corresponding translate field. You only need to return the corresponding JSON string data and do not modify any other data or parameters"
            },
            {
                "content": objectData,
                "role": "user"
            }
        ],
        "stream": False,
        "max_tokens": 4096,
        "enable_thinking": False,
        "thinking_budget": 4096,
        "min_p": 0.05,
        "stop": None,
        "temperature": 0,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "json_object"},
        "tools": []
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    dataResponse = response.json()
    print(f"💡[WeiLin-Comfyui-Tools] 硅基AI翻译接口-翻译完成，以下是使用信息：\n - PromptToken：{dataResponse['usage']['total_tokens']}，\n - CompletionTokens：{dataResponse['usage']['completion_tokens']}，\n - TotalTokens：{dataResponse['usage']['total_tokens']}")
    return dataResponse["choices"][0]["message"]["content"]


# 硅基AI模型列表接口
def getModelList() -> dict:
    ai_info_setting = get_ai_info_setting()
    api_key = ai_info_setting["api_key"]
    base_url = ai_info_setting["base_url"]

    url = f"{base_url}/models"

    headers = {"Authorization": f"Bearer {api_key}"}

    querystring = {"type": "text"}

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
