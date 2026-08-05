from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_health_check_server():
    # Back4app uses HTTP, so bind to standard HTTP logic on the requested port
    server_address = ('0.0.0.0', 443)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    # print("Health check server running on port 443...")
    httpd.serve_forever()
