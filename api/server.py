import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.engine import EclypsaEngine
from plugins.loader import PluginLoader

engine = EclypsaEngine()
plugin_loader = PluginLoader()

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECLYPSA AI - Control Center</title>
    <style>
        :root { --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9; --accent: #58a6ff; --green: #238636; }
        body { font-family: monospace; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 15px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 15px; }
        h3 { margin-top: 0; color: var(--accent); }
        input, button, textarea { width: 100%; background: #010409; border: 1px solid var(--border); color: #fff; padding: 10px; border-radius: 4px; box-sizing: border-box; font-family: monospace; }
        button { background: var(--green); cursor: pointer; font-weight: bold; margin-top: 10px; }
        pre { background: #010409; padding: 10px; border-radius: 4px; overflow-x: auto; color: #7ee787; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>ECLYPSA AI // Operational Dashboard</h2>
            <span style="color:#7ee787;">● SYSTEM ONLINE</span>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>Agent Dispatcher</h3>
                <label>Enter Security Task / Query:</label>
                <textarea id="taskInput" rows="4" placeholder="Perform a port scan on target 127.0.0.1..."></textarea>
                <button onclick="runTask()">Dispatch Agent</button>
            </div>
            <div class="card">
                <h3>Loaded Plugins</h3>
                <div id="pluginList">Loading plugins...</div>
            </div>
        </div>

        <div class="card" style="margin-top: 20px;">
            <h3>Execution Telemetry & Output</h3>
            <pre id="outputLog">Awaiting command execution...</pre>
        </div>
    </div>

    <script>
        async function fetchPlugins() {
            try {
                const res = await fetch('/v1/plugins');
                const data = await res.json();
                document.getElementById('pluginList').innerHTML = Object.keys(data).map(p => `<div>⚡ <b>${p}</b> (Status: Active)</div>`).join('') || 'No plugins loaded';
            } catch(e) { document.getElementById('pluginList').innerText = 'Failed to load plugins.'; }
        }

        async function runTask() {
            const task = document.getElementById('taskInput').value;
            const log = document.getElementById('outputLog');
            log.innerText = "[*] Dispatching task to ECLYPSA AI Engine...";
            try {
                const res = await fetch('/v1/agent/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ task: task })
                });
                const result = await res.json();
                log.innerText = JSON.stringify(result, null, 2);
            } catch (e) { log.innerText = "[X] Error connecting to API Gateway: " + e; }
        }
        fetchPlugins();
    </script>
</body>
</html>
"""

class EclypsaAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path in ["/", "/dashboard"]:
            self._set_headers(200, "text/html")
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
        elif self.path == "/v1/health":
            self._set_headers(200)
            status = engine.health_check()
            self.wfile.write(json.dumps(status).encode("utf-8"))
        elif self.path == "/v1/plugins":
            self._set_headers(200)
            loaded = plugin_loader.discover_and_load()
            res = {k: v.get_metadata() for k, v in loaded.items()}
            self.wfile.write(json.dumps(res).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def do_POST(self):
        if self.path == "/v1/agent/execute":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode("utf-8"))
                task = payload.get("task", "None")
                
                self._set_headers(200)
                response = {
                    "status": "success",
                    "task_received": task,
                    "engine_version": engine.config["version"],
                    "telemetry": "Task processed via Core Pipeline"
                }
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON payload"}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

def run_server(host: str = "0.0.0.0", port: int = 8080):
    engine.initialize()
    server_address = (host, port)
    httpd = HTTPServer(server_address, EclypsaAPIHandler)
    engine.logger.info(f"API & Dashboard listening on http://{host}:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        engine.logger.info("Stopping server...")
        httpd.server_close()
        engine.shutdown()

if __name__ == "__main__":
    run_server()