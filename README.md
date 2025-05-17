# AWS Computer Vision Agent

This agent uses the Computer Vision MCP server to analyze images with Amazon Bedrock's Claude model. It is a minimal example today with a single tool but can be extended with additional vision features.

## Prerequisites

1. Python 3.11 or later
2. Docker installed and running
3. AWS credentials configured
4. Perplexity API key (optional)

## Setup

1. Install the required dependencies:
```bash
pip install -e ../amazon-bedrock-agent-samples/src/InlineAgent
```

2. Set up your environment variables in a `.env` file:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
BEDROCK_LOG_GROUP_NAME=your_log_group
PERPLEXITY_API_KEY=your_perplexity_key
```

3. Build the computer vision MCP server Docker image:
```bash
cd aws-cv-mcp-server
docker build -t awslabs/aws-cv-mcp-server:latest .
```

## Usage

Run the agent:
```bash
python main.py
```

The agent can:
1. Analyze images using the computer vision tool
2. Provide additional context using Perplexity search
3. Perform data analysis and visualization using the code interpreter

## Example Query
- "What's in image `image001.png`?"

## Running Tests
Run `bash aws-cv-mcp-server/run_tests.sh` to execute the unit tests. The script installs dependencies and uses mocks so AWS credentials are not required.

## Notes

- The agent uses Claude 3.5 Sonnet as the foundation model
- Image analysis is powered by the AWS Computer Vision MCP server
- Additional context is provided by Perplexity search
