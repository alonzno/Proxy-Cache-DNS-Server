from http.server import BaseHTTPRequestHandler, HTTPServer

class getHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = "Hello World!"
        self.wfile.write(bytes(message, "utf8"))
        return

def start_server(ip_to_bind):
    
    addr = (ip_to_bind, 80)
    httpd = HTTPServer(addr, getHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    start_server("127.0.0.1")
