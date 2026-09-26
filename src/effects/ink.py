from PIL import Image, ImageFilter, ImageEnhance
import random
import numpy as np

def apply_ink_effects(image, config, seed=None):
    """
    Simulate realistic ink effects: bleeding, smudging, and faded strokes.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    if random.random() > config.get("probability", 0.7):
        return image
        
    width, height = image.size
    img_np = np.array(image).astype(np.float32)
    
    # 1. Localized ink bleeding — find dark (text) pixels and dilate them
    gray = np.mean(img_np, axis=2)
    # Threshold to find text regions (dark pixels)
    text_mask = (gray < 100).astype(np.uint8) * 255
    
    if np.sum(text_mask) > 0:
        # Create bleeding by blurring the text mask
        intensity_range = config.get("intensity_range", [1.0, 2.5])
        blur_radius = random.uniform(intensity_range[0], intensity_range[1])
        
        text_mask_img = Image.fromarray(text_mask)
        bled_mask = text_mask_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        bled_np = np.array(bled_mask).astype(np.float32) / 255.0
        
        # Darken pixels where the bleed mask is active
        bleed_color = np.array([40, 30, 25], dtype=np.float32)
        for c in range(3):
            bleed_contribution = bled_np * bleed_color[c] * 0.3
            img_np[:, :, c] = img_np[:, :, c] * (1 - bled_np * 0.15) + bleed_contribution
    
    # 2. Random ink smudges — small directional blurs at random locations
    max_smudges = config.get("max_smudges", 5)
    smudge_count = random.randint(0, max_smudges)
    
    result = Image.fromarray(np.clip(img_np, 0, 255).astype(np.uint8))
    
    for _ in range(smudge_count):
        sx = random.randint(0, width - 60)
        sy = random.randint(0, height - 40)
        sw = random.randint(30, 80)
        sh = random.randint(20, 50)
        
        # Crop the region
        region = result.crop((sx, sy, sx + sw, sy + sh))
        # Apply directional blur (horizontal or vertical)
        if random.random() > 0.5:
            region = region.filter(ImageFilter.GaussianBlur(radius=random.uniform(2, 5)))
        else:
            # Motion-like blur by repeated box blur in one direction
            region = region.filter(ImageFilter.BoxBlur(radius=random.randint(2, 4)))
        
        # Paste back with slight offset
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-2, 2)
        result.paste(region, (sx + offset_x, sy + offset_y))
    
    # 3. Subtle contrast and sharpness adjustments for age effect
    enhancer = ImageEnhance.Contrast(result)
    result = enhancer.enhance(random.uniform(0.88, 0.98))
    
    return result
