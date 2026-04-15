# PDF Form Filling

## Initial Assessment

First check if the PDF has fillable form fields:
```bash
python scripts/check_fillable_fields.py file.pdf
```

---

## For Fillable Forms

**Step 1 — Extract field info:**
```bash
python scripts/extract_form_field_info.py input.pdf fields.json
```
Outputs JSON cataloging all fields (IDs, locations, types: text/checkbox/radio/choice).

**Step 2 — Visually verify (optional):**
```bash
mkdir pages && python scripts/convert_pdf_to_images.py input.pdf pages/
```

**Step 3 — Create field values JSON:**
```json
[
  {"field_id": "FirstName", "page": 1, "value": "John"},
  {"field_id": "Agree", "page": 1, "value": "/Yes"},
  {"field_id": "Gender", "page": 1, "value": "/Male"}
]
```
- Checkboxes: use the `checked_value` shown in the field info JSON
- Radio groups: use one of the `radio_options[].value` values
- Choice fields: use one of the `choice_options[].value` values

**Step 4 — Fill the form:**
```bash
python scripts/fill_fillable_fields.py input.pdf field_values.json output.pdf
```

---

## For Non-Fillable Forms (Text Annotations)

### Approach A — Preferred (digitally-created PDFs)

Extract structural coordinates:
```bash
python scripts/extract_form_structure.py input.pdf structure.json
```

Build a `fields.json` with `form_fields` array using PDF coordinates:
```json
{
  "pages": [{"page_number": 1, "pdf_width": 612, "pdf_height": 792}],
  "form_fields": [
    {
      "description": "Name field",
      "page_number": 1,
      "label_bounding_box": [72, 100, 150, 115],
      "entry_bounding_box": [155, 98, 400, 116],
      "entry_text": {"text": "John Smith", "font": "Helvetica", "font_size": 11}
    }
  ]
}
```

### Approach B — Fallback (scanned PDFs)

Convert to images, determine pixel coordinates visually, then use image-based coordinates:
```json
{
  "pages": [{"page_number": 1, "image_width": 1000, "image_height": 1294}],
  "form_fields": [...]
}
```

### Hybrid

Use Approach A for most fields and Approach B for anything extract_form_structure misses.

---

## Validation

Before generating output, validate bounding boxes:
```bash
python scripts/check_bounding_boxes.py fields.json
```

Visually verify a page:
```bash
python scripts/create_validation_image.py 1 fields.json pages/page_1.png validation_page_1.png
```

Red boxes = entry areas, Blue boxes = label areas.

**Fill with annotations:**
```bash
python scripts/fill_pdf_form_with_annotations.py input.pdf fields.json output.pdf
```

Then convert output to images to verify text placement.
