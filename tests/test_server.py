from unittest.mock import patch

import server


def test_server_tools_delegation(mock_bridge):
    mock_bridge.execute.return_value = {"ok": True, "path": "/fake/path.jpg"}

    assert server.lightroom_get_selected_photos(10, 0)["ok"] is True
    assert server.lightroom_search_photos("query")["ok"] is True
    assert server.lightroom_get_photo_metadata("p1")["ok"] is True

    assert server.lightroom_set_develop_settings("p1", {"Exposure2012": 0.5})["ok"] is True
    assert server.lightroom_copy_develop_settings("p1", ["p2"])["ok"] is True
    assert server.lightroom_list_develop_presets()["ok"] is True
    assert server.lightroom_get_develop_preset("Preset")["ok"] is True
    assert server.lightroom_apply_develop_preset("p1", "Preset")["ok"] is True
    assert server.lightroom_create_develop_preset("Name", "Folder", {})["ok"] is True
    assert server.lightroom_compare_develop_presets({}, {})["ok"] is True
    assert server.lightroom_export_develop_preset("/tmp", preset_uuid="uuid")["ok"] is True

    assert server.lightroom_set_rating(["p1"], 5)["ok"] is True
    assert server.lightroom_set_keywords(["p1"], ["tag"])["ok"] is True
    assert server.lightroom_list_collections()["ok"] is True
    assert server.lightroom_create_collection("Coll")["ok"] is True
    assert server.lightroom_add_to_collection("c1", ["p1"])["ok"] is True
    assert server.lightroom_export_photos(["p1"], "/tmp")["ok"] is True
    assert server.lightroom_import_photos("/tmp/pic.jpg")["ok"] is True

    with patch("tools.coop.subprocess.run") as mock_sub, patch("os.path.exists", return_value=True):
        mock_sub.return_value.returncode = 0
        assert server.lightroom_send_to_photoshop("p1")["ok"] is True

    with patch("os.path.exists", return_value=True):
        assert server.lightroom_import_retouched_photo("/tmp/retouched.tif")["ok"] is True


def test_server_main():
    with patch("mcp.server.mcpserver.MCPServer.run") as mock_run:
        server.main()
        mock_run.assert_called_once_with(transport="stdio")
