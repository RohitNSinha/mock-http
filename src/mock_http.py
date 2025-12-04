#!/usr/bin/env python3
import argparse
import sys
import signal
from pathlib import Path
from .server import MockHTTPServer
from .config import ConfigLoader

def signal_handler(signum, frame):
    print("\nShutting down gracefully...")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Lightweight HTTP mock server for API testing"
    )
    parser.add_argument(
        "config",
        type=str,
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8080,
        help="Port to run server on (default: 8080)"
    )
    parser.add_argument(
        "-h", "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    args = parser.parse_args()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Config file not found: {args.config}")
        sys.exit(1)
    
    try:
        loader = ConfigLoader()
        config = loader.load(config_path)
        loader.validate(config)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)
    
    server = MockHTTPServer(config, args.host, args.port)
    print(f"Mock HTTP server running on {args.host}:{args.port}")
    print(f"Loaded {len(config.get('endpoints', []))} endpoints")
    server.start()

if __name__ == "__main__":
    main()
