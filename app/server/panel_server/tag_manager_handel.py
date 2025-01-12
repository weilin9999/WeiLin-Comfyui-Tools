import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler
from .tag_manager import (
    add_tag_group,
    edit_tag_group,
    delete_tag_group,
    get_tag_groups,
    add_tag_subgroup,
    edit_tag_subgroup,
    delete_tag_subgroup,
    get_tag_subgroups,
    add_tag,
    edit_tag,
    delete_tag,
    get_tags,
    move_tag_group,
    move_tag_subgroup,
    move_tag
)

class TagManagerHandler:
    def _set_headers(self, handler):
        handler.send_header('Content-type', 'application/json')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        handler.send_header('Access-Control-Allow-Headers', 'x-api-key,Content-Type')

    def handle(self, handler: BaseHTTPRequestHandler):
        parsed_path = urlparse(handler.path)
        if handler.command == 'GET':
            if parsed_path.path == '/tag/get_tag_groups':
                handler.send_response(200)
                self._set_headers(handler)
                handler.end_headers()
                data = get_tag_groups()
                response = json.dumps({"data": json.loads(data)})
                handler.wfile.write(response.encode())
            elif parsed_path.path == '/tag/get_tag_subgroups':
                query_params = parse_qs(parsed_path.query)
                group_id = query_params.get('group_id', [None])[0]
                if group_id:
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    data = get_tag_subgroups(group_id)
                    response = json.dumps({"data": json.loads(data)})
                    handler.wfile.write(response.encode())
                else:
                    handler.send_response(400)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": "Missing group_id parameter"}).encode())
            elif parsed_path.path == '/tag/get_tags':
                query_params = parse_qs(parsed_path.query)
                subgroup_id = query_params.get('subgroup_id', [None])[0]
                if subgroup_id:
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    data = get_tags(subgroup_id)
                    response = json.dumps({"data": json.loads(data)})
                    handler.wfile.write(response.encode())
                else:
                    handler.send_response(400)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": "Missing subgroup_id parameter"}).encode())
            else:
                return False  # Not handled by this handler
        elif handler.command == 'POST':
            content_length = int(handler.headers['Content-Length'])
            post_data = handler.rfile.read(content_length)
            data = json.loads(post_data)

            if parsed_path.path == '/tag/add_tag_group':
                try:
                    add_tag_group(data['name'], data['color'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/edit_tag_group':
                try:
                    edit_tag_group(data['id_index'], data['name'], data['color'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/delete_tag_group':
                try:
                    delete_tag_group(data['id_index'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/add_tag_subgroup':
                try:
                    add_tag_subgroup(data['group_id'], data['name'], data['color'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/edit_tag_subgroup':
                try:
                    edit_tag_subgroup(data['id_index'], data['name'], data['color'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/delete_tag_subgroup':
                try:
                    delete_tag_subgroup(data['id_index'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/add_tag':
                try:
                    add_tag(data['subgroup_id'], data['text'], data['desc'], data['color'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/edit_tag':
                try:
                    edit_tag(data['id_index'], data['text'], data['desc'], data['color'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/delete_tag':
                try:
                    delete_tag(data['id_index'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/move_tag_group':
                try:
                    move_tag_group(data['id_index'], data['reference_id_index'], data['position'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/move_tag_subgroup':
                try:
                    move_tag_subgroup(data['id_index'], data['reference_id_index'], data['position'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            elif parsed_path.path == '/tag/move_tag':
                try:
                    move_tag(data['id_index'], data['reference_id_index'], data['position'])
                    handler.send_response(200)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"info": 'ok'}).encode())
                except Exception as e:
                    handler.send_response(500)
                    self._set_headers(handler)
                    handler.end_headers()
                    handler.wfile.write(json.dumps({"error": str(e)}).encode())

            else:
                return False  # Not handled by this handler
        else:
            return False  # Not handled by this handler

        return True  # Handled by this handler