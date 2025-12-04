import pytest
from pathlib import Path
import tempfile
import yaml
from src.config import ConfigLoader, ConfigValidationError


class TestConfigLoader:
    @pytest.fixture
    def loader(self):
        return ConfigLoader()

    @pytest.fixture
    def valid_config(self):
        return {
            "endpoints": [
                {
                    "path": "/api/test",
                    "method": "GET",
                    "status": 200,
                    "response": {"message": "ok"}
                }
            ]
        }

    @pytest.fixture
    def temp_yaml_file(self, valid_config):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(valid_config, f)
            return Path(f.name)

    def test_load_valid_config(self, loader, temp_yaml_file):
        config = loader.load(temp_yaml_file)
        assert isinstance(config, dict)
        assert "endpoints" in config
        temp_yaml_file.unlink()

    def test_load_invalid_yaml(self, loader):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            path = Path(f.name)
        
        with pytest.raises(ConfigValidationError, match="Invalid YAML syntax"):
            loader.load(path)
        path.unlink()

    def test_validate_valid_config(self, loader, valid_config):
        loader.validate(valid_config)

    def test_validate_missing_endpoints(self, loader):
        with pytest.raises(ConfigValidationError, match="At least one endpoint"):
            loader.validate({"endpoints": []})

    def test_validate_invalid_method(self, loader):
        config = {
            "endpoints": [
                {"path": "/test", "method": "INVALID", "response": {}}
            ]
        }
        with pytest.raises(ConfigValidationError, match="Invalid method"):
            loader.validate(config)

    def test_validate_missing_path(self, loader):
        config = {"endpoints": [{"method": "GET", "response": {}}]}
        with pytest.raises(ConfigValidationError, match="missing required 'path'"):
            loader.validate(config)

    def test_validate_invalid_status_code(self, loader):
        config = {
            "endpoints": [
                {"path": "/test", "status": 999, "response": {}}
            ]
        }
        with pytest.raises(ConfigValidationError, match="Invalid status code"):
            loader.validate(config)

    def test_validate_invalid_content_type(self, loader):
        config = {
            "endpoints": [
                {"path": "/test", "content_type": "invalid/type", "response": {}}
            ]
        }
        with pytest.raises(ConfigValidationError, match="Unsupported content_type"):
            loader.validate(config)

    def test_validate_negative_delay(self, loader):
        config = {
            "endpoints": [
                {"path": "/test", "delay": -100, "response": {}}
            ]
        }
        with pytest.raises(ConfigValidationError, match="delay must be non-negative"):
            loader.validate(config)