
import comfy.lora
import comfy.utils
import logging
import locale
import json
import shutil

# Server Init
from .app.server.prompt_server import *

# 检测系统语言
localLan = locale.getdefaultlocale()[0]
placeholder_text = ""
retrun_name_text = ""
retrun_type_text = ""
node_name_text = ""
node_model_text = ""
if localLan == "zh_CN":
    placeholder_text = "输入提示词"
    retrun_name_text = "条件"
    retrun_type_text = "条件"
    node_name_text = "WeiLin-节点工具"
    node_model_text = "模型"
else:
    placeholder_text = "input prompt words"
    retrun_name_text = "CONDITIONING"
    retrun_type_text = "CONDITIONING"
    node_name_text = "WeiLin Node Tools"
    node_model_text = "MODEL"


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

# 提示词UI
class WeiLinPromptUI:

    def __init__(self):
        self.loaded_loraA = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP", ),
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": placeholder_text,
                }),
            },
            "optional": {
                "model": ("MODEL",)
            }
        }

    # RETURN_TYPES = ("STRING",)
    # RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_TYPES = ("STRING", "CONDITIONING", "MODEL", )
    RETURN_NAMES = ("STRING", "CONDITIONING", "MODEL", )

    # FUNCTION = "encode"
    FUNCTION = "load_lora_ing"

    # OUTPUT_NODE = False

    CATEGORY = node_name_text

    # 加载Lora
    def load_lora_ing(self, model, clip, positive):
        model_lora_secondA = model
        clip_lora_secondA = clip

        text_dec = ""
        lora_list= None

        if is_json(positive):
            json_object = json.loads(positive)
            lora_list = json_object.get("lora", None)
            text_dec = json_object.get("prompt", "")
        else:
            text_dec = positive

        # 当模型不为空时
        if model != None and lora_list != None:
            for str_lora_item in lora_list:
                # print(loar_sim_path,str_n_arr)
                strength_model = float(str_lora_item["weight"])
                strength_clip = float(str_lora_item["text_encoder_weight"])
                print("strength_model：",strength_model,"strength_clip：",strength_clip)
                if strength_clip<=0.0:
                    strength_clip = 0
                if strength_model <= 0.0:
                    strength_model = 0.5

                lora_path = folder_paths.get_full_path("loras", str_lora_item["lora"])
                print("lora_path:",lora_path)
                lora = None
                if self.loaded_loraA is not None:
                    if self.loaded_loraA[0] == lora_path:
                        lora = self.loaded_loraA[1]
                    else:
                        temp = self.loaded_loraA
                        self.loaded_loraA = None
                        del temp

                if lora is None:
                    lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
                    self.loaded_loraA = (lora_path, lora)

                model_lora_secondA, clip_lora_secondA = load_lora_for_models(model_lora_secondA, clip_lora_secondA, lora, strength_model, strength_clip)
        
        tokensA = clip_lora_secondA.tokenize(text_dec)
        outputA = clip_lora_secondA.encode_from_tokens(tokensA, return_pooled=True, return_dict=True)
        condA = outputA.pop("cond")
        return (text_dec,[[condA, outputA]], model_lora_secondA)
        # return (model_lora_second, clip_lora_second)


def load_lora_for_models(model, clip, lora, strength_model, strength_clip):
    key_map = {}
    if model is not None:
        key_map = comfy.lora.model_lora_keys_unet(model.model, key_map)
    if clip is not None:
        key_map = comfy.lora.model_lora_keys_clip(
            clip.cond_stage_model, key_map)

    loaded = comfy.lora.load_lora(lora, key_map)
    if model is not None:
        new_modelpatcher = model.clone()
        k = new_modelpatcher.add_patches(loaded, strength_model)
    else:
        k = ()
        new_modelpatcher = None

    if clip is not None:
        new_clip = clip.clone()
        k1 = new_clip.add_patches(loaded, strength_clip)
    else:
        k1 = ()
        new_clip = None
    k = set(k)
    k1 = set(k1)
    for x in loaded:
        if (x not in k) and (x not in k1):
            logging.warning("NOT LOADED {}".format(x))

    return (new_modelpatcher, new_clip)

def copy_folder(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for item in os.listdir(source_folder):
        source = os.path.join(source_folder, item)
        destination = os.path.join(destination_folder, item)

        if os.path.isdir(source):
            copy_folder(source, destination)
        else:
            shutil.copy2(source, destination)

# 检测Tag组是否存在，不存在则复制模板
dir = os.path.join(os.path.dirname(__file__),'./tags_userdatas/')
filenames=os.listdir(dir)
if len(filenames) <= 0:
    dirDes = os.path.join(os.path.dirname(__file__),'./tags_templete/')
    copy_folder(dirDes, dir)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "WeiLinPromptUI": WeiLinPromptUI,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}

if localLan == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "WeiLinPromptUI": "WeiLin 提示词UI",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "WeiLinPromptUI": "WeiLin Prompt UI",
    }

WEB_DIRECTORY = "./js_node"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

