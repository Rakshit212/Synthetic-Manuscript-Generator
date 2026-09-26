from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np
import cv2
from src.backgrounds.paper import create_noise_texture, apply_vignette

def generate_palm_leaf(width, height, config, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        
    colors = config.get("base_colors", {}).get("palm_leaf", [[180, 160, 120]])
    base_color = random.choice(colors)
    
    # Base texture
    img = create_noise_texture(width, height, base_color)
    img_np = np.array(img).astype(np.float32)
    
    # Add horizontal palm leaf striations
    striation_noise = np.random.normal(0, 20, (height, width // 20, 3)).astype(np.float32)
    striation_noise = cv2.resize(striation_noise, (width, height), interpolation=cv2.INTER_LINEAR)
    
    # Enhance horizontal blur
    striation_noise = cv2.blur(striation_noise, (50, 1))
    
    img_np = np.clip(img_np + striation_noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_np)
    
    # Draw binding holes (typically 1 or 2 in palm leaf manuscripts)
    draw = ImageDraw.Draw(img)
    hole_radius = random.randint(15, 25)
    
    has_holes = random.random() > 0.3
    if has_holes:
        # Central hole or two holes
        if random.random() > 0.5:
            # One central hole
            hx, hy = width // 2, height // 2
            draw.ellipse([hx-hole_radius, hy-hole_radius, hx+hole_radius, hy+hole_radius], fill=(40, 30, 20))
            # Ring around hole
            draw.ellipse([hx-hole_radius-2, hy-hole_radius-2, hx+hole_radius+2, hy+hole_radius+2], outline=(100, 80, 50), width=3)
        else:
            # Two holes
            hx1, hy1 = int(width * 0.3), height // 2
            hx2, hy2 = int(width * 0.7), height // 2
            draw.ellipse([hx1-hole_radius, hy1-hole_radius, hx1+hole_radius, hy1+hole_radius], fill=(40, 30, 20))
            draw.ellipse([hx1-hole_radius-2, hy1-hole_radius-2, hx1+hole_radius+2, hy1+hole_radius+2], outline=(100, 80, 50), width=3)
            
            draw.ellipse([hx2-hole_radius, hy2-hole_radius, hx2+hole_radius, hy2+hole_radius], fill=(40, 30, 20))
            draw.ellipse([hx2-hole_radius-2, hy2-hole_radius-2, hx2+hole_radius+2, hy2+hole_radius+2], outline=(100, 80, 50), width=3)

    img = apply_vignette(img, config.get("edge_darkening_intensity", 0.5))
    return img
