"""Organization, Ratings, Collections, and Export Tools for Lightroom Classic."""

from __future__ import annotations

from typing import Any

from core.bridge import bridge


def set_rating(photo_ids: list[str | int], rating: int) -> dict[str, Any]:
    """Set star rating (0 to 5) for one or more photos."""
    res = bridge.execute("set_rating", {"photo_ids": photo_ids, "rating": rating})
    if isinstance(res, dict):
        return res
    return {"ok": True, "rating": rating, "count": len(photo_ids)}


def set_keywords(photo_ids: list[str | int], keywords: list[str], mode: str = "add") -> dict[str, Any]:
    """Add, remove, or replace keywords on one or more photos."""
    res = bridge.execute("set_keywords", {
        "photo_ids": photo_ids,
        "keywords": keywords,
        "mode": mode
    })
    if isinstance(res, dict):
        return res
    return {"ok": True, "keywords": keywords, "mode": mode, "count": len(photo_ids)}


def list_collections() -> dict[str, Any]:
    """List all collections and collection sets in the active catalog."""
    res = bridge.execute("list_collections")
    if isinstance(res, dict):
        return res
    return {"collections": res if isinstance(res, list) else []}


def create_collection(name: str, parent_set_id: str | None = None) -> dict[str, Any]:
    """Create a new collection in the active catalog."""
    params: dict[str, Any] = {"name": name}
    if parent_set_id:
        params["parent_set_id"] = parent_set_id
    res = bridge.execute("create_collection", params)
    if isinstance(res, dict):
        return res
    return {"ok": True, "name": name}


def add_to_collection(collection_id: str, photo_ids: list[str | int]) -> dict[str, Any]:
    """Add specified photos to a collection."""
    res = bridge.execute("add_to_collection", {"collection_id": collection_id, "photo_ids": photo_ids})
    if isinstance(res, dict):
        return res
    return {"ok": True, "collection_id": collection_id, "count": len(photo_ids)}


def export_photos(
    photo_ids: list[str | int],
    output_dir: str,
    format_type: str = "jpeg",
    quality: int = 90
) -> dict[str, Any]:
    """Export photos from Lightroom Classic to disk with format and quality specifications."""
    res = bridge.execute("export_photos", {
        "photo_ids": photo_ids,
        "output_dir": output_dir,
        "format": format_type,
        "quality": quality
    })
    if isinstance(res, dict):
        return res
    return {"ok": True, "output_dir": output_dir, "count": len(photo_ids)}


def import_photos(source_path: str, collection_name: str | None = None, copy_to: str | None = None) -> dict[str, Any]:
    """Import photos into Lightroom Classic catalog."""
    params: dict[str, Any] = {"source_path": source_path}
    if collection_name:
        params["collection_name"] = collection_name
    if copy_to:
        params["copy_to"] = copy_to
    res = bridge.execute("import_photos", params)
    if isinstance(res, dict):
        return res
    return {"ok": True, "source_path": source_path}

