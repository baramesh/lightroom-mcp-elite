from tools import coop, develop, organization, selection


def test_selection_tools(mock_bridge):
    mock_bridge.execute.return_value = {"photos": [{"id": 1, "path": "/photos/pic1.jpg"}]}
    sel = selection.get_selected_photos()
    assert len(sel["photos"]) == 1

    mock_bridge.execute.return_value = {"photos": [{"id": 2}]}
    search = selection.search_photos(query="portrait", rating=5)
    assert search["photos"][0]["id"] == 2

    mock_bridge.execute.return_value = {"id": 1, "ISO": 100, "ExposureTime": "1/250"}
    meta = selection.get_photo_metadata(1)
    assert meta["ISO"] == 100


def test_develop_tools(mock_bridge):
    mock_bridge.execute.return_value = {"ok": True, "photo_id": 1}
    dev = develop.set_develop_settings(1, {"Exposure2012": 0.5, "Clarity2012": 15})
    assert dev["ok"] is True

    mock_bridge.execute.return_value = {"ok": True, "synced_count": 3}
    synced = develop.copy_develop_settings(1, [2, 3, 4])
    assert synced["synced_count"] == 3

    mock_bridge.execute.return_value = [{"name": "Classic Chrome", "folder": "Vintage"}]
    presets = develop.list_develop_presets()
    assert len(presets["presets"]) == 1

    mock_bridge.execute.return_value = {"settings": {"Exposure2012": 0.2}}
    preset_data = develop.get_develop_preset("Classic Chrome")
    assert preset_data["settings"]["Exposure2012"] == 0.2

    mock_bridge.execute.return_value = {"ok": True}
    applied = develop.apply_develop_preset(1, "Classic Chrome")
    assert applied["ok"] is True

    created = develop.create_develop_preset("Moody Warm", "User Presets", {"Temperature": 5500})
    assert created["ok"] is True


def test_organization_tools(mock_bridge):
    mock_bridge.execute.return_value = {"ok": True, "count": 2}
    rated = organization.set_rating([1, 2], 5)
    assert rated["count"] == 2

    mock_bridge.execute.return_value = {"ok": True}
    kw = organization.set_keywords([1], ["travel", "japan"])
    assert kw["ok"] is True

    mock_bridge.execute.return_value = [{"id": "col_1", "name": "Favorites"}]
    cols = organization.list_collections()
    assert len(cols["collections"]) == 1

    mock_bridge.execute.return_value = {"ok": True, "id": "col_2"}
    created_col = organization.create_collection("Vacation 2026")
    assert created_col["ok"] is True

    mock_bridge.execute.return_value = {"ok": True}
    added = organization.add_to_collection("col_1", [1, 2])
    assert added["ok"] is True

    exported = organization.export_photos([1], "/output/dir")
    assert exported["ok"] is True


def test_coop_tools(mock_bridge, monkeypatch, tmp_path):
    # Mock photo file path
    test_img = tmp_path / "sample.jpg"
    test_img.write_text("fake_image_content")

    mock_bridge.execute.return_value = {"id": 1, "path": str(test_img)}

    # Mock subprocess for photoshop launch
    from unittest.mock import MagicMock
    mock_proc = MagicMock(returncode=0)
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: mock_proc)

    send_res = coop.send_to_photoshop(1)
    assert send_res["ok"] is True
    assert send_res["action"] == "opened_in_photoshop"

    # Import retouched
    mock_bridge.execute.return_value = {"imported_count": 1}
    import_res = coop.import_retouched_photo(str(test_img), collection_name="Master Retouched")
    assert import_res["ok"] is True
    assert import_res["action"] == "imported_to_lightroom"
