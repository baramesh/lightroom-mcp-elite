# Golden Example: Lightroom Classic & Photoshop Co-op Pipeline

## Scenario
A photographer has selected an architectural portrait shot in Lightroom Classic. The shot has a great mood, but there are unwanted tourists in the background, a flat sky, and it needs a final magazine-grade color grade.
User request:
> *"ช่วยแต่งรูปที่เลือกอยู่ใน Lightroom ลบคนข้างหลังออก เปลี่ยนฟ้า แล้วเกรดสีให้สวยพร้อมลง Catalog"*

---

## Retoucher's Co-op Mental Model
1. **Lightroom First (Curation & RAW Baseline)**:
   - Identify active photo via `lightroom_get_selected_photos()`.
   - Inspect exposure and WB metadata via `lightroom_get_photo_metadata()`.
   - Apply base exposure correction and dynamic range recovery (`Highlights2012`: -30, `Shadows2012`: +20).
2. **Handoff to Photoshop (Firefly AI & Compositing)**:
   - Call `lightroom_send_to_photoshop(photo_id)`.
   - In Photoshop, run `photoshop_generative_remove_ai` on the tourists.
   - Run `photoshop_harmonize_sky` with horizon atmospheric haze.
   - Run `photoshop_apply_camera_raw_filter` for unified studio grading.
   - Save the file as a master TIFF/PSD.
3. **Round-trip Back to Lightroom (Catalog Ingestion)**:
   - Call `lightroom_import_retouched_photo(file_path, "Master Retouched")`.
   - Apply 5-star rating via `lightroom_set_rating()` and tag with `lightroom_set_keywords()`.

---

## Tool Execution Sequence

### Phase 1: Lightroom RAW Baseline
```json
// 1. Get selected photo
// Tool: lightroom_get_selected_photos
{"limit": 1}

// 2. Set base develop settings
// Tool: lightroom_set_develop_settings
{
  "photo_id": 101,
  "settings": {
    "Highlights2012": -35,
    "Shadows2012": 25,
    "Vibrance": 12,
    "Dehaze": 6
  }
}
```

### Phase 2: Send to Photoshop
```json
// Tool: lightroom_send_to_photoshop
{
  "photo_id": 101
}
```
*Effect: Photoshop activates with the exact photo ready on canvas.*

### Phase 3: Photoshop Retouching Suite
```json
// 1. Firefly Inpainting
// Tool: photoshop_generative_remove_ai
{
  "regions": [[700, 1500, 1000, 2300]],
  "feather_px": 2.5
}

// 2. Sky Replacement & Ambient Light Wrap
// Tool: photoshop_harmonize_sky
{
  "new_sky_path": "/path/to/sunny_sky.jpg",
  "sky_opacity": 85.0,
  "warm_foreground": true
}

// 3. Save File
// Tool: photoshop_save_document
{
  "file_path": "/path/to/photo_master_retouched.tif"
}
```

### Phase 4: Ingest Back to Lightroom & Curate
```json
// 1. Re-import into Lightroom
// Tool: lightroom_import_retouched_photo
{
  "file_path": "/path/to/photo_master_retouched.tif",
  "collection_name": "Portfolio 2026"
}

// 2. Set 5 Stars & Tags
// Tool: lightroom_set_rating
{
  "photo_ids": ["photo_master_retouched"],
  "rating": 5
}
```
