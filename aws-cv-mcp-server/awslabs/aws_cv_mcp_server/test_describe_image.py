# © 2025 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
#
# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

import asyncio
import logging

from awslabs.aws_cv_mcp_server.server import mcp

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

async def test_describe_image():
    # dummy test parameters
    image_file_name = "dummy_image.jpg"
    monitoring_instructions = "Please analyze the image for any unusual activity."
    try:
        # call the describe_image tool (registered as mcp_describe_image) via mcp
        result = await mcp.describe_image(image_file_name, monitoring_instructions)
        print("Tool response (model_dump):", result)
    except Exception as e:
        print("Error calling describe_image:", e)

if __name__ == "__main__":
    asyncio.run(test_describe_image()) 