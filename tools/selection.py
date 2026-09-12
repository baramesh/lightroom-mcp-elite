"""Selection and Photo Query Tools for Lightroom Classic."""

from __future__ import annotations

from typing import Any

from core.bridge import bridge


def get_selected_photos(limit: int = 100, offset: int = 0) -> dict[str, Any]:
    """Get currently selected photos in Lightroom Classic (or filmstrip if none selected)."""
    res = bridge.execute("get_selected_photos", {"limit": limit, "offset": offset})
    if isinstance(res, dict):
        return res
    return {"photos": res if isinstance(res, list) else []}


def search_photos(
    query: str = "",
    rating: int | None = None,
    flag: str | None = None,
    color_label: str | None = None,
    limit: int = 100
) -> dict[str, Any]:
    """Search photos in Lightroom Classic by text, rating, pick flag, or color label."""
    params: dict[str, Any] = {"limit": limit}
    if query:
        params["query"] = query
    if rating is not None:
        params["rating"] = rating
    if flag:
        params["flag"] = flag
    if color_label:
        params["color_label"] = color_label

    res = bridge.execute("search_photos", params)
    if isinstance(res, dict):
        return res
    return {"photos": res if isinstance(res, list) else []}


def get_photo_metadata(photo_id: str | int) -> dict[str, Any]:
    """Get metadata (EXIF, dimensions, capture time, camera, lens, current develop settings) for a photo."""
    res = bridge.execute("get_photo_metadata", {"photo_id": photo_id})
    if isinstance(res, dict):
        return res
    return {"metadata": res}
