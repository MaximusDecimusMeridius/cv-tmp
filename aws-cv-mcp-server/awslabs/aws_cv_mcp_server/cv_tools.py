#
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

"""Computer vision tools for analyzing images using Amazon Bedrock."""

import logging
import os
from typing import Optional
from awslabs.aws_cv_mcp_server.connections import Connections
from awslabs.aws_cv_mcp_server.models import ImageAnalysisResponse
from awslabs.aws_cv_mcp_server.bedrock_utils import create_multimodal_prompt, invoke_bedrock_model

logger = logging.getLogger(__name__)

async def describe_image(
    image_file_name: str,
    monitoring_instructions: str,
) -> ImageAnalysisResponse:
    """Analyze an image using Amazon Bedrock's Claude model.

    Args:
        image_file_name: The name of the image file in S3 to analyze
        monitoring_instructions: Specific instructions for what to monitor or analyze in the image

    Returns:
        ImageAnalysisResponse: Response containing the analysis results
    """
    try:
        # Get the image from S3
        response = Connections.s3_client.get_object(
            Bucket=Connections.agent_bucket_name,
            Key=image_file_name
        )
        image_data = response['Body'].read()
        content_type = response['ContentType']

        # Create the prompt for Claude
        prompt = create_multimodal_prompt(
            image_data=image_data,
            text=monitoring_instructions,
            content_type=content_type,
            system_prompt="You are a helpful assistant that analyzes images. Provide detailed, accurate descriptions based on the user's instructions."
        )

        # Get analysis from Claude
        analysis = invoke_bedrock_model(prompt)

        return ImageAnalysisResponse(
            status="success",
            source=image_file_name,
            analysis=analysis,
            message="Image analysis completed successfully"
        )

    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return ImageAnalysisResponse(
            status="error",
            source=image_file_name,
            analysis=None,
            message=f"Error analyzing image: {str(e)}"
        )
