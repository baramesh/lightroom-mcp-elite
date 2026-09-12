"""Develop and Color Grading Tools for Lightroom Classic."""

from __future__ import annotations

from typing import Any

from core.bridge import bridge


def set_develop_settings(photo_id: str | int, settings: dict[str, Any]) -> dict[str, Any]:
    """Set Develop adjustment parameters directly on a photo in Lightroom Classic.

    Keys include:
    - Exposure / Contrast: Exposure2012, Contrast2012
    - Tone: Highlights2012, Shadows2012, Whites2012, Blacks2012
    - Texture / Clarity: Texture, Clarity2012, Dehaze
    - Color Balance: Temperature, Tint, Vibrance, Saturation
    - HSL: HueAdjustment*, SaturationAdjustment*, LuminanceAdjustment*
    - Curves: ToneCurvePV2012 (flat [in, out] pairs)
    """
    res = bridge.execute("set_develop_settings", {"photo_id": photo_id, "settings": settings})
    if isinstance(res, dict):
        return res
    return {"ok": True, "photo_id": photo_id, "settings": settings}


def copy_develop_settings(source_photo_id: str | int, target_photo_ids: list[str | int]) -> dict[str, Any]:
    """Copy all Develop adjustments from a source photo to multiple target photos."""
    res = bridge.execute("copy_develop_settings", {
        "source_photo_id": source_photo_id,
        "target_photo_ids": target_photo_ids
    })
    if isinstance(res, dict):
        return res
    return {"ok": True, "source": source_photo_id, "synced_count": len(target_photo_ids)}


def list_develop_presets() -> dict[str, Any]:
    """List all available Lightroom Develop presets organized by folder."""
    res = bridge.execute("list_develop_presets")
    if isinstance(res, dict):
        return res
    return {"presets": res if isinstance(res, list) else []}


def get_develop_preset(preset_name: str) -> dict[str, Any]:
    """Inspect the internal settings and adjustments defined inside a Develop preset."""
    res = bridge.execute("get_develop_preset", {"preset_name": preset_name})
    if isinstance(res, dict):
        return res
    return {"preset": res}


def apply_develop_preset(photo_id: str | int, preset_name: str) -> dict[str, Any]:
    """Apply a Develop preset to a specified photo."""
    res = bridge.execute("apply_develop_preset", {"photo_id": photo_id, "preset_name": preset_name})
    if isinstance(res, dict):
        return res
    return {"ok": True, "photo_id": photo_id, "preset": preset_name}


def create_develop_preset(name: str, folder: str, settings: dict[str, Any]) -> dict[str, Any]:
    """Save current or specified adjustment parameters as a new Develop preset."""
    res = bridge.execute("create_develop_preset", {
        "name": name,
        "folder": folder,
        "settings": settings
    })
    if isinstance(res, dict):
        return res
    return {"ok": True, "name": name, "folder": folder}


def compare_develop_presets(base: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Compare two Develop presets and return a deterministic per-setting diff."""
    res = bridge.execute("compare_develop_presets", {
        "base": base,
        "candidate": candidate
    })
    if isinstance(res, dict):
        return res
    return {"diff": res}


def export_develop_preset(
    destination_dir: str,
    preset_uuid: str | None = None,
    preset_name: str | None = None,
    preset_folder: str | None = None,
    preset_scope: str | None = None,
    filename: str | None = None
) -> dict[str, Any]:
    """Export one exact custom or plugin-managed Develop preset backing file."""
    params: dict[str, Any] = {"destination_dir": destination_dir}
    if preset_uuid:
        params["preset_uuid"] = preset_uuid
    if preset_name:
        params["preset_name"] = preset_name
    if preset_folder:
        params["preset_folder"] = preset_folder
    if preset_scope:
        params["preset_scope"] = preset_scope
    if filename:
        params["filename"] = filename

    res = bridge.execute("export_develop_preset", params)
    if isinstance(res, dict):
        return res
    return {"ok": True, "destination_dir": destination_dir}

