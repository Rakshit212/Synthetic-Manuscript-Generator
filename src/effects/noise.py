from PIL import Image
import random
import numpy as np

def apply_noise(image, config, seed=None):
    """
    Add realistic paper noise: gaussian grain and speckle.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    if random.random() > config.get("probability", 0.8):
        return image
        
    width, height = image.size
    img_np = np.array(image).astype(np.float32)
    
    # 1. Gaussian noise for paper grain
    sigma = config.get("gaussian_sigma", 3)
    gaussian_noise = np.random.normal(0, sigma, img_np.shape).astype(np.float32)
    img_np = img_np + gaussian_noise
    
    # 2. Speckle noise (salt-and-pepper-like dark/light spots)
    density = config.get("speckle_density", 0.002)
    total_pixels = width * height
    num_specks = int(total_pixels * density)
    
    # Dark specks (dirt, debris) — vectorised
    if num_specks > 0:
        xs = np.random.randint(0, width,  num_specks)
        ys = np.random.randint(0, height, num_specks)
        darkness = np.random.randint(0, 80, num_specks)
        img_np[ys, xs] = np.stack([darkness, darkness, darkness], axis=1)

    # Light specks (paper fiber highlights) — vectorised
    num_light = num_specks // 3
    if num_light > 0:
        xs = np.random.randint(0, width,  num_light)
        ys = np.random.randint(0, height, num_light)
        lightness = np.random.randint(200, 255, num_light)
        img_np[ys, xs] = np.stack([lightness, lightness, lightness], axis=1)
    
    return Image.fromarray(np.clip(img_np, 0, 255).astype(np.uint8))
