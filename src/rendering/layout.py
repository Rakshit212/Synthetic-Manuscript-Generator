class Layout:
    def __init__(self, width, height, margins):
        self.width = width
        self.height = height
        self.margins = margins
        self.blocks = []
    
    def add_block(self, text, x, y, w, h, font_info):
        self.blocks.append({
            "text": text,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "font": font_info
        })
