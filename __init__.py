
import comfy.lora
import comfy.utils
import logging
import locale
import json
import shutil

# Server Init
from .install_request import *
install_requirements()
from .app.server.prompt_server import *

# 检测系统语言
localLan = locale.getdefaultlocale()[0]
placeholder_text = ""
retrun_name_text = ""
retrun_type_text = ""
node_name_text = ""
node_model_text = ""
placeholder_node_text = ""
placeholder_lora_text = ""
if localLan == "zh_CN":
    placeholder_text = "输入提示词"
    placeholder_lora_text = "Lora信息框"
    placeholder_node_text = "输入节点命名"
    retrun_name_text = "条件"
    retrun_type_text = "条件"
    node_name_text = "WeiLin-Tools-节点工具"
    node_model_text = "模型"
else:
    placeholder_text = "input prompt words"
    placeholder_lora_text = "Lora info box"
    retrun_name_text = "CONDITIONING"
    retrun_type_text = "CONDITIONING"
    node_name_text = "WeiLin Node Tools"
    node_model_text = "MODEL"
    placeholder_node_text = "input node name"


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True

class AnyType(str):
    """
    A class representing any type in ComfyUI nodes.
    Used for parameters that can accept any type of input.
    """
    def __ne__(self, __value: object) -> bool:
        return False

    @classmethod
    def INPUT_TYPE(cls):
        return (ANY, {})

ANY = AnyType("*")

# 提示词UI
class WeiLinPromptUI:

    def __init__(self):
        self.loaded_loraA = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": placeholder_text,
                }),
            },
            "optional": {
                "lora_str": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": placeholder_lora_text,
                }),
                "temp_str": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "temp prompt words",
                }),
                "temp_lora_str": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "temp prompt words",
                }),
                "opt_text": (ANY, {"default": ""}),
                "opt_clip": ("CLIP", ),
                "opt_model": ("MODEL",),
            }
        }

    # RETURN_TYPES = ("STRING",)
    # RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_TYPES = ("STRING", "CONDITIONING", "CLIP", "MODEL", )
    RETURN_NAMES = ("STRING", "CONDITIONING", "CLIP", "MODEL", )

    # FUNCTION = "encode"
    FUNCTION = "load_lora_ing"

    # OUTPUT_NODE = False

    CATEGORY = node_name_text

    # 加载Lora
    def load_lora_ing(self, positive="",lora_str="",temp_str="",temp_lora_str="", opt_text="", opt_clip=None, opt_model=None):
        model_lora_secondA = opt_model
        clip_lora_secondA = opt_clip

        text_dec = ""
        lora_list= None

        if is_json(positive):
            json_object = json.loads(positive)
            lora_list = json_object.get("lora", None)
            if len(opt_text) > 0:
                text_dec = opt_text +", "+ json_object.get("prompt", "")
            else:
                text_dec = json_object.get("prompt", "")
        else:
            if len(opt_text) > 0:
                text_dec = opt_text +", "+positive
            else:
                text_dec = positive
        if len(lora_str) > 0:
            json_object = json.loads(lora_str)
            lora_list = json_object

        # 当模型不为空时
        if opt_model != None and lora_list != None:
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
                print("加载Lora lora_path:",lora_path)
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
        if opt_clip != None:
            tokensA = clip_lora_secondA.tokenize(text_dec)
            outputA = clip_lora_secondA.encode_from_tokens(tokensA, return_pooled=True, return_dict=True)
            condA = outputA.pop("cond")
            return (text_dec,[[condA, outputA]], clip_lora_secondA, model_lora_secondA)
        return (text_dec, clip_lora_secondA, clip_lora_secondA, model_lora_secondA)
        # return (model_lora_second, clip_lora_second)


# 提示词UI - 仅使用Lora堆
class WeiLinPromptUIOnlyLoraStack:

    def __init__(self):
        self.loaded_loraA = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP", ),
                "model": ("MODEL",),
            },
            "optional": {
                "lora_str": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": placeholder_lora_text,
                }),
                "temp_lora_str": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "temp prompt words",
                }),
            }
        }

    RETURN_TYPES = ( "CLIP", "MODEL", )
    RETURN_NAMES = ( "CLIP", "MODEL", )

    # FUNCTION = "encode"
    FUNCTION = "load_lora_ing"

    # OUTPUT_NODE = False

    CATEGORY = node_name_text

    # 加载Lora
    def load_lora_ing(self, clip=None, model=None, lora_str="", temp_lora_str=""):
        model_lora_secondA = model
        clip_lora_secondA = clip

        lora_list= None

        if len(lora_str) > 0:
            json_object = json.loads(lora_str)
            lora_list = json_object

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
                print("加载Lora lora_path:",lora_path)
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

        return (clip_lora_secondA, model_lora_secondA)
        # return (model_lora_second, clip_lora_second)

# 提示词UI - 不加载Lora
class WeiLinPromptUIWithoutLora:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": placeholder_text,
                }),
            },
            "optional": {
                "temp_str": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "temp prompt words",
                }),
                "opt_text": (ANY, {"default": ""}),
                "opt_clip": ("CLIP", ),
            }
        }

    RETURN_TYPES = ("STRING", "CONDITIONING", "CLIP", )
    RETURN_NAMES = ("STRING", "CONDITIONING", "CLIP", )

    FUNCTION = "encode"

    CATEGORY = node_name_text

    def encode(self, positive="", temp_str="", opt_text="", opt_clip=None):
        text_dec = ""
        if is_json(positive):
            json_object = json.loads(positive)
            if len(opt_text) > 0:
                text_dec = opt_text +", "+ json_object.get("prompt", "")
            else:
                text_dec = json_object.get("prompt", "")
        else:
            if len(opt_text) > 0:
                text_dec = opt_text +", "+positive
            else:
                text_dec = positive
        
        if opt_clip is not None:
            tokens = opt_clip.tokenize(text_dec)
            return (text_dec, opt_clip.encode_from_tokens_scheduled(tokens), opt_clip)
        
        return (text_dec, opt_clip, opt_clip)



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




# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "WeiLinPromptUI": WeiLinPromptUI,
    "WeiLinPromptUIWithoutLora": WeiLinPromptUIWithoutLora,
    "WeiLinPromptUIOnlyLoraStack": WeiLinPromptUIOnlyLoraStack,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}

if localLan == "zh_CN":
    NODE_DISPLAY_NAME_MAPPINGS = {
        "WeiLinPromptUI": "WeiLin 全能提示词编辑器",
        "WeiLinPromptUIWithoutLora": "WeiLin 提示词编辑器",
        "WeiLinPromptUIOnlyLoraStack": "WeiLin Lora堆",
    }
else:
    NODE_DISPLAY_NAME_MAPPINGS = {
        "WeiLinPromptUI": "All-Round WeiLin Prompt Editor",
        "WeiLinPromptUIWithoutLora": "WeiLin Prompt Editor",
        "WeiLinPromptUIOnlyLoraStack": "WeiLin Lora Stack",
    }

WEB_DIRECTORY = "./js_node"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

