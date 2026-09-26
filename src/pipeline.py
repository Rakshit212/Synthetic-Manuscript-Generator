from pathlib import Path
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
        margins = self.config.get("margins", {})
        x = margins.get("left", 100)
        y = margins.get("top", 100)
        max_w = width - x - margins.get("right", 100)
        max_h = height - y - margins.get("bottom", 100)
        
        layout = Layout(width, height, margins)
        layout.add_block(text, x, y, max_w, max_h, str(font_path))
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
