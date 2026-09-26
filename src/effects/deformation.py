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
    
    # Create mesh grid
    map_x = np.zeros((height, width), dtype=np.float32)
    map_y = np.zeros((height, width), dtype=np.float32)
    
    for y_coord in range(height):
        for x_coord in range(width):
            map_x[y_coord, x_coord] = x_coord + amp_x * np.sin(freq_y * y_coord + phase_x)
            map_y[y_coord, x_coord] = y_coord + amp_y * np.sin(freq_x * x_coord + phase_y)
    
    # Apply remap
    result = cv2.remap(img_np, map_x, map_y, interpolation=cv2.INTER_LINEAR, 
                       borderMode=cv2.BORDER_REFLECT_101)
    
    return Image.fromarray(result)
