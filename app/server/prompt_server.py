import os
from server import PromptServer
from aiohttp import web
from .prompt_api.lora_info import *
from .prompt_api.lora_networks import *
from .prompt_api.tags_manager import *
from .history.history_contl import *
from .history.collect_history_contl import *
from .fast_autocomplete.autocomplete import fuzzy_search
from .user_init.user_init import read_init_file, set_user_lang
from .translate.local_translate import translate_phrase
from .ai_translator.ai_translator import (
    initialize_config,
    update_openai_settings,
    add_openai_setting,
    delete_openai_setting,
    set_select_openai
)


static_path = os.path.join(os.path.dirname(__file__), "../../dist/")
dir = os.path.join(os.path.dirname(__file__), "../../dist/javascript/")
baseUrl = "/weilin/prompt_ui/api/"


@PromptServer.instance.routes.get("/weilin/prompt_ui/webjs")
async def _getWeiLinPromptUIWebJs(request):
    # 合并JS
    js = ''
    for file in os.listdir(dir):
        if file.endswith('.js'):
            with open(os.path.join(dir, file), 'r', encoding='utf-8') as f:
                js += f.read() + '\n'
    return web.Response(status=200, text=js, content_type="application/javascript")


@PromptServer.instance.routes.get("/weilin/prompt_ui/file/{file_path:.*}")
async def _getWeiLinPromptUIFile(request):
    file_path = request.match_info.get('file_path', '')
    full_path = os.path.join(static_path, file_path)
    # 检查文件路径是否存在
    if os.path.isfile(full_path):
        return web.FileResponse(full_path)
    raise web.HTTPNotFound()

# ============================================= Lora列表获取 ============================================


@PromptServer.instance.routes.get(baseUrl+"get_lora_list")
async def _get_extra_networks(request):
    return web.json_response({"data": await get_extra_networks(auto_fetch=False)})


@PromptServer.instance.routes.get(baseUrl+"get_lora_load_all")
async def _get_extra_networks_load_all(request):
    return web.json_response({"data": await get_extra_networks(auto_fetch=True)})
# =======================================================================================================

# ============================================= Lora 信息 ============================================


@PromptServer.instance.routes.post(baseUrl+'lorainfo/api/loras/info')
async def _api_save_lora_data(request):
    """Saves data to a lora by name. """
    api_response = {'status': 200}
    lora_file = get_param(request, 'file')
    if lora_file is None:
        api_response['status'] = '404'
        api_response['error'] = 'No Lora found at path'
    else:
        post = await request.post()
        await set_model_info_partial(lora_file, json.loads(post.get("json")))
        info_data = await get_model_info(lora_file)
        api_response['data'] = info_data
    return web.json_response(api_response)


@PromptServer.instance.routes.get(baseUrl+'lorainfo/api/loras/info')
async def _api_get_loras_info(request):
    """ Returns a list loras info; either all or a single if provided a 'file' param. """
    lora_file = get_param(request, 'file')
    maybe_fetch_metadata = lora_file is not None
    if not is_param_falsy(request, 'light'):
        maybe_fetch_metadata = False
    api_response = await get_loras_info_response(request, maybe_fetch_metadata=maybe_fetch_metadata)
    return web.json_response(api_response)


@PromptServer.instance.routes.get(baseUrl+'lorainfo/api/loras/info/clear')
async def _delete_lora_info(request):
    """Clears lora info from the filesystem for the provided file."""
    api_response = {'status': 200}
    lora_file = get_param(request, 'file')
    del_info = not is_param_falsy(request, 'del_info')
    del_metadata = not is_param_falsy(request, 'del_metadata')
    del_civitai = not is_param_falsy(request, 'del_civitai')
    if lora_file is None:
        api_response['status'] = '404'
        api_response['error'] = 'No Lora file provided'
    elif lora_file == "ALL":  # Force the user to supply file=ALL to trigger all clearing.
        lora_files = folder_paths.get_filename_list("loras")
        for lora_file in lora_files:
            await delete_model_info(lora_file, del_info=del_info, del_metadata=del_metadata, del_civitai=del_civitai)
    else:
        await delete_model_info(lora_file, del_info=del_info, del_metadata=del_metadata, del_civitai=del_civitai)
    return web.json_response(api_response)


@PromptServer.instance.routes.get(baseUrl+'lorainfo/api/loras/info/refresh')
async def _refresh_get_loras_info(request):
    """ Refreshes lora info; either all or a single if provided a 'file' param. """
    api_response = await get_loras_info_response(request,
                                                 maybe_fetch_civitai=True,
                                                 maybe_fetch_metadata=True)
    return web.json_response(api_response)


@PromptServer.instance.routes.get(baseUrl+'lorainfo/api/loras/img')
async def _api_get_loras_info_img(request):
    """ Returns an image response if one exists for the lora. """
    lora_file = get_param(request, 'file')
    lora_path = folder_paths.get_full_path("loras", lora_file)
    if not path_exists(lora_path):
        lora_path = os.path.abspath(lora_path)

    img_path = None
    for ext in ['jpg', 'png', 'jpeg', 'gif']:
        try_path = f'{os.path.splitext(lora_path)[0]}.{ext}'
        if path_exists(try_path):
            img_path = try_path
            break

    if not path_exists(img_path):
        api_response = {}
        api_response['status'] = '404'
        api_response['error'] = 'No Lora found at path'
        return web.json_response(api_response)

    return web.FileResponse(img_path)


@PromptServer.instance.routes.post(baseUrl+'lorainfo/api/loras/set/img')
async def _upload_image(request):
    post = await request.post()
    data = image_upload(post)
    return web.json_response(data)
# ======================================================================================================================

# ================================= Tag管理 =================================


@PromptServer.instance.routes.get(baseUrl+"prompt/get_group_tags")
async def _get_group_tags(request):
    return web.json_response({"data": get_group_tags()})


@PromptServer.instance.routes.post(baseUrl+"prompt/add_new_f_group")
async def _add_new_s_group(request):
    data = await request.json()
    resp = {"code":202}
    try:
       resp = add_new_node_group(data['name'], data['color'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response(resp)


@PromptServer.instance.routes.post(baseUrl+"prompt/edit_f_group")
async def _edit_s_group(request):
    data = await request.json()
    resp = {"code":202}
    try:
        resp = edit_node_group(data['id_index'], data['name'], data['color'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response(resp)


@PromptServer.instance.routes.post(baseUrl+"prompt/delete_f_group")
async def _delete_s_group(request):
    data = await request.json()
    try:
        delete_node_group(data['id_index'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/add_new_s_group")
async def _add_new_s_group(request):
    data = await request.json()
    resp = {"code":202}
    try:
        resp = add_new_group(data['key'], data['name'], data['color'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response(resp)


@PromptServer.instance.routes.post(baseUrl+"prompt/edit_s_group")
async def _edit_new_s_group(request):
    data = await request.json()
    resp = {"code":202}
    try:
        resp = edit_child_node_group(data['id_index'], data['name'], data['color'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response(resp)


@PromptServer.instance.routes.post(baseUrl+"prompt/delete_s_group")
async def _delete_new_s_group(request):
    data = await request.json()
    try:
        delete_child_node_group(data['id_index'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/new_tags")
async def _new_tags(request):
    data = await request.json()
    try:
        add_group_tag(data['text'], data['desc'],
                      data['id_index'], data['color'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/edit_tags")
async def _edit_tags(request):
    data = await request.json()
    try:
        edit_group_tag(data['text'], data['desc'],
                       data['id_index'], data['color'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/delete_tags")
async def _delete_tags(request):
    data = await request.json()
    try:
        delete_group_tag(data['id_index'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/batch_delete_tags")
async def _batch_delete_tags(request):
    data = await request.json()
    try:
        batch_delete_group_tags(data['id_indexs'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/move_tag")
async def _move_tag(request):
    data = await request.json()
    try:
        result = move_tag(data['id_index'],
                          data['reference_id_index'], data['position'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": result})

# =====================================================================================================

# ================================= 历史记录功能 =================================


@PromptServer.instance.routes.get(baseUrl+"prompt/history/get_history")
async def _get_history(request):
    try:
        data = read_history()
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"data": data})


@PromptServer.instance.routes.post(baseUrl+"prompt/history/add_history")
async def _add_history(request):
    data = await request.json()
    try:
        new_entry = add_history(data['tag'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"data": new_entry})


@PromptServer.instance.routes.post(baseUrl+"prompt/history/delete_history")
async def _delete_history(request):
    data = await request.json()
    try:
        delete_info = delete_history(data['id_index'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": delete_info})


@PromptServer.instance.routes.post(baseUrl+"prompt/history/batch_delete_history")
async def _batch_delete_history(request):
    data = await request.json()
    try:
        delete_info = batch_delete_history(data['id_index'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": delete_info})

# =====================================================================================================

# ================================= 收藏历史记录功能 =================================


@PromptServer.instance.routes.get(baseUrl+"prompt/collect_history/get_collect_history")
async def _get_collect_history(request):
    try:
        data = read_collect_history()
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"data": data})


@PromptServer.instance.routes.post(baseUrl+"prompt/collect_history/add_collect_history")
async def _add_collect_history(request):
    data = await request.json()
    try:
        new_entry = add_collect_history(
            data['tag'], data.get('name', ""), data.get('color', ""))
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"data": new_entry})


@PromptServer.instance.routes.post(baseUrl+"prompt/collect_history/delete_collect_history")
async def _delete_collect_history(request):
    data = await request.json()
    try:
        delete_info = delete_collect_history(data['id_index'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": delete_info})


@PromptServer.instance.routes.post(baseUrl+"prompt/collect_history/batch_delete_collect_history")
async def _batch_delete_collect_history(request):
    data = await request.json()
    try:
        delete_info = batch_delete_collect_history(data['id_indices'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": delete_info})


@PromptServer.instance.routes.post(baseUrl+"prompt/collect_history/edit_collect_history")
async def _edit_collect_history(request):
    data = await request.json()
    try:
        edit_info = edit_collect_history(data['id_index'], data.get(
            'name'), data.get('color'), data.get('tag'))
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": edit_info})

# =====================================================================================================

# ================================= 用户初始化设置 =================================


@PromptServer.instance.routes.get(baseUrl+"user_init/get_settings")
async def _get_user_settings(request):
    try:
        data = read_init_file()
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"data": data})


@PromptServer.instance.routes.post(baseUrl+"user_init/set_user_lang")
async def _set_user_lang(request):
    data = await request.json()
    try:
        set_user_lang(data['user_lang'])
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"info": 'ok'})
# =====================================================================================================

# ================================= 翻译功能 =================================


@PromptServer.instance.routes.post(baseUrl+"prompt/local/translate")
async def _translate_phrase(request):
    data = await request.json()
    phrase = data.get('phrase', '')
    try:
        translated = translate_phrase(phrase)
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"original": phrase, "translated": translated})
# =====================================================================================================

# ================================= 快速补全功能 =================================


@PromptServer.instance.routes.post(baseUrl+"prompt/fast/autocomplete")
async def _autocomplete(request):
    data = await request.json()
    query = data.get('query', '')
    try:
        results = fuzzy_search(query)
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)

    return web.json_response({"data": results})
# =====================================================================================================

# ================================= OpenAI 功能 =================================


@PromptServer.instance.routes.get(baseUrl+"prompt/openai/get_settings")
async def _get_openai_setting(request):
    return  web.json_response({"data":initialize_config()})


@PromptServer.instance.routes.post(baseUrl+"prompt/openai/update_settings")
async def _update_openai_settings(request):
    data = await request.json()
    index = data.get('index')
    api_key = data.get('api_key')
    base_url = data.get('base_url')
    model = data.get('model')
    try:
        update_openai_settings(index, api_key, base_url, model)
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)
    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/openai/add_setting")
async def _add_openai_setting(request):
    data = await request.json()
    api_key = data.get('api_key')
    base_url = data.get('base_url')
    model = data.get('model')
    try:
        add_openai_setting(api_key, base_url, model)
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)
    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/openai/delete_setting")
async def _delete_openai_setting(request):
    data = await request.json()
    index = data.get('index')
    try:
        delete_openai_setting(index)
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)
    return web.json_response({"info": 'ok'})


@PromptServer.instance.routes.post(baseUrl+"prompt/openai/set_select")
async def _set_select_openai(request):
    data = await request.json()
    index = data.get('index')
    try:
        set_select_openai(index)
    except Exception as e:
        print(f"Error: {e}")
        return web.Response(status=500)
    return web.json_response({"info": 'ok'})
# =====================================================================================================

# =================================== 启动面板 无法实现 暂时不考虑 =============================================
@PromptServer.instance.routes.post(baseUrl+"panel/start")
async def _start_panel(request):
    try:
        return web.json_response({"status": "success", "message": f"Panel started on port 9898"})
    except Exception as e:
        print(f"Error starting panel: {e}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)
# =====================================================================================================


print("======== WeiLin插件服务已启动 ========")
print("======== WeiLin Server Init ========")
