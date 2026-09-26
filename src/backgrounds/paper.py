from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np
import cv2

def create_noise_texture(width, height, base_color):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = base_color
    
    # Add gaussian noise
    noise = np.random.normal(0, 6, (height, width, 3)).astype(np.int16)
    img = np.clip(img + noise, 0, 255).astype(np.uint8)
    
    # Add low frequency noise (cloudy texture)
    small_noise = np.random.normal(0, 12, (height // 10, width // 10, 3)).astype(np.float32)
    cloud_noise = cv2.resize(small_noise, (width, height), interpolation=cv2.INTER_CUBIC)
    img = np.clip(img + cloud_noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img)

def apply_vignette(img, intensity=0.4):
    width, height = img.size
    
    # Create radial gradient for vignette
    X, Y = np.meshgrid(np.linspace(-1, 1, width), np.linspace(-1, 1, height))
    radius = np.sqrt(X**2 + Y**2)
    
    # Normalize radius
    radius = radius / np.max(radius)
    
    # Vignette mask
    mask = 1 - (radius * intensity)
    mask = np.clip(mask, 0, 1)
    
    img_np = np.array(img).astype(np.float32)
    
    # Dark brown edge color
    edge_color = np.array([101, 67, 33])
    
    for i in range(3):
        img_np[:, :, i] = img_np[:, :, i] * mask + edge_color[i] * (1 - mask) * intensity
        
    return Image.fromarray(np.clip(img_np, 0, 255).astype(np.uint8))

def generate_paper(width, height, config, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        
    colors = config.get("base_colors", {}).get("paper", [[240, 230, 210]])
    base_color = random.choice(colors)
    
    img = create_noise_texture(width, height, base_color)
    
    # Add paper fibers
    fiber_count = config.get("fiber_count", 40)
    draw = ImageDraw.Draw(img)
    for _ in range(fiber_count):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        length = random.randint(5, 30)
        angle = random.uniform(0, 3.14159)
        x2 = x1 + int(length * np.cos(angle))
        y2 = y1 + int(length * np.sin(angle))
        
        fiber_color = (random.randint(150, 200), random.randint(140, 190), random.randint(120, 170))
        draw.line([x1, y1, x2, y2], fill=fiber_color, width=1)
        
    # Blur slightly to integrate fibers
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
    img = apply_vignette(img, config.get("edge_darkening_intensity", 0.4))
    return img
