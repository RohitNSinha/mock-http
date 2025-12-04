# mock-http

Lightweight HTTP mock server configured via YAML for quick API client testing

## Features

- Parse YAML configuration file defining endpoints, methods, and responses
- Start HTTP server on configurable port (default 8080)
- Match incoming requests to configured endpoints by path and method
- Return predefined JSON or text responses with custom status codes
- Support response delays to simulate network latency or timeouts
- Log all incoming requests to stdout with timestamp, method, path, and query params
- Support dynamic responses based on query parameters (simple variable substitution)
- Handle multiple content types (application/json, text/plain, text/html)
- Validate YAML config on startup with helpful error messages
- Graceful shutdown on SIGINT/SIGTERM

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/mock-http.git
cd mock-http

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python

## Dependencies

- `pyyaml`
- `pytest`
- `pytest-cov`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
