from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        device_code = query.get('device_code', [None])[0]

        if not device_code or not device_code.isdigit():
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid code'}).encode('utf-8'))
            return

        seed = int(device_code)
        reset_code = (seed ^ 0x5A5A) % 10000

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {'reset_code': f"{reset_code:04d}"}
        self.wfile.write(json.dumps(response).encode('utf-8'))
