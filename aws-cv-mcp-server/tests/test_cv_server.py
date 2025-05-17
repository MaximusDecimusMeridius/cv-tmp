import pytest
from awslabs.aws_cv_mcp_server.server import mcp_describe_image

@pytest.mark.asyncio
async def test_describe_image(monkeypatch):
    async def fake_describe_image(image_file_name: str, monitoring_instructions: str):
        class FakeResp:
            analysis = "cats detected"
        return FakeResp()

    monkeypatch.setattr(
        "awslabs.aws_cv_mcp_server.server.describe_image",
        fake_describe_image,
    )

    result = await mcp_describe_image(
        image_file_name="test.png",
        monitoring_instructions="look for cats",
    )

    assert result == {"description": "cats detected", "source_image": "test.png"}
