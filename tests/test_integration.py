import pytest
import tempfile
import yaml
from pathlib import Path
import threading
import time
import requests
from src.server import MockHTTPServer
from src.config import ConfigLoader


class TestIntegration:
    @pytest.fixture
    def test_config(self):
        return {
            "endpoints": [
                {
                    "path": "/api/users",
                    "method": "GET",
                    "status": 200,
                    "content_type": "application/json",
                    "response": {"users": [{"id": 1, "name": "Test"}]}
                },
                {
                    "path": "/api/greet",
                    "method": "GET",
                    "status": 200,
                    "response": {"message": "Hello {name}!"}
                },
                {
                    "path": "/health",
                    "method": "GET",
                    "status": 200,
                    "content_type": "text/plain",
                    "response": "OK"
                }
            ]
        }

    @pytest.fixture
    def running_server(self, test_config):
        server = MockHTTPServer(test_config, "127.0.0.1", 9999)
        thread = threading.Thread(target=server.start, daemon=True)
        thread.start()
        time.sleep(0.5)
        yield server
        server.server.shutdown()

    def test_get_json_endpoint(self, running_server):
        response = requests.get("http://127.0.0.1:9999/api/users")
        assert response.status_code == 200
        assert response.json()["users"][0]["name"] == "Test"

    def test_query_param_substitution(self, running_server):
        response = requests.get("http://127.0.0.1:9999/api/greet?name=Alice")
        assert response.status_code == 200
        assert "Hello Alice!" in response.json()["message"]

    def test_text_plain_response(self, running_server):
        response = requests.get("http://127.0.0.1:9999/health")
        assert response.status_code == 200
        assert response.text == "OK"

    def test_404_not_found(self, running_server):
        response = requests.get("http://127.0.0.1:9999/nonexistent")
        assert response.status_code == 404

    def test_config_loader_end_to_end(self, test_config):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_config, f)
            path = Path(f.name)
        
        loader = ConfigLoader()
        config = loader.load(path)
        loader.validate(config)
        assert len(config["endpoints"]) == 3
        path.unlink()