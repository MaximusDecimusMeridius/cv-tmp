# AWS Computer Vision MCP Server

Model Context Protocol (MCP) server for computer vision tasks. This server exposes tools that analyze images with Amazon Bedrock's Claude model.

## Prerequisites

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/)
2. Install Python using `uv python install 3.10`
3. Docker installed and running

## Installation

Add the server to your MCP configuration:

```json
{
  "mcpServers": {
    "awslabs.aws-cv-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "--interactive",
        "--env",
        "FASTMCP_LOG_LEVEL=ERROR",
        "awslabs/aws-cv-mcp-server:latest"
      ]
    }
  }
}
```

## Features

- **Describe Images**: Analyze an image stored in S3 using Claude.
- **Extensible**: More computer vision tools can be added over time.

## Development

Run the tests using the provided script:

```bash
./run_tests.sh
```

This script installs `pytest` if needed and executes the test suite.
