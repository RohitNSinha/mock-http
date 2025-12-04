import pytest
import json
import time
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
from src.server import MockHTTPRequestHandler, MockHTTPServer


class TestMockHTTPRequestHandler:
    @pytest.fixture
    def handler(self):
        request = Mock()
        request.makefile = Mock(return_value=BytesIO(b"GET / HTTP/1.1\r\n\r\n"))
        client_address = ('127.0.0.1', 12345)
        server = Mock()
        server.config = {
            "endpoints": [
                {
                    "path": "/api/test",
                    "method": "GET",
                    "status": 200,
                    "response": {"message": "success"}
                }
            ]
        }
        handler = MockHTTPRequestHandler(request, client_address, server)
        handler.wfile = BytesIO()
        return handler

    def test_match_endpoint_exact_path(self, handler):
        handler.path = "/api/test"
        handler.command = "GET"
        endpoint = handler.match_endpoint()
        assert endpoint is not None
        assert endpoint["path"] == "/api/test"

    def test_match_endpoint_not_found(self, handler):
        handler.path = "/nonexistent"
        handler.command = "GET"
        endpoint = handler.match_endpoint()
        assert endpoint is None

    def test_match_endpoint_wrong_method(self, handler):
        handler.path = "/api/test"
        handler.command = "POST"
        endpoint = handler.match_endpoint()
        assert endpoint is None

    def test_substitute_params_simple(self, handler):
        text = "Hello {name}!"
        query_params = {"name": ["World"]}
        result = handler.substitute_params(text, query_params)
        assert result == "Hello World!"

    def test_substitute_params_no_match(self, handler):
        text = "Hello {name}!"
        query_params = {"other": ["value"]}
        result = handler.substitute_params(text, query_params)
        assert result == "Hello {name}!"

    @patch('time.sleep')
    def test_send_response_with_delay(self, mock_sleep, handler):
        endpoint = {
            "path": "/test",
            "delay": 1000,
            "status": 200,
            "response": {"ok": True}
        }
        handler.path = "/test"
        handler.send_response_data(endpoint)
        mock_sleep.assert_called_once_with(1.0)

    def test_send_response_json(self, handler):
        endpoint = {
            "path": "/test",
            "status": 200,
            "content_type": "application/json",
            "response": {"data": "value"}
        }
        handler.path = "/test"
        handler.send_response = Mock()
        handler.send_header = Mock()
        handler.end_headers = Mock()
        handler.send_response_data(endpoint)
        handler.send_response.assert_called_with(200)

    def test_send_response_text(self, handler):
        endpoint = {
            "path": "/test",
            "status": 200,
            "content_type": "text/plain",
            "response": "Plain text response"
        }
        handler.path = "/test"
        handler.send_response = Mock()
        handler.send_header = Mock()
        handler.end_headers = Mock()
        handler.send_response_data(endpoint)
        body = handler.wfile.getvalue()
        assert b"Plain text response" in body


class TestMockHTTPServer:
    def test_server_initialization(self):
        config = {"endpoints": []}
        server = MockHTTPServer(config, "127.0.0.1", 8080)
        assert server.config == config
        assert server.server is not None