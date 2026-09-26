from PIL import Image, ImageDraw, ImageEnhance
import random
import numpy as np

def apply_aging(image, config, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        
    effects_config = config.get("effects", {}).get("aging", {})
    if random.random() > effects_config.get("probability", 0.9):
        return image
        
    width, height = image.size
    
    # 1. Yellowing
    yellowing = effects_config.get("yellowing", 0.15)
    yellow_overlay = Image.new("RGBA", (width, height), (220, 200, 100, int(255 * yellowing)))
    image = Image.alpha_composite(image.convert("RGBA"), yellow_overlay).convert("RGB")
    
    # 2. Foxing (brown age spots)
    foxing_count_range = effects_config.get("foxing_count", [5, 25])
    foxing_count = random.randint(foxing_count_range[0], foxing_count_range[1])
    
    draw = ImageDraw.Draw(image, "RGBA")
    for _ in range(foxing_count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(2, 8)
        
        # Foxing spots are usually reddish-brown and semi-transparent
        color = (random.randint(100, 160), random.randint(60, 100), random.randint(20, 50), random.randint(50, 150))
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
        
    # 3. Reduce overall contrast slightly to simulate age fading
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(random.uniform(0.85, 0.95))
    
    return image
