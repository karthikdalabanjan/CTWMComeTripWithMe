import http.server
import socketserver
import os
import sys

PORT = int(os.environ.get("PORT", 3000))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("======================================================")
            print("✨ ComeTripWithMe Local Web Server is Running!")
            print(f"🔗 Access App at: http://localhost:{PORT}")
            print(f"⚙️ Master Controller: {os.path.join(DIRECTORY, 'index.html')}")
            print("======================================================")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48: # Address already in use
            alt_port = PORT + 1
            print(f"Port {PORT} in use, trying port {alt_port}...")
            with socketserver.TCPServer(("", alt_port), Handler) as httpd:
                print("======================================================")
                print("✨ ComeTripWithMe Local Web Server is Running!")
                print(f"🔗 Access App at: http://localhost:{alt_port}")
                print("======================================================")
                httpd.serve_forever()
        else:
            raise e

if __name__ == "__main__":
    run()
