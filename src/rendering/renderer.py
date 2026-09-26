from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import math
import numpy as np

def render_text(image, layout, font_path, script_config, global_config, seed=None):
    if seed is not None:
        random.seed(seed)
        
    if not font_path or not Path(font_path).exists():
        raise FileNotFoundError(f"Font not found: {font_path}")
    
    base_font_size = script_config.get("default_font_size", 40)
    render_config = global_config.get("rendering", {})
    ink_colors = script_config.get("ink_colors", [script_config.get("default_ink_color", [30, 20, 20])])
    
    try:
        font = ImageFont.truetype(str(font_path), base_font_size)
    except Exception:
        font = ImageFont.load_default()
        
    img_rgba = image.convert("RGBA")
    
    for block in layout.blocks:
        x_start, y_start = block["x"], block["y"]
        max_w = block["width"]
        max_h = block["height"]
        
        # Split text into words for wrapping
        # For Indic scripts, word-level rendering preserves conjuncts/ligatures
        raw_words = block["text"].split()
        if not raw_words:
            continue
            
        # If fill_page is true, repeat words to fill the block
        if render_config.get("fill_page", True):
            raw_words = raw_words * 80
            
        # Word-wrap into lines
        lines = []
        current_line = []
        
        for word in raw_words:
            current_line.append(word)
            test_line = " ".join(current_line)
            try:
                bbox = font.getbbox(test_line)
                w = bbox[2] - bbox[0]
            except AttributeError:
                w, _ = font.getsize(test_line)
                
            if w > max_w and len(current_line) > 1:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(" ".join(current_line))
            
        try:
            line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
            if line_height == 0:
                line_height = base_font_size
        except AttributeError:
            line_height = font.getsize("A")[1]
            
        base_line_spacing = int(line_height * script_config.get("line_spacing", 1.5))
        
        y = y_start
        line_idx = 0
        
        # Pick a primary ink color for this block
        primary_color = random.choice(ink_colors)
        
        for line in lines:
            if y + line_height > y_start + max_h:
                break  # Reached bottom of the block
                
            # --- Per-line variations ---
            rot_range = render_config.get("rotation_range", [-1.0, 1.0])
            angle = random.uniform(rot_range[0], rot_range[1])
            
            spacing_var = render_config.get("line_spacing_variation", 5)
            spacing_jitter = random.randint(-spacing_var, spacing_var)
            
            margin_jitter = random.randint(-8, 8)
            
            # Baseline wave parameters (applied at word level)
            baseline_amp = render_config.get("baseline_variation", 4)
            baseline_freq = render_config.get("baseline_frequency", 0.02)
                                            
            # Occasional ink color shift (e.g. new pen dip or red section headers)
            if random.random() < 0.03:
                primary_color = random.choice(ink_colors)
                
            # Per-line ink opacity
            opacity_range = render_config.get("ink_opacity_range", [180, 255])
            line_opacity = random.randint(opacity_range[0], opacity_range[1])
            ink_fill = tuple(primary_color) + (line_opacity,)
            
            # Measure line dimensions
            try:
                bbox = font.getbbox(line)
                lw = bbox[2] - bbox[0]
                lh = bbox[3] - bbox[1] + 10
            except AttributeError:
                lw, lh = font.getsize(line)
                
            # Render the whole line onto a transparent layer (preserves conjuncts)
            pad = 30
            txt_layer = Image.new("RGBA", (lw + 2 * pad, lh + 2 * pad), (0, 0, 0, 0))
            txt_draw = ImageDraw.Draw(txt_layer)
            
            # --- Word-by-word placement with baseline wave ---
            words = line.split(" ")
            cx = pad
            for wi, word in enumerate(words):
                # Baseline sinusoidal offset
                wave_y = int(math.sin(cx * baseline_freq + line_idx * 0.7) * baseline_amp)
                
                # Slight per-word opacity variation
                word_opacity = max(100, min(255, line_opacity + random.randint(-20, 20)))
                word_fill = tuple(primary_color) + (word_opacity,)
                
                txt_draw.text((cx, pad + wave_y), word, font=font, fill=word_fill)
                
                try:
                    ww = font.getbbox(word)[2] - font.getbbox(word)[0]
                except AttributeError:
                    ww = font.getsize(word)[0]
                    
                # Space after word with jitter
                space_w = font.getbbox(" ")[2] - font.getbbox(" ")[0] if hasattr(font, 'getbbox') else font.getsize(" ")[0]
                char_sp_var = render_config.get("char_spacing_variation", 2)
                cx += ww + space_w + random.randint(-char_sp_var, char_sp_var)
                
            # Apply slant (horizontal shear)
            slant_range = render_config.get("slant_range", [-0.04, 0.04])
            slant = random.uniform(slant_range[0], slant_range[1])
            if abs(slant) > 0.005:
                txt_layer = txt_layer.transform(
                    txt_layer.size, Image.AFFINE, 
                    (1, slant, 0, 0, 1, 0), 
                    resample=Image.BICUBIC
                )
                
            # Apply line rotation
            if abs(angle) > 0.1:
                txt_layer = txt_layer.rotate(angle, resample=Image.BICUBIC, expand=1)
                
            # Composite onto main image
            paste_x = max(0, int(x_start + margin_jitter))
            paste_y = max(0, int(y))
            
            # Ensure we don't paste outside image bounds
            if paste_x + txt_layer.width <= img_rgba.width and paste_y + txt_layer.height <= img_rgba.height:
                img_rgba.paste(txt_layer, (paste_x, paste_y), txt_layer)
            
            y += base_line_spacing + spacing_jitter
            line_idx += 1

    return img_rgba.convert("RGB")
