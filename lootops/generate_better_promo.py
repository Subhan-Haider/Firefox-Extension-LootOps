from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import math

# Constants
BG_COLOR = (5, 5, 8)         # Deep Obsidian (Darker)
ACCENT_COLOR = (168, 85, 247) # Violet
ACCENT_BRIGHT = (216, 180, 254)
TEXT_COLOR = (255, 255, 255)
GRID_COLOR = (255, 255, 255, 15)

def draw_radial_gradient(draw, width, height, inner_color, outer_color):
    center = (width // 2, height // 2)
    max_dist = math.sqrt(center[0]**2 + center[1]**2)
    
    # We can't do true pixel-shader gradients efficiently in pure PIL python loops for large images
    # So we cheat: draw expanding concentric circles from outside in? No, that's hard.
    # Faster cheat: Create a small gradient image and resize it?
    # Let's simple fill with outer, and draw a large radial light in center
    
    draw.rectangle([0,0,width,height], fill=outer_color)
    
    # Draw a glow in the center
    layers = 40
    for i in range(layers):
        r = int(max(width, height) * (1.0 - (i/layers)) * 0.8)
        alpha = int(255 * (i/layers) * 0.1) # vary alpha
        
        # interpolate color
        # actually just a simple violet glow
        c = (60, 20, 80) # Dark violet
        
        x0 = center[0] - r
        y0 = center[1] - r * 0.8 # Squish slightly
        x1 = center[0] + r
        y1 = center[1] + r * 0.8
        
        draw.ellipse([x0, y0, x1, y1], fill=(c[0], c[1], c[2], 5))

def draw_hud_overlay(draw, w, h):
    # Tech corners
    c_len = 20
    c_col = (168, 85, 247, 150)
    thk = 3
    
    # Top Left
    draw.line([(10, 10), (10+c_len, 10)], fill=c_col, width=thk)
    draw.line([(10, 10), (10, 10+c_len)], fill=c_col, width=thk)
    
    # Top Right
    draw.line([(w-10, 10), (w-10-c_len, 10)], fill=c_col, width=thk)
    draw.line([(w-10, 10), (w-10, 10+c_len)], fill=c_col, width=thk)
    
    # Bottom Left
    draw.line([(10, h-10), (10+c_len, h-10)], fill=c_col, width=thk)
    draw.line([(10, h-10), (10, h-10-c_len)], fill=c_col, width=thk)
    
    # Bottom Right
    draw.line([(w-10, h-10), (w-10-c_len, h-10)], fill=c_col, width=thk)
    draw.line([(w-10, h-10), (w-10, h-10-c_len)], fill=c_col, width=thk)
    
    # Scanlines
    for y in range(0, h, 4):
        draw.line([(0, y), (w, y)], fill=(0,0,0, 30), width=1)

def draw_glow_text(draw, x, y, text, font, base_color=(255,255,255), glow_color=(168, 85, 247)):
    # Draw glow layers
    # We need to draw text multiple times with slight offsets or just width outline
    # PIL Text borders are okay
    
    # 1. Broad soft glow
    for off in range(6, 0, -1):
        alpha = int(10 + (6-off)*5)
        # We can't actually blur text easily without blurring image
        # Instead, we draw the text in glow color with stroke_width
        draw.text((x, y), text, font=font, fill=None, stroke_width=off*2, stroke_fill=(glow_color[0], glow_color[1], glow_color[2], 10))

    # 2. Main Text
    draw.text((x, y), text, font=font, fill=base_color)

def draw_starfield(draw, width, height, count=100):
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        alpha = random.randint(50, 200)
        size = random.randint(1, 2)
        draw.ellipse([x, y, x+size, y+size], fill=(255, 255, 255, alpha))

def draw_premium_icon(draw, center, size):
    cx, cy = center
    
    # 1. Back Glow (Soft)
    glow_r = size * 0.7
    for i in range(10):
        r = glow_r - (i * (glow_r/10))
        alpha = int(10 + i * 5)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=None, outline=(168, 85, 247, alpha), width=size//10)
        
    # 2. Radar Rings (Sharp)
    for i in range(3):
        r = (size * 0.6) + (i * (size * 0.15))
        alpha = int(80 - (i * 20))
        width = max(1, size // 40)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(168, 85, 247, alpha), width=width)

    # 3. The Crystal (Diamond Shape)
    gem_size = size * 0.4
    pts = [
        (cx, cy - gem_size),           # Top
        (cx + gem_size, cy),           # Right
        (cx, cy + gem_size),           # Bottom
        (cx - gem_size, cy)            # Left
    ]
    
    # Draw Facets with gradients simulated by solid fills
    draw.polygon([pts[0], pts[3], (cx, cy)], fill=(216, 180, 254, 255)) # Top-Left (Brightest)
    draw.polygon([pts[0], pts[1], (cx, cy)], fill=(192, 132, 252, 255)) # Top-Right
    draw.polygon([pts[2], pts[3], (cx, cy)], fill=(147, 51, 234, 255))  # Bottom-Left
    draw.polygon([pts[2], pts[1], (cx, cy)], fill=(107, 33, 168, 255))  # Bottom-Right (Darkest)
    
    # 4. White Core Highlight
    core_r = size * 0.05
    draw.ellipse([cx-core_r, cy-core_r, cx+core_r, cy+core_r], fill=(255, 255, 255, 200))
    
    # 5. Edge Highlights on Gem
    draw.line([pts[0], (cx, cy)], fill=(255,255,255,100), width=2)
    draw.line([pts[3], (cx, cy)], fill=(255,255,255,50), width=2)

def generate_tiles():
    font_path = "arial.ttf"
    try: font_path = "C:\\Windows\\Fonts\\segoeui.ttf" 
    except: pass
    try: 
        # Attempt to load a bold font for the title
        title_font_path = "C:\\Windows\\Fonts\\segoeuib.ttf"
        ImageFont.truetype(title_font_path, 20)
    except:
        title_font_path = font_path

    # --- Cinematic Small Tile (440x280) ---
    W, H = 440, 280
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # 1. Background
    draw_radial_gradient(draw, W, H, (30, 0, 40), BG_COLOR)
    
    # 2. Subtle Icon Watermark (Huge, faint)
    watermark_size = 360
    # Create temp image for watermark to handle alpha correctly
    wm = Image.new('RGBA', (W, H), (0,0,0,0))
    wm_draw = ImageDraw.Draw(wm)
    # Draw faint icon
    draw_premium_icon(wm_draw, (W//2, H//2), watermark_size)
    # Fade it out - We need to reduce alpha of the whole layer
    # Simple hack: draw it with very low alpha colors in the helper function?
    # No, let's just use the drawn layer and composite it with reduced opacity
    # ACTUALLY, simpler: just draw radial rings faintly here manually
    cx, cy = W//2, H//2
    for i in range(3):
        r = 100 + i*40
        width = 2
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(168,85,247, 30), width=2)
    
    # 3. Text
    try:
        f_title = ImageFont.truetype(title_font_path, 64)
        f_sub = ImageFont.truetype(font_path, 20)
        
        text = "LootOps"
        bbox = draw.textbbox((0,0), text, font=f_title)
        tx = (W - (bbox[2]-bbox[0])) // 2
        ty = (H - (bbox[3]-bbox[1])) // 2 - 15
        
        draw_glow_text(draw, tx, ty, text, f_title)
        
        sub = "TACTICAL INTEL"
        sbbox = draw.textbbox((0,0), sub, font=f_sub)
        sx = (W - (sbbox[2]-sbbox[0])) // 2
        draw.text((sx, ty + 75), sub, font=f_sub, fill=ACCENT_BRIGHT, spacing=10)
        
    except:
        pass
        
    # 4. HUD Overlay
    draw_hud_overlay(draw, W, H)

    img.save("promo_small_tile.png")

    # --- Marquee (Keep existing premium logic but apply HUD) ---
    W, H = 1400, 560
    img2 = Image.new('RGB', (W, H), BG_COLOR)
    draw2 = ImageDraw.Draw(img2, 'RGBA')
    draw_radial_gradient(draw2, W, H, (40, 0, 50), BG_COLOR)
    draw_starfield(draw2, W, H, 100)
    draw_premium_icon(draw2, (350, H//2), 380)
    
    try:
        f_t = ImageFont.truetype(title_font_path, 120)
        f_s = ImageFont.truetype(font_path, 40)
        draw_glow_text(draw2, 650, 180, "LootOps", f_t)
        draw2.text((660, 310), "EPIC & STEAM INTEL", font=f_s, fill=ACCENT_BRIGHT)
        
        # Badge
        draw2.rounded_rectangle([660, 380, 880, 430], radius=10, outline=ACCENT_COLOR, width=2)
        draw2.text((695, 392), "FREE FOREVER", font=ImageFont.truetype(font_path, 25), fill=TEXT_COLOR)
    except: pass
    
    draw_hud_overlay(draw2, W, H)
    img2.save("promo_marquee_tile.png")

    print("Generated Cinematic Tiles")

if __name__ == "__main__":
    generate_tiles()
