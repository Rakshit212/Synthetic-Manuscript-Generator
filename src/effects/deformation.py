from PIL import Image
import random
import numpy as np
import cv2

def apply_deformation(image, config, seed=None):
    """
    Apply subtle page warping/deformation to simulate curved or wrinkled manuscript pages.
    Uses sine-wave based mesh distortion.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    if random.random() > config.get("probability", 0.6):
        return image
        
    img_np = np.array(image)
    height, width = img_np.shape[:2]
    
    # Wave parameters
    amp_range = config.get("wave_amplitude", [3, 8])
    freq_range = config.get("wave_frequency", [0.005, 0.015])
    
    amp_x = random.uniform(amp_range[0], amp_range[1])
    amp_y = random.uniform(amp_range[0] * 0.5, amp_range[1] * 0.5)
    freq_x = random.uniform(freq_range[0], freq_range[1])
    freq_y = random.uniform(freq_range[0], freq_range[1])
    phase_x = random.uniform(0, 2 * np.pi)
    phase_y = random.uniform(0, 2 * np.pi)
    
    # Create mesh grid — fully vectorised (replaces the slow per-pixel Python loop)
    x_coords = np.arange(width,  dtype=np.float32)
    y_coords = np.arange(height, dtype=np.float32)
    grid_x, grid_y = np.meshgrid(x_coords, y_coords)

    map_x = (grid_x + amp_x * np.sin(freq_y * grid_y + phase_x)).astype(np.float32)
    map_y = (grid_y + amp_y * np.sin(freq_x * grid_x + phase_y)).astype(np.float32)
    
    # Apply remap
    result = cv2.remap(img_np, map_x, map_y, interpolation=cv2.INTER_LINEAR, 
                       borderMode=cv2.BORDER_REFLECT_101)
    
    return Image.fromarray(result)
