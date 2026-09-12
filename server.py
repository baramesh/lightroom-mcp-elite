#!/usr/bin/env python3
"""Adobe Lightroom Classic Elite MCP Server.

Native Python MCP Server for Lightroom Classic with Develop Controls, Presets,
Catalog Management, and Seamless Adobe Photoshop Co-op.
"""

from __future__ import annotations

from typing import Any

from mcp.server.mcpserver import MCPServer

from tools import coop, develop, organization, selection

app = MCPServer("lightroom")


# --- Selection & Photo Discovery Tools ---

@app.tool()
def lightroom_get_selected_photos(limit: int = 100, offset: int = 0) -> dict[str, Any]:
    """Get currently selected photos in Lightroom Classic (or filmstrip if none selected)."""
    return selection.get_selected_photos(limit=limit, offset=offset)


@app.tool()
def lightroom_search_photos(
    query: str = "",
    rating: int | None = None,
    flag: str | None = None,
    color_label: str | None = None,
    limit: int = 100
) -> dict[str, Any]:
    """Search photos in Lightroom Classic by text, star rating, pick flag, or color label."""
    return selection.search_photos(query=query, rating=rating, flag=flag, color_label=color_label, limit=limit)


@app.tool()
def lightroom_get_photo_metadata(photo_id: str | int) -> dict[str, Any]:
    """Get detailed metadata (EXIF, camera, lens, dimensions, and develop parameters) for a photo."""
    return selection.get_photo_metadata(photo_id=photo_id)


# --- Develop & Color Grading Tools ---

@app.tool()
def lightroom_set_develop_settings(photo_id: str | int, settings: dict[str, Any]) -> dict[str, Any]:
    """Set Develop adjustments directly on a photo (Exposure2012, Highlights2012, Shadows2012, Clarity2012, Dehaze, Vibrance, etc.)."""
    return develop.set_develop_settings(photo_id=photo_id, settings=settings)


@app.tool()
def lightroom_copy_develop_settings(source_photo_id: str | int, target_photo_ids: list[str | int]) -> dict[str, Any]:
    """Sync all Develop adjustments from a source photo to multiple target photos."""
    return develop.copy_develop_settings(source_photo_id=source_photo_id, target_photo_ids=target_photo_ids)


@app.tool()
def lightroom_list_develop_presets() -> dict[str, Any]:
    """List all Lightroom Develop presets available in the catalog."""
    return develop.list_develop_presets()


@app.tool()
def lightroom_get_develop_preset(preset_name: str) -> dict[str, Any]:
    """Inspect internal adjustment parameters stored inside a Develop preset."""
    return develop.get_develop_preset(preset_name=preset_name)


@app.tool()
def lightroom_apply_develop_preset(photo_id: str | int, preset_name: str) -> dict[str, Any]:
    """Apply a Develop preset to a specified photo."""
    return develop.apply_develop_preset(photo_id=photo_id, preset_name=preset_name)


@app.tool()
def lightroom_create_develop_preset(name: str, folder: str, settings: dict[str, Any]) -> dict[str, Any]:
    """Save specified Develop settings as a new preset in Lightroom Classic."""
    return develop.create_develop_preset(name=name, folder=folder, settings=settings)


# --- Organization, Collections & Export ---

@app.tool()
def lightroom_set_rating(photo_ids: list[str | int], rating: int) -> dict[str, Any]:
    """Set star rating (0 to 5) on one or more photos."""
    return organization.set_rating(photo_ids=photo_ids, rating=rating)


@app.tool()
def lightroom_set_keywords(photo_ids: list[str | int], keywords: list[str], mode: str = "add") -> dict[str, Any]:
    """Add, remove, or replace keywords on specified photos."""
    return organization.set_keywords(photo_ids=photo_ids, keywords=keywords, mode=mode)


@app.tool()
def lightroom_list_collections() -> dict[str, Any]:
    """List all collections and collection sets in the catalog."""
    return organization.list_collections()


@app.tool()
def lightroom_create_collection(name: str, parent_set_id: str | None = None) -> dict[str, Any]:
    """Create a new collection in the active catalog."""
    return organization.create_collection(name=name, parent_set_id=parent_set_id)


@app.tool()
def lightroom_add_to_collection(collection_id: str, photo_ids: list[str | int]) -> dict[str, Any]:
    """Add photos to an existing collection."""
    return organization.add_to_collection(collection_id=collection_id, photo_ids=photo_ids)


@app.tool()
def lightroom_export_photos(
    photo_ids: list[str | int],
    output_dir: str,
    format_type: str = "jpeg",
    quality: int = 90
) -> dict[str, Any]:
    """Export selected photos to disk with specified format and quality."""
    return organization.export_photos(photo_ids=photo_ids, output_dir=output_dir, format_type=format_type, quality=quality)


# --- Photoshop Co-op Workflow Tools ---

@app.tool()
def lightroom_send_to_photoshop(photo_id: str | int) -> dict[str, Any]:
    """Send a photo from Lightroom Classic directly into Adobe Photoshop for advanced retouching or Firefly AI inpainting."""
    return coop.send_to_photoshop(photo_id=photo_id)


@app.tool()
def lightroom_import_retouched_photo(file_path: str, collection_name: str = "Photoshop Retouched") -> dict[str, Any]:
    """Import a retouched master photo back into Lightroom Classic and organize into a collection."""
    return coop.import_retouched_photo(file_path=file_path, collection_name=collection_name)


def main():
    """Run the Lightroom MCP server over stdio."""
    app.run(transport="stdio")


if __name__ == "__main__":
    main()
