---
name: lightroom-mcp-elite
description: Control and automate Adobe Lightroom Classic through the Lightroom MCP Elite server with professional Develop controls, preset syncing, catalog organization, and seamless round-trip handoff to Adobe Photoshop for AI inpainting and composite retouching.
---

# Lightroom MCP Elite Guide & Workflow Standard

Use the connected `lightroom` MCP server (`lightroom-mcp-elite`) to control **Adobe Lightroom Classic** on macOS.
Follow non-destructive RAW processing, catalog curation, and seamless Adobe Photoshop round-trip standards.

---

## 1. Operating Principles

1. **Verify State & Inspect Selection First**:
   - Always call `lightroom_get_selected_photos()` to identify which photos the user is currently looking at in the filmstrip or grid.
   - Call `lightroom_get_photo_metadata(photo_id)` to read current EXIF, camera settings, and active Develop adjustments before making modifications.
   - If no photos are selected, use `lightroom_search_photos()` by text, rating, or pick flag.

2. **Develop & Grading Best Practices**:
   - **Exposure / Contrast**: `Exposure2012` (+/- stops, e.g. 0.2, -0.3), `Contrast2012`.
   - **Dynamic Range**: `Highlights2012` (recover sky/clouds), `Shadows2012` (lift dark regions), `Whites2012`, `Blacks2012`.
   - **Clarity & Texture**: `Clarity2012` (+10 to +20 on architecture/landscapes, subtle on portraits), `Dehaze` (+5 to +15 to remove haze).
   - **Color Balance**: `Temperature` (Kelvin or offset), `Tint`, `Vibrance` (preferred over global `Saturation` to preserve skin tones).
   - **Batch Sync**: Edit the master frame, then use `lightroom_copy_develop_settings(source_photo_id, target_photo_ids)` to sync across the entire shoot in seconds.

3. **Preset Management**:
   - Discover available catalog presets with `lightroom_list_develop_presets()`.
   - Inspect internal parameters with `lightroom_get_develop_preset()`.
   - Apply looks with `lightroom_apply_develop_preset()`.
   - Save custom look checkpoints using `lightroom_create_develop_preset()`.

---

## 2. Seamless Photoshop Round-trip Pipeline (Co-op)

When an edit exceeds Lightroom's scope (e.g. object removal on complex architectural balustrades, text typography, advanced multi-layer compositing, or Firefly Generative Fill):

1. **Handoff to Photoshop**:
   - Call `lightroom_send_to_photoshop(photo_id)`.
   - Lightroom MCP resolves the true master file path and activates Adobe Photoshop, opening the image directly.
2. **Execute Photoshop MCP Elite Tools**:
   - Switch context to Photoshop MCP to run `photoshop_generative_fill_ai`, `photoshop_generative_remove_ai`, `photoshop_harmonize_sky`, or `photoshop_add_text_layer`.
   - Save the master file (TIFF or PSD).
3. **Re-import to Lightroom**:
   - Call `lightroom_import_retouched_photo(file_path, collection_name="Master Retouched")`.
   - The retouched image is instantly ingested back into the Lightroom Catalog, organized into the target collection.

---

## 3. Tool Catalog (17 Tools)

### Selection & Discovery
* `lightroom_get_selected_photos`: Get photos currently highlighted in Lightroom.
* `lightroom_search_photos`: Search catalog by text, rating, flag, or color label.
* `lightroom_get_photo_metadata`: Read full EXIF and current Develop parameters.

### Develop & Presets
* `lightroom_set_develop_settings`: Set raw develop parameters directly on a photo.
* `lightroom_copy_develop_settings`: Sync adjustments across multiple photos.
* `lightroom_list_develop_presets`: List presets in catalog.
* `lightroom_get_develop_preset`: Inspect internal preset settings.
* `lightroom_apply_develop_preset`: Apply a preset look to a photo.
* `lightroom_create_develop_preset`: Save settings as a new preset.

### Organization & Export
* `lightroom_set_rating`: Assign 0-5 stars to photos.
* `lightroom_set_keywords`: Add, remove, or replace tags.
* `lightroom_list_collections`: List collection sets and collections.
* `lightroom_create_collection`: Create a new collection.
* `lightroom_add_to_collection`: Add photos to a collection.
* `lightroom_export_photos`: Export high-fidelity JPEGs/TIFFs.

### Photoshop Co-op
* `lightroom_send_to_photoshop`: Seamlessly open photo in Adobe Photoshop.
* `lightroom_import_retouched_photo`: Import retouched master back into catalog.

---

## 4. Golden Example: Master Studio & Photoshop Co-op

Refer to `examples/lightroom_photoshop_coop.md` for the complete end-to-end recipe.
