"""Photoshop Co-op and Round-trip Retouching Pipeline.

Enables seamless handoff between Adobe Lightroom Classic and Adobe Photoshop 2026:
1. Exporting or finding the master RAW/TIFF from Lightroom.
2. Opening it directly into Photoshop for Firefly AI Inpainting / Sky Harmonization / Compositing.
3. Automatically re-importing or updating the catalog upon completion.
"""

from __future__ import annotations

import os
import subprocess
from typing import Any

from core.bridge import bridge


def send_to_photoshop(photo_id: str | int) -> dict[str, Any]:
    """Retrieves file path of photo from Lightroom and opens it in Adobe Photoshop."""
    meta = bridge.execute("get_photo_metadata", {"photo_id": photo_id})
    file_path = None
    if isinstance(meta, dict):
        file_path = meta.get("path") or meta.get("file_path") or meta.get("filePath")

    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not resolve valid filesystem path for photo ID {photo_id}: {file_path}")

    # Open directly in Adobe Photoshop using macOS AppleScript
    ascript = f'''
    tell application id "com.adobe.Photoshop"
        activate
        open POSIX file "{file_path}"
    end tell
    '''
    proc = subprocess.run(["/usr/bin/osascript", "-e", ascript], capture_output=True, text=True, check=False)  # nosec B603
    if proc.returncode != 0:
        return {"ok": False, "error": f"Failed to open in Photoshop: {proc.stderr.strip()}", "path": file_path}

    return {
        "ok": True,
        "action": "opened_in_photoshop",
        "photo_id": photo_id,
        "path": file_path,
        "message": "Photo opened in Adobe Photoshop. Perform Firefly inpainting, generative retouch, or layers, then save."
    }


def import_retouched_photo(file_path: str, collection_name: str = "Photoshop Retouched") -> dict[str, Any]:
    """Imports a saved retouched file (TIFF/PSD/JPEG) from Photoshop back into Lightroom Classic."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Retouched file not found: {file_path}")

    # 1. Import photo
    res = bridge.execute("import_photos", {"file_paths": [file_path]})
    # 2. Add to collection if requested
    if collection_name:
        bridge.execute("create_collection", {"name": collection_name})

    return {
        "ok": True,
        "action": "imported_to_lightroom",
        "path": file_path,
        "collection": collection_name,
        "details": res
    }
