"""aws-cv-mcp-server implementation.

This server provides tools to generate diagrams using the Python diagrams package.
It accepts Python code as a string and generates PNG diagrams without displaying them.
"""

import argparse
import os
import boto3
from awslabs.aws_cv_mcp_server.cv_tools import (
    generate_diagram,
    get_diagram_examples,
    list_diagram_icons,
    describe_image,
)
from awslabs.aws_cv_mcp_server.models import DiagramType
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Optional

# Initialize AWS clients
aws_region = os.environ.get("AWS_REGION", "us-east-1")
aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

s3_client = boto3.client(
    "s3",
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Create the MCP server
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
mcp = FastMCP(
    'aws-cv-mcp-server',
    dependencies=[
        'pydantic',
        'diagrams',
    ],
    log_level='ERROR',
    instructions="""Use this server to carry out various computer vision tasks.""",
)

# Register tools
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
):
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
    result = await describe_image(image_file_name, monitoring_instructions)
    return result.model_dump()


@mcp.tool(name='get_diagram_examples')
async def mcp_get_diagram_examples(
    diagram_type: DiagramType = Field(
        default=DiagramType.ALL,
        description='Type of diagram example to return. Options: aws, sequence, flow, class, k8s, onprem, custom, all',
    ),
):
    """Get example code for different types of diagrams.

    This tool provides ready-to-use example code for various diagram types.
    Use these examples to understand the syntax and capabilities of the diagrams package
    before creating your own custom diagrams.

    USAGE INSTRUCTIONS:
    1. Select the diagram type you're interested in (or 'all' to see all examples)
    2. Study the returned examples to understand the structure and syntax
    3. Use these examples as templates for your own diagrams
    4. When ready, modify an example or write your own code and use generate_diagram

    EXAMPLE CATEGORIES:
    - aws: AWS cloud architecture diagrams (basic services, grouped workers, clustered web services, Bedrock)
    - sequence: Process and interaction flow diagrams
    - flow: Decision trees and workflow diagrams
    - class: Object relationship and inheritance diagrams


    Parameters:
        diagram_type (str): Type of diagram example to return. Options: aws, sequence, flow, class, k8s, onprem, custom, all

    Returns:
        Dictionary with example code for the requested diagram type(s), organized by example name
    """
    result = get_diagram_examples(diagram_type)
    return result.model_dump()


@mcp.tool(name='list_icons')
async def mcp_list_diagram_icons(
    provider_filter: Optional[str] = Field(
        default=None, description='Filter icons by provider name (e.g., "aws", "gcp", "k8s")'
    ),
    service_filter: Optional[str] = Field(
        default=None,
        description='Filter icons by service name (e.g., "compute", "database", "network")',
    ),
):
    """List available icons from the diagrams package, with optional filtering.

    This tool dynamically inspects the diagrams package to find available
    providers, services, and icons that can be used in diagrams.

    USAGE INSTRUCTIONS:
    1. Call without filters to get a list of available providers
    2. Call with provider_filter to get all services and icons for that provider
    3. Call with both provider_filter and service_filter to get icons for a specific service

    Example workflow:
    - First call: list_icons() → Returns all available providers
    - Second call: list_icons(provider_filter="aws") → Returns all AWS services and icons
    - Third call: list_icons(provider_filter="aws", service_filter="compute") → Returns AWS compute icons

    This approach is more efficient than loading all icons at once, especially when you only need
    icons from specific providers or services.

    Returns:
        Dictionary with available providers, services, and icons organized hierarchically
    """
    # Extract the actual values from the parameters
    provider_filter_value = None if provider_filter is None else provider_filter
    service_filter_value = None if service_filter is None else service_filter

    result = list_diagram_icons(provider_filter_value, service_filter_value)
    return result.model_dump()


def main():
    """Run the MCP server with CLI argument support."""
    parser = argparse.ArgumentParser(
        description='An MCP server that seamlessly creates diagrams using the Python diagrams package DSL'
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
