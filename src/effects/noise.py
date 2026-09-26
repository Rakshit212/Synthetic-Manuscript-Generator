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
    
    # Dark specks (dirt, debris)
    for _ in range(num_specks):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        darkness = random.randint(0, 80)
        img_np[y, x] = [darkness, darkness, darkness]
    
    # Light specks (paper fiber highlights)
    for _ in range(num_specks // 3):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        lightness = random.randint(200, 255)
        img_np[y, x] = [lightness, lightness, lightness]
    
    return Image.fromarray(np.clip(img_np, 0, 255).astype(np.uint8))
