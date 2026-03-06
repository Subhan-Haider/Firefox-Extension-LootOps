from PIL import Image, ImageDraw, ImageFont
import os
import math

# Constants
BG_COLOR = (9, 9, 11)        # Obsidian
ACCENT_COLOR = (168, 85, 247) # Violet
ACCENT_DIM = (139, 92, 246)
TEXT_COLOR = (255, 255, 255)
GRID_COLOR = (255, 255, 255, 10)

def draw_hex_icon(draw, center, size, alpha=255):
    """Draws the LootOps Pulse Icon at a specific location"""
    cx, cy = center
    p = size * 0.15
    
    # Pulse Rings
    for i in range(2):
        r = (size // 2) - (i * (size // 6))
        a = max(0, 100 - (i * 40))
        if alpha < 255: a = int(a * (alpha/255))
        w = max(1, size // 24)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(168, 85, 247, a), width=w)

    # Gem Points
    gem_r = size // 2.2
    pts = [
        (cx, cy - gem_r),           # Top
        (cx + gem_r, cy),           # Right
        (cx, cy + gem_r),           # Bottom
        (cx - gem_r, cy)            # Left
    ]
    
    # Facets
    draw.polygon([pts[0], pts[3], (cx, cy)], fill=(192, 132, 252, alpha))
    draw.polygon([pts[0], pts[1], (cx, cy)], fill=(168, 85, 247, alpha))
    draw.polygon([pts[2], pts[3], (cx, cy)], fill=(147, 51, 234, alpha))
    draw.polygon([pts[2], pts[1], (cx, cy)], fill=(126, 34, 206, alpha))

    # Core
    cr = size // 10
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(255, 255, 255, int(150 * (alpha/255))))

def create_grid(draw, width, height, step=40):
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=GRID_COLOR, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=GRID_COLOR, width=1)

def generate_small_tile():
    W, H = 440, 280
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    create_grid(draw, W, H)
    
    # Draw Icon centered but slightly offset
    icon_sz = 160
    draw_hex_icon(draw, (W//2, H//2 - 20), icon_sz)
    
    # Draw Text "LootOps"
    # Using simple drawing for text since we might not have custom fonts
    # We will simulate text with simple geometric shapes or load default
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        text = "LootOps"
        # Calculate text size using getbbox (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((W-tw)/2, H - 70), text, font=font, fill=TEXT_COLOR)
    except Exception:
        # Fallback if arial not found
        pass
        
    img.save("promo_small_tile.png")
    print("Generated promo_small_tile.png")

def generate_marquee_tile():
    W, H = 1400, 560
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    create_grid(draw, W, H, step=60)
    
    # Big Icon on left
    icon_sz = 350
    draw_hex_icon(draw, (300, H//2), icon_sz)
    
    # Draw Text
    try:
        # Title
        font_title = ImageFont.truetype("arial.ttf", 120)
        font_sub = ImageFont.truetype("arial.ttf", 50)
        
        title = "LootOps"
        draw.text((580, 180), title, font=font_title, fill=TEXT_COLOR)
        
        subtitle = "TACTICAL GAME INTEL"
        draw.text((585, 310), subtitle, font=font_sub, fill=ACCENT_COLOR)
        
    except Exception:
        pass

    img.save("promo_marquee_tile.png")
    print("Generated promo_marquee_tile.png")

if __name__ == "__main__":
    generate_small_tile()
    generate_marquee_tile()
