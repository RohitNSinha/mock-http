import yaml
from pathlib import Path
from typing import Dict, Any, List

class ConfigValidationError(Exception):
    pass

class ConfigLoader:
    VALID_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    VALID_CONTENT_TYPES = [
        "application/json",
        "text/plain",
        "text/html",
        "application/xml"
    ]
    
    def load(self, path: Path) -> Dict[str, Any]:
        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
            return config or {}
        except yaml.YAMLError as e:
            raise ConfigValidationError(f"Invalid YAML syntax: {e}")
        except Exception as e:
            raise ConfigValidationError(f"Failed to load config: {e}")
    
    def validate(self, config: Dict[str, Any]) -> None:
        if not isinstance(config, dict):
            raise ConfigValidationError("Config must be a dictionary")
        
        endpoints = config.get("endpoints", [])
        if not isinstance(endpoints, list):
            raise ConfigValidationError("'endpoints' must be a list")
        
        if not endpoints:
            raise ConfigValidationError("At least one endpoint must be defined")
        
        for idx, endpoint in enumerate(endpoints):
            self._validate_endpoint(endpoint, idx)
    
    def _validate_endpoint(self, endpoint: Dict[str, Any], idx: int) -> None:
        if not isinstance(endpoint, dict):
            raise ConfigValidationError(f"Endpoint {idx} must be a dictionary")
        
        if "path" not in endpoint:
            raise ConfigValidationError(f"Endpoint {idx} missing required 'path'")
        
        method = endpoint.get("method", "GET")
        if method not in self.VALID_METHODS:
            raise ConfigValidationError(
                f"Endpoint {idx}: Invalid method '{method}'. "
                f"Valid methods: {', '.join(self.VALID_METHODS)}"
            )
        
        if "response" not in endpoint:
            raise ConfigValidationError(f"Endpoint {idx} missing 'response'")
        
        status = endpoint.get("status", 200)
        if not isinstance(status, int) or status < 100 or status > 599:
            raise ConfigValidationError(
                f"Endpoint {idx}: Invalid status code {status}"
            )
        
        content_type = endpoint.get("content_type", "application/json")
        if content_type not in self.VALID_CONTENT_TYPES:
            raise ConfigValidationError(
                f"Endpoint {idx}: Unsupported content_type '{content_type}'"
            )
        
        delay = endpoint.get("delay", 0)
        if not isinstance(delay, (int, float)) or delay < 0:
            raise ConfigValidationError(
                f"Endpoint {idx}: delay must be non-negative number"
            )
