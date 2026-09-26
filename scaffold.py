import os
from pathlib import Path

files = {
    "src/backgrounds/paper.py": '''from PIL import Image, ImageDraw
import random

def generate_paper(width, height, config, seed=None):
    if seed is not None:
        random.seed(seed)
    base_color = random.choice(config.get("base_colors", {}).get("paper", [[240, 230, 210]]))
    img = Image.new("RGB", (width, height), tuple(base_color))
    # Simple procedural variation
    return img
''',
    "src/backgrounds/palm_leaf.py": '''from PIL import Image
import random

def generate_palm_leaf(width, height, config, seed=None):
    if seed is not None:
        random.seed(seed)
    base_color = random.choice(config.get("base_colors", {}).get("palm_leaf", [[180, 160, 120]]))
    img = Image.new("RGB", (width, height), tuple(base_color))
    return img
''',
    "src/backgrounds/aging.py": '''from PIL import Image
def apply_aging(image, config, seed=None):
    # Mock aging by just returning the image
    return image
''',
    "src/rendering/layout.py": '''class Layout:
    def __init__(self, width, height, margins):
        self.width = width
        self.height = height
        self.margins = margins
        self.blocks = []
    
    def add_block(self, text, x, y, w, h, font_info):
        self.blocks.append({
            "text": text,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "font": font_info
        })
''',
    "src/rendering/handwriting.py": '''def apply_handwriting_variation(layout, config):
    # Modify layout positions slightly
    return layout
''',
    "src/rendering/renderer.py": '''from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random

def render_text(image, layout, font_path, config):
    draw = ImageDraw.Draw(image)
    if not font_path or not Path(font_path).exists():
        raise FileNotFoundError(f"Font not found: {font_path}")
    
    try:
        font = ImageFont.truetype(str(font_path), config.get("default_font_size", 40))
    except Exception:
        font = ImageFont.load_default()
        
    for block in layout.blocks:
        draw.text((block["x"], block["y"]), block["text"], font=font, fill=(30, 20, 20))
    return image
''',
    "src/effects/ink.py": '''def apply_ink_effects(image, config, seed=None):
    return image
''',
    "src/effects/deformation.py": '''def apply_deformation(image, config, seed=None):
    return image
''',
    "src/effects/stains.py": '''def apply_stains(image, config, seed=None):
    return image
''',
    "src/effects/noise.py": '''def apply_noise(image, config, seed=None):
    return image
''',
    "src/annotations/markdown.py": '''from pathlib import Path
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
''',
    "src/dataset/splitter.py": '''import math
def get_split(index, total, splits_config):
    # simple deterministic split
    train = splits_config.get("train", 85)
    val = splits_config.get("validation", 10)
    test = splits_config.get("test", 5)
    total_ratio = train + val + test
    
    ratio = index / total * total_ratio
    if ratio < train:
        return "train"
    elif ratio < train + val:
        return "validation"
    else:
        return "test"
''',
    "src/dataset/validator.py": '''from pathlib import Path

def validate_dataset(output_dir, config):
    report = {"passed": True, "errors": []}
    out_path = Path(output_dir)
    if not out_path.exists():
        report["passed"] = False
        report["errors"].append("Output directory does not exist.")
        return report
        
    for script in config.get("scripts", {}).keys():
        script_dir = out_path / script
        if not script_dir.exists():
            continue
            
        for split in ["train", "validation", "test"]:
            split_dir = script_dir / split
            if not split_dir.exists():
                continue
            images = list((split_dir / "images").glob("*.png"))
            mds = list((split_dir / "annotations").glob("*.md"))
            if len(images) != len(mds):
                report["passed"] = False
                report["errors"].append(f"Mismatch in {script}/{split}: {len(images)} images vs {len(mds)} mds")
                
    return report
''',
    "src/pipeline.py": '''from pathlib import Path
from src.text.loader import TextLoader
from src.text.processor import TextProcessor
from src.text.script_registry import ScriptRegistry
from src.backgrounds.paper import generate_paper
from src.backgrounds.palm_leaf import generate_palm_leaf
from src.backgrounds.aging import apply_aging
from src.rendering.layout import Layout
from src.rendering.renderer import render_text
from src.rendering.handwriting import apply_handwriting_variation
from src.effects.ink import apply_ink_effects
from src.effects.deformation import apply_deformation
from src.annotations.markdown import generate_markdown_annotation
from src.dataset.splitter import get_split
import random

class Pipeline:
    def __init__(self, config_path):
        self.registry = ScriptRegistry(config_path)
        self.config = self.registry.config
        
    def generate_image(self, script_name, text, seed, output_dir, split, image_idx):
        script_config = self.registry.get_script_config(script_name)
        fonts = self.registry.discover_fonts(script_name)
        if not fonts:
            raise FileNotFoundError(f"No fonts available for script {script_name}. Cannot generate image.")
            
        font_path = fonts[0]
        
        # 1. Background
        width = self.config.get("image_size", {}).get("width", 1200)
        height = self.config.get("image_size", {}).get("height", 1600)
        bg_type = random.choice(self.config.get("background", {}).get("types", ["paper"]))
        
        if bg_type == "paper":
            img = generate_paper(width, height, self.config.get("background", {}), seed)
        else:
            img = generate_palm_leaf(width, height, self.config.get("background", {}), seed)
            
        img = apply_aging(img, self.config, seed)
        
        # 2. Layout
        layout = Layout(width, height, self.config.get("margins", {}))
        layout.add_block(text, 100, 100, width-200, height-200, str(font_path))
        layout = apply_handwriting_variation(layout, self.config.get("rendering", {}))
        
        # 3. Render
        img = render_text(img, layout, font_path, script_config)
        
        # 4. Effects
        img = apply_ink_effects(img, self.config.get("effects", {}), seed)
        img = apply_deformation(img, self.config.get("effects", {}), seed)
        
        # 5. Save
        filename_base = f"{script_name}_{split}_{image_idx:04d}"
        img_path = Path(output_dir) / script_name / split / "images" / f"{filename_base}.png"
        md_path = Path(output_dir) / script_name / split / "annotations" / f"{filename_base}.md"
        
        img_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        
        img.save(img_path)
        
        # 6. Annotate
        generate_markdown_annotation(md_path, {
            "script": script_name,
            "split": split,
            "seed": seed,
            "image_filename": f"{filename_base}.png",
            "source_text": text,
            "layout": layout.blocks
        })
        return True
'''
}

for path_str, content in files.items():
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

print("Files generated successfully.")
