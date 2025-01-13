import os
import json
from http.server import BaseHTTPRequestHandler
from app.server.dao.dao import set_language
from app.server.panel_server.ymal_utils import mergerDataToDb

class FileListHandler:
    def __init__(self, directory='user_data'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, f'../../../user_data')
        self.directory = db_path

    def handle(self, request_handler: BaseHTTPRequestHandler):
        if request_handler.path == '/api/file_list':
            file_list = self.get_file_list()
            response = json.dumps({"data": file_list})
            request_handler.send_response(200)
            request_handler.send_header('Content-type', 'application/json')
            request_handler.send_header('Access-Control-Allow-Origin', '*')
            request_handler.end_headers()
            request_handler.wfile.write(response.encode('utf-8'))
            return True
        return False

    def get_file_list(self):
        file_list = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append({
                    'path': file_path,
                    'name': file
                })
        return file_list

class LanguageHandler:
    def _set_headers(self, handler):
        handler.send_header('Content-type', 'application/json')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        handler.send_header('Access-Control-Allow-Headers', 'x-api-key,Content-Type')

    def handle(self, request_handler: BaseHTTPRequestHandler):
        if request_handler.path == '/api/set_language':
            if request_handler.command == 'OPTIONS':
                self.handle_options(request_handler)
                return True
            elif request_handler.command == 'POST':
                self.handle_post(request_handler)
                return True
        return False

    def handle_options(self, request_handler: BaseHTTPRequestHandler):
        request_handler.send_response(200)
        self._set_headers(request_handler)
        request_handler.end_headers()

    def handle_post(self, request_handler: BaseHTTPRequestHandler):
        try:
            content_length = int(request_handler.headers['Content-Length'])
            post_data = request_handler.rfile.read(content_length)
            # 确保读取到的数据是字符串
            post_data = post_data.decode('utf-8')
            data = json.loads(post_data)
            name = data.get("name")

            if name:
                try:
                    set_language(name)
                    response = json.dumps({"status": "success"})
                    request_handler.send_response(200)
                except FileNotFoundError as e:
                    response = json.dumps({"status": "error", "message": str(e)})
                    request_handler.send_response(404)
                except Exception as e:
                    response = json.dumps({"status": "error", "message": str(e)})
                    request_handler.send_response(500)
            else:
                response = json.dumps({"status": "error", "message": "Missing 'name' parameter"})
                request_handler.send_response(400)

            self._set_headers(request_handler)
            request_handler.end_headers()
            request_handler.wfile.write(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling request: {e}")
            request_handler.send_response(500)
            self._set_headers(request_handler)
            request_handler.end_headers()
            response = json.dumps({"status": "error", "message": str(e)})
            request_handler.wfile.write(response.encode('utf-8'))

class YamlConvertHandler:
    def _set_headers(self, handler):
        handler.send_header('Content-type', 'application/json')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        handler.send_header('Access-Control-Allow-Headers', 'x-api-key,Content-Type')

    def handle(self, request_handler: BaseHTTPRequestHandler):
        if request_handler.path == '/api/convert_yaml':
            if request_handler.command == 'OPTIONS':
                self.handle_options(request_handler)
                return True
            elif request_handler.command == 'POST':
                self.handle_post(request_handler)
                return True
        return False

    def handle_options(self, request_handler: BaseHTTPRequestHandler):
        request_handler.send_response(200)
        self._set_headers(request_handler)
        request_handler.end_headers()

    def handle_post(self, request_handler: BaseHTTPRequestHandler):
        try:
            content_length = int(request_handler.headers['Content-Length'])
            post_data = request_handler.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            yaml_file = data.get("yaml_file")
            
            if not yaml_file:
                response = json.dumps({"status": "error", "message": "Missing yaml_file parameter"})
                request_handler.send_response(400)
            else:
                try:
                    mergerDataToDb(yaml_file)
                    response = json.dumps({"status": "success"})
                    request_handler.send_response(200)
                except Exception as e:
                    response = json.dumps({"status": "error", "message": str(e)})
                    request_handler.send_response(500)
            
            self._set_headers(request_handler)
            request_handler.end_headers()
            request_handler.wfile.write(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling request: {e}")
            request_handler.send_response(500)
            self._set_headers(request_handler)
            request_handler.end_headers()
            response = json.dumps({"status": "error", "message": str(e)})
            request_handler.wfile.write(response.encode('utf-8'))