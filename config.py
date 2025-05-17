from mcp import StdioServerParameters

from InlineAgent import AgentAppConfig

config = AgentAppConfig()


cv_server_params = StdioServerParameters(
    command="docker",
    args=[
        "run",
        "-i",
        "--rm",
        "-e",
        "FASTMCP_LOG_LEVEL=ERROR",
        "-e",
        "AWS_ACCESS_KEY_ID",
        "-e",
        "AWS_SECRET_ACCESS_KEY",
        "-e",
        "AWS_REGION",
        "-e",
        "AGENT_BUCKET_NAME",
        "-e",
        "BEDROCK_LOG_GROUP_NAME",        
        "awslabs/aws-cv-mcp-server:latest",
    ],
    env={
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_ACCESS_KEY_ID": config.AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": config.AWS_SECRET_ACCESS_KEY,
        "AWS_REGION": config.AWS_REGION,
        "AGENT_BUCKET_NAME": config.AGENT_BUCKET_NAME,
        "BEDROCK_LOG_GROUP_NAME": config.BEDROCK_LOG_GROUP_NAME,
        
    },
)

# Perplexity MCP Server configuration (for additional context)
perplexity_server_params = StdioServerParameters(
    command="docker",
    args=["run", "-i", "--rm", "-e", "PERPLEXITY_API_KEY", "mcp/perplexity-ask"],
    env={"PERPLEXITY_API_KEY": config.PERPLEXITY_API_KEY},
) 