"""aws-cv-mcp-server implementation.

This server provides tools to analyze images using Amazon Bedrock's Claude model.
"""

import argparse
import os
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Dict, List, Union

from awslabs.aws_cv_mcp_server.connections import Connections
from awslabs.aws_cv_mcp_server.cv_tools import describe_image

# Create the MCP server
mcp = FastMCP(
    'aws-cv-mcp-server',
    dependencies=[
        'pydantic',
        'boto3',
    ],
    log_level='ERROR',
    instructions="""Use this server to carry out various computer vision tasks.""",
)

@mcp.tool(name='describe_image')
async def mcp_describe_image(
    image_file_name: str = Field(
        ...,
        description='The name of the image file in S3 to analyze. This should be the full path/key in the S3 bucket.',
    ),
    monitoring_instructions: str = Field(
        ...,
        description='Specific instructions for what to monitor or analyze in the image. This guides the model on what aspects to focus on.',
    ),
) -> Dict[str, Union[List[str], str]]:
    """Analyze an image using Amazon Bedrock's Claude model.

    This tool takes an image from S3 and uses Claude to analyze it according to specific monitoring instructions.
    The image is processed through Amazon Bedrock's Claude model to generate a detailed description and analysis.

    USAGE INSTRUCTIONS:
    1. Provide the S3 image file name (key) that you want to analyze
    2. Provide specific monitoring instructions to guide the analysis
    3. The tool will return a detailed analysis of the image based on the instructions

    Returns:
        Dictionary containing the source image file name and the analysis results
    """
    try:
        # Use the describe_image function from cv_tools
        response = await describe_image(
            image_file_name=image_file_name,
            monitoring_instructions=monitoring_instructions
        )
        return {
            "description": response.analysis,
            "source_image": image_file_name
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    """Run the MCP server with CLI argument support."""
    parser = argparse.ArgumentParser(
        description='An MCP server that provides computer vision capabilities using Amazon Bedrock'
    )
    parser.add_argument('--sse', action='store_true', help='Use SSE transport')
    parser.add_argument('--port', type=int, default=8888, help='Port to run the server on')

    args = parser.parse_args()

    # Run server with appropriate transport
    if args.sse:
        mcp.settings.port = args.port
        mcp.run(transport='sse')
    else:
        mcp.run()

if __name__ == '__main__':
    main()
