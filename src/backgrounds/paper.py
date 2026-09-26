from PIL import Image, ImageDraw
import random

def generate_paper(width, height, config, seed=None):
    if seed is not None:
        random.seed(seed)
    base_color = random.choice(config.get("base_colors", {}).get("paper", [[240, 230, 210]]))
    img = Image.new("RGB", (width, height), tuple(base_color))
    # Simple procedural variation
    return img
