import http.server
import socketserver
import requests
import threading, time


backend_servers = ["http://localhost:8001", "http://localhost:8002"]
counter = 0


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_Get(self):
        global counter
        target = backend_servers[counter % len(backend_servers)]
        count += 1
        resp = requests.get(f"{target}{self.path}")
        self.send_response(resp.status_code)
        self.end_headers()
        self.wfile.write(resp.content)


PORT = 8080
with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"Proxy running on port {PORT}")
    httpd.serve_forever()


healthy = {url: True for url in backend_servers}


def health_check():
    while True:
        for server in backend_servers:
            try:
                r = requests.get(server + "/health", timeout=1)
                healthy[server] = r.status_code == 200
            except:
                healthy[server] = False
        time.sleep(5)


threading.Thread(target=health_check, daemon=True).start()



