import sys

import pytest
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_mcp_lightroom_e2e_lifecycle():
    """End-to-end test verifying MCP stdio protocol handshake, listing all tools, and checking schema."""
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
        env=None
    )

    async with (
        stdio_client(server_params) as (read, write),
        ClientSession(read, write) as session,
    ):
        # 1. Initialize MCP Handshake
        init_res = await session.initialize()
        assert init_res.server_info.name == "lightroom"

        # 2. List all registered tools
        tools_res = await session.list_tools()
        tool_names = [t.name for t in tools_res.tools]

        # Verify key tool registrations
        assert len(tool_names) == 17
        assert "lightroom_get_selected_photos" in tool_names
        assert "lightroom_search_photos" in tool_names
        assert "lightroom_get_photo_metadata" in tool_names
        assert "lightroom_set_develop_settings" in tool_names
        assert "lightroom_copy_develop_settings" in tool_names
        assert "lightroom_list_develop_presets" in tool_names
        assert "lightroom_get_develop_preset" in tool_names
        assert "lightroom_apply_develop_preset" in tool_names
        assert "lightroom_create_develop_preset" in tool_names
        assert "lightroom_set_rating" in tool_names
        assert "lightroom_set_keywords" in tool_names
        assert "lightroom_list_collections" in tool_names
        assert "lightroom_create_collection" in tool_names
        assert "lightroom_add_to_collection" in tool_names
        assert "lightroom_export_photos" in tool_names
        assert "lightroom_send_to_photoshop" in tool_names
        assert "lightroom_import_retouched_photo" in tool_names
