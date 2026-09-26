from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np

def apply_stains(image, config, seed=None):
    """
    Add realistic stains: water damage rings, foxing spots, and dark blotches.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    if random.random() > config.get("probability", 0.5):
        return image
        
    width, height = image.size
    max_stains = config.get("max_stains", 4)
    opacity_range = config.get("opacity_range", [20, 80])
    stain_count = random.randint(1, max_stains)
    
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for _ in range(stain_count):
        stain_type = random.choice(["ring", "blotch", "splash"])
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        opacity = random.randint(opacity_range[0], opacity_range[1])
        
        if stain_type == "ring":
            # Water damage ring
            rx = random.randint(30, 120)
            ry = random.randint(25, 100)
            ring_color = (random.randint(120, 170), random.randint(90, 130), random.randint(50, 80), opacity)
            ring_width = random.randint(3, 10)
            draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], outline=ring_color, width=ring_width)
            
        elif stain_type == "blotch":
            # Dark blotch
            rx = random.randint(15, 60)
            ry = random.randint(15, 60)
            blotch_color = (random.randint(100, 160), random.randint(80, 120), random.randint(40, 70), opacity)
            draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=blotch_color)
            
        else:
            # Splash / irregular stain — draw multiple overlapping circles
            for _ in range(random.randint(3, 8)):
                dx = random.randint(-30, 30)
                dy = random.randint(-30, 30)
                r = random.randint(5, 25)
                splash_color = (random.randint(130, 170), random.randint(100, 140), random.randint(50, 80), 
                               random.randint(opacity_range[0], opacity_range[1]))
                draw.ellipse([cx+dx-r, cy+dy-r, cx+dx+r, cy+dy+r], fill=splash_color)
    
    # Blur stains for natural look
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=random.uniform(3, 8)))
    
    # Composite
    result = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    return result
