from PIL import Image
import random

def generate_palm_leaf(width, height, config, seed=None):
    if seed is not None:
        random.seed(seed)
    base_color = random.choice(config.get("base_colors", {}).get("palm_leaf", [[180, 160, 120]]))
    img = Image.new("RGB", (width, height), tuple(base_color))
    return img
