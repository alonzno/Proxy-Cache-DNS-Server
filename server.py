from http.server import BaseHTTPRequestHandler, HTTPServer

class getHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.path = self.path.replace("http://", "")
        self.path = "/" + self.path.partition("/")[2]
        print("Path", self.path)
        if self.path == "/":
            f = open("./www/index.html", "rb")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())
            return
        if self.path == "/video.mp4":
            f = open("./www/video.mp4", "rb")
            self.send_response(200)
            self.send_header("Content-type", "video/mp4")
            self.send_header("Keep-Alive", ["timeout=30", "max=0"])
            self.end_headers()
            self.wfile.write(f.read())
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = "Didn't Have the file"
        self.wfile.write(bytes(message, "utf8"))
        return

def start_server(ip_to_bind):
    try: 
        addr = (ip_to_bind, 80)
        httpd = HTTPServer(addr, getHandler)
        httpd.serve_forever()
    except:
        pass

if __name__ == "__main__":
    start_server("127.0.0.1")
