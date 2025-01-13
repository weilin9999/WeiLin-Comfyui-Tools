import argparse
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse

from app.server.panel_server.tag_manager_handel import TagManagerHandler
from app.server.panel_server.server_init import FileListHandler, LanguageHandler, YamlConvertHandler

class CustomHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'x-api-key,Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_headers()
        self.end_headers()

    def do_GET(self):
        # 解析请求路径
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 处理API请求
        if path.startswith('/api/') or path.startswith('/tag/'):
            handlers = [FileListHandler(), TagManagerHandler()]
            for handler in handlers:
                if handler.handle(self):
                    return
            self.send_response(404)
            self.end_headers()
        else:
            # 处理静态文件
            self.serve_static_file(path)
        

    def serve_static_file(self, path):
        # Vue打包后的静态文件目录
        static_dir = os.path.join(os.path.dirname(__file__), 'panel_web')
        
        # 需要处理的静态文件扩展名
        static_extensions = ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf']
        
        # 检查是否是静态资源请求
        is_static_request = any(path.endswith(ext) for ext in static_extensions)
        
        try:
            # 如果是静态资源请求
            if is_static_request:
                # 处理静态资源路径
                if path.startswith('/assets/'):
                    file_path = os.path.join(static_dir, path.lstrip('/'))
                else:
                    file_path = os.path.join(static_dir, 'assets', path.lstrip('/'))
                
                if os.path.isfile(file_path):
                    self.send_response(200)
                    # 设置MIME类型
                    if file_path.endswith('.js'):
                        self.send_header('Content-Type', 'application/javascript')
                    elif file_path.endswith('.css'):
                        self.send_header('Content-Type', 'text/css')
                    elif file_path.endswith('.png'):
                        self.send_header('Content-Type', 'image/png')
                    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                        self.send_header('Content-Type', 'image/jpeg')
                    elif file_path.endswith('.gif'):
                        self.send_header('Content-Type', 'image/gif')
                    elif file_path.endswith('.svg'):
                        self.send_header('Content-Type', 'image/svg+xml')
                    elif file_path.endswith('.ico'):
                        self.send_header('Content-Type', 'image/x-icon')
                    elif file_path.endswith('.woff'):
                        self.send_header('Content-Type', 'font/woff')
                    elif file_path.endswith('.woff2'):
                        self.send_header('Content-Type', 'font/woff2')
                    elif file_path.endswith('.ttf'):
                        self.send_header('Content-Type', 'font/ttf')
                    self.end_headers()
                    
                    # 使用分块传输读取文件
                    with open(file_path, 'rb') as f:
                        while chunk := f.read(8192):  # 8KB chunks
                            self.wfile.write(chunk)
                    return True
            
            # 处理Vue路由 - 所有其他请求都返回index.html
            file_path = os.path.join(static_dir, 'index.html')
            if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):  # 8KB chunks
                        self.wfile.write(chunk)
                return True
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
                return True
        except ConnectionResetError:
            # 处理客户端断开连接的情况
            return False
        except Exception as e:
            print(f"Error serving file: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'500 Internal Server Error')
            return False

    def do_POST(self):
        handlers = [LanguageHandler(), YamlConvertHandler(), TagManagerHandler()]
        for handler in handlers:
            if handler.handle(self):
                return
        self.send_response(404)
        self.end_headers()

def main():
    parser = argparse.ArgumentParser(description="Start a custom HTTP server.")
    parser.add_argument('--port', type=int, default=9898, help='Port to run the HTTP server on')
    args = parser.parse_args()

    server_address = ('', args.port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"Starting HTTP server on port {args.port}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()