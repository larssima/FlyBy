"""
FlyBy local server — replaces `python -m http.server`

Serves index.html + remote.html and provides a JSON command bus so an
iPhone on the same network can control the radar display.

  python server.py        → http://localhost:8080
  http://<pi-ip>:8080     → radar display
  http://<pi-ip>:8080/remote → iPhone remote control
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, threading

_lock     = threading.Lock()
_cmd      = None   # one pending command at a time (latest wins)
_state    = {}     # latest aircraft state pushed by the radar

class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/api/cmd':
            global _cmd
            with _lock:
                payload, _cmd = _cmd or {}, None
            self._json(payload)

        elif self.path == '/api/aircraft':
            with _lock:
                data = dict(_state)
            self._json(data)

        elif self.path in ('/remote', '/remote/'):
            self.path = '/remote.html'
            super().do_GET()

        else:
            super().do_GET()

    def do_POST(self):
        global _cmd, _state
        length = int(self.headers.get('Content-Length', 0))
        body   = json.loads(self.rfile.read(length) or b'{}')

        if self.path == '/api/cmd':
            with _lock:
                _cmd = body
            self._json({'ok': True})

        elif self.path == '/api/aircraft':
            with _lock:
                _state = body
            self._json({'ok': True})

        else:
            self.send_error(404)

    def _json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # Only log API calls, not every static file request
        if '/api/' in args[0] if args else False:
            super().log_message(fmt, *args)


if __name__ == '__main__':
    port = 8080
    print(f'FlyBy running at http://localhost:{port}')
    print(f'Remote control:  http://localhost:{port}/remote')
    print('(On your network, replace localhost with your IP address)')
    HTTPServer(('', port), Handler).serve_forever()
