# 🚀 mock-http - Simple HTTP Mock Server for Easy Testing 

[![Download mock-http](https://img.shields.io/badge/Download-mock--http-blue.svg)](https://github.com/RohitNSinha/mock-http/releases)

## 📖 Overview

mock-http is a lightweight HTTP mock server designed to help you test your API clients quickly. It is easy to configure using a YAML file, allowing users to simulate API responses without needing a real server. This tool provides a fast and simple way to create mock servers for your development and testing needs.

## ⚙️ Features

- **YAML Configuration**: Easily define your mock server responses with simple YAML files.
- **Multiple Endpoints**: Mock multiple API endpoints, providing flexibility for your tests.
- **Lightweight**: Fast startup and low resource usage for efficient testing.
- **Easy to Use**: Designed for all users, even those without technical backgrounds.

## 🔧 System Requirements

- **Operating System**: Compatible with Windows, macOS, and Linux.
- **Python Version**: Python 3.6 or higher must be installed on your machine.
- **Network Access**: Ensure you have internet access for downloading dependencies.

## 🚀 Getting Started

Follow these steps to download and run mock-http on your machine.

### 📥 Download & Install

1. Visit the [Releases page](https://github.com/RohitNSinha/mock-http/releases) to download mock-http.
2. Locate the latest release. Download the appropriate file for your operating system.
3. Follow the installation instructions specific to your platform.

### 🖥️ How to Run

1. After downloading, extract the files if needed.
2. Open your terminal or command prompt.
3. Navigate to the folder where you downloaded mock-http.
4. Run the command to start the server, such as:
   ```bash
   python mock-http.py <your-yaml-file>.yaml
   ```
5. The server will start, and you can now access your mocked API endpoints.

### 📁 YAML Configuration Example

To help you get started with YAML configurations, here’s an example:

```yaml
mock:
  - url: /api/users
    method: GET
    response:
      status: 200
      body:
        - id: 1
          name: "John Doe"
        - id: 2
          name: "Jane Smith"
```

This configuration mocks a GET request to the `/api/users` endpoint and returns a list of users.

## 📜 Documentation

For detailed documentation, you can refer to the [GitHub Wiki](https://github.com/RohitNSinha/mock-http/wiki). It contains comprehensive guides on various features, advanced configurations, and troubleshooting tips.

## 🛠️ Support

If you encounter issues or have questions, please open an issue in the [Issues section](https://github.com/RohitNSinha/mock-http/issues) of this repository. We’re here to help!

## 🔗 Additional Resources

- [Read the Documentation](https://github.com/RohitNSinha/mock-http/wiki)
- [Visit the Releases page](https://github.com/RohitNSinha/mock-http/releases) to download the latest version.

[![Download mock-http](https://img.shields.io/badge/Download-mock--http-blue.svg)](https://github.com/RohitNSinha/mock-http/releases)

With mock-http, you can streamline your API testing process and ensure smooth interactions. Enjoy testing!