from InlineAgent.tools import MCPStdio
from InlineAgent.action_group import ActionGroup
from InlineAgent.agent import InlineAgent
import logging
import asyncio
import sys

from config import cv_server_params

# Set up logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting main function...")
    
    try:
        # Initialize CV MCP client
        logger.info("Initializing CV MCP client...")
        logger.debug(f"CV server params: {cv_server_params}")
        
        cv_client = await MCPStdio.create(server_params=cv_server_params)
        logger.info("CV MCP client initialized successfully")

        # Create action group with CV client
        logger.info("Creating action group...")
        action_group = ActionGroup(
            name="CVActionGroup",
            mcp_clients=[cv_client],
        )
        logger.info("Action group created successfully")

        # Create and invoke the agent with a timeout
        logger.info("Creating and invoking agent...")
        try:
            async with asyncio.timeout(30):  # 30 second timeout
                agent = InlineAgent(
                    foundation_model="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                    instruction="""You are a friendly assistant that is responsible for analyzing images
                    
                    You have access to tools to analyze images using Amazon Bedrock's Claude model.
                    """,
                    agent_name="cv_agent",
                    action_groups=[action_group],
                )
                logger.info("Agent created, invoking...")
                await agent.invoke(
                    input_text="Whats in image image001.png?"
                )
                logger.info("Agent invocation completed")
        except asyncio.TimeoutError:
            logger.error("Operation timed out after 30 seconds")
            raise
        except Exception as e:
            logger.error(f"Error during agent invocation: {str(e)}", exc_info=True)
            raise
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        raise
    finally:
        # Cleanup client
        try:
            logger.info("Cleaning up client...")
            await cv_client.cleanup()
            logger.info("Cleanup complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}", exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        sys.exit(1) 