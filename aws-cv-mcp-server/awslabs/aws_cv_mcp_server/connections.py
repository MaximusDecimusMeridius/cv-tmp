# © 2025 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
#
# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

import os
import boto3
import logging

logger = logging.getLogger(__name__)

class Connections:
    """AWS service connections using a shared boto3 session."""
    
    logger = logger
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    agent_bucket_name = os.environ.get("AGENT_BUCKET_NAME", "your-agent-bucket-name")
    
    # Create a single boto3 session for all AWS service clients
    session = boto3.Session(
        region_name=region_name,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    
    # Initialize AWS service clients using the shared session
    s3_client = session.client("s3")
    bedrock_client = session.client("bedrock-runtime") 