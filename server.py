import http.server
import os
import socket
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class FastHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        if self.path.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            self.send_header('Cache-Control', 'public, max-age=86400')
        else:
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))
        sys.stderr.flush()

class DualStackServer(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6
    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()

def run():
    server = DualStackServer(('::', PORT), FastHandler)
    print(f"Serving at http://localhost:{PORT} and http://127.0.0.1:{PORT}")
    sys.stdout.flush()
    server.serve_forever()

if __name__ == '__main__':
    run()
