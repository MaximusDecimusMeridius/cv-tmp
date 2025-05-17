# AWS Cost Explorer and Diagram Agent

This agent combines the capabilities of AWS Cost Explorer and AWS Diagram MCP servers to provide a powerful tool for analyzing AWS costs and creating architecture diagrams.

## Prerequisites

1. Python 3.11 or later
2. Docker installed and running
3. AWS credentials configured
4. Perplexity API key (for additional context)

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

3. Build the required Docker images:
```bash
# Build the cost explorer MCP server
cd ../mcp/src/aws-cost-explorer-mcp-server
docker build -t aws-cost-explorer-mcp:latest .

# Build the diagram MCP server
cd ../mcp/src/aws-diagram-mcp-server
docker build -t awslabs/aws-diagram-mcp-server:latest .
```

## Usage

Run the agent:
```bash
python main.py
```

The agent can:
1. Create AWS architecture diagrams using the diagram tool
2. Analyze AWS costs using the cost explorer tool
3. Provide additional context using Perplexity search
4. Perform data analysis and visualization using the code interpreter

## Example Queries

- "Create a diagram of a serverless application with API Gateway, Lambda, and DynamoDB"
- "Show me my AWS costs for the last 7 days"
- "Create a diagram of my current AWS architecture and analyze its costs"

## Notes

- The agent uses Claude 3.5 Sonnet as the foundation model
- Diagrams are generated using the Python diagrams package
- Cost analysis is performed using AWS Cost Explorer
- Additional context is provided by Perplexity search 