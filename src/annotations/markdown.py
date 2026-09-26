from pathlib import Path
import json

def generate_markdown_annotation(output_path, metadata):
    content = f"""# Manuscript Annotation
    
- Script: {metadata.get("script")}
- Split: {metadata.get("split")}
- Seed: {metadata.get("seed")}
- Image: {metadata.get("image_filename")}

## Source Text
{metadata.get("source_text")}

## Layout Info
```json
{json.dumps(metadata.get("layout", []), indent=2)}
```
"""
    Path(output_path).write_text(content, encoding="utf-8")
