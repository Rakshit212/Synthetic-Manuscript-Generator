from PIL import Image, ImageDraw, ImageFont
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
        x, y = block["x"], block["y"]
        max_w = block["width"]
        
        lines = []
        words = block["text"].split()
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = " ".join(current_line)
            try:
                bbox = font.getbbox(test_line)
                w = bbox[2] - bbox[0]
            except AttributeError:
                w, h = font.getsize(test_line)
                
            if w > max_w and len(current_line) > 1:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(" ".join(current_line))
            
        try:
            line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
            if line_height == 0:
                line_height = font.getbbox("T")[3] - font.getbbox("T")[1]
            if line_height == 0:
                line_height = 40
        except AttributeError:
            line_height = font.getsize("A")[1]
            
        line_spacing = int(line_height * config.get("line_spacing", 1.5))
        
        for line in lines:
            draw.text((x, y), line, font=font, fill=(30, 20, 20))
            y += line_spacing

    return image
