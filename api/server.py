import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.engine import EclypsaEngine

engine = EclypsaEngine()

class EclypsaAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path == "/v1/health":
            self._set_headers(200)
            status = engine.health_check()
            self.wfile.write(json.dumps(status).encode("utf-8"))
        else:
            self._set_headers(404)
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_POST(self):
        if self.path == "/v1/agent/execute":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode("utf-8"))
                task = payload.get("task", "None")
                
                self._set_headers(200)
                response = {
                    "status": "accepted",
                    "task_received": task,
                    "engine_version": engine.config["version"],
                    "message": "Task queued in foundation pipeline"
                }
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON payload"}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

def run_server(host: str = None, port: int = None):
    engine.initialize()
    target_host = host or engine.config["engine"]["host"]
    target_port = port or engine.config["engine"]["port"]

    server_address = (target_host, target_port)
    httpd = HTTPServer(server_address, EclypsaAPIHandler)
    engine.logger.info(f"API Server listening on http://{target_host}:{target_port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        engine.logger.info("Stopping API server...")
        httpd.server_close()
        engine.shutdown()

if __name__ == "__main__":
    run_server()