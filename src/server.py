from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import re

class MockHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def log_request_info(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        print(f"[{timestamp}] {self.command} {parsed.path} {dict(query)}")
    
    def match_endpoint(self):
        parsed = urlparse(self.path)
        path = parsed.path
        method = self.command
        
        for endpoint in self.server.config.get("endpoints", []):
            if endpoint.get("method", "GET") != method:
                continue
            
            pattern = endpoint.get("path", "")
            if pattern.startswith("^") or "*" in pattern:
                if re.match(pattern.replace("*", ".*"), path):
                    return endpoint
            elif pattern == path:
                return endpoint
        
        return None
    
    def substitute_params(self, text, query_params):
        if not isinstance(text, str):
            return text
        
        for key, values in query_params.items():
            placeholder = f"{{{key}}}"
            if placeholder in text:
                text = text.replace(placeholder, values[0] if values else "")
        
        return text
    
    def send_response_data(self, endpoint):
        parsed = urlparse(self.path)
        query_params = parse_qs(parsed.query)
        
        delay = endpoint.get("delay", 0)
        if delay > 0:
            time.sleep(delay / 1000.0)
        
        status = endpoint.get("status", 200)
        content_type = endpoint.get("content_type", "application/json")
        response_body = endpoint.get("response", {})
        
        if isinstance(response_body, dict):
            body_str = json.dumps(response_body)
            body_str = self.substitute_params(body_str, query_params)
            response_body = json.loads(body_str)
            body = json.dumps(response_body).encode("utf-8")
        else:
            body_str = self.substitute_params(str(response_body), query_params)
            body = body_str.encode("utf-8")
        
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def handle_request(self):
        self.log_request_info()
        endpoint = self.match_endpoint()
        
        if endpoint:
            self.send_response_data(endpoint)
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_GET(self):
        self.handle_request()
    
    def do_POST(self):
        self.handle_request()
    
    def do_PUT(self):
        self.handle_request()
    
    def do_DELETE(self):
        self.handle_request()
    
    def do_PATCH(self):
        self.handle_request()

class MockHTTPServer:
    def __init__(self, config, host="0.0.0.0", port=8080):
        self.config = config
        self.host = host
        self.port = port
        self.server = None
    
    def start(self):
        handler = MockHTTPRequestHandler
        self.server = HTTPServer((self.host, self.port), handler)
        self.server.config = self.config
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.server_close()
