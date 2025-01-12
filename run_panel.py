import argparse
from http.server import SimpleHTTPRequestHandler, HTTPServer

from app.server.panel_server.tag_manager_handel import TagManagerHandler

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
        handlers = [TagManagerHandler()]
        for handler in handlers:
            if handler.handle(self):
                return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        handlers = [TagManagerHandler()]
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