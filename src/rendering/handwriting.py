import random
import math

def apply_handwriting_variation(layout, rendering_config, seed=None):
    if seed is not None:
        random.seed(seed)
        
    # We apply layout-level variations here, like margin jitter.
    # Line level variations (rotation, baseline curve) are done in renderer.py
    
    margin_jitter = rendering_config.get("margin_jitter", 15)
    
    for block in layout.blocks:
        block["x"] += random.randint(-margin_jitter, margin_jitter)
        # We can also modify the block text or add instructions for renderer,
        # but the renderer handles the line-by-line placement.
        
    return layout
