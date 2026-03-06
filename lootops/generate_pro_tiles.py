from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

# --- Configuration ---
SCALE = 4  # Super-sampling factor (Draw 4x bigger, resize down for smooth edges)
BG_TOP = (20, 10, 30)      # Deep Violet-Black
BG_BOTTOM = (46, 16, 101)  # Rich Violet
ACCENT = (167, 139, 250)   # Light Violet
ACCENT_GLOW = (139, 92, 246)
TEXT_WHITE = (255, 255, 255)

def get_font(size, is_bold=False):
    """Try to load a high-quality system font"""
    fonts = [
        "meiryo.ttc", "consola.ttf", "arialbd.ttf", "arial.ttf", 
        "segoeuib.ttf", "segoeui.ttf",  # Windows
        "Helvetica.ttc", ".SFNSDisplay.ttf", # Mac
        "DejaVuSans-Bold.ttf", "DejaVuSans.ttf" # Linux
    ]
    
    # Adjust size for super-sampling
    scaled_size = size * SCALE
    
    for font_name in fonts:
        try:
            # Check standard Windows path first for common fonts
            if os.path.exists(f"C:\\Windows\\Fonts\\{font_name}"):
                return ImageFont.truetype(f"C:\\Windows\\Fonts\\{font_name}", scaled_size)
            # Try direct load (if in path)
            return ImageFont.truetype(font_name, scaled_size)
        except:
            continue
            
    # Fallback default
    return ImageFont.load_default()

def draw_gradient_bg(draw, w, h):
    """Draws a smooth vertical linear gradient"""
    # For a perfect gradient in PIL we draw lines
    # Since we are super-sampling, this loop might be slow if we do every pixel row
    # Let's do steps of SCALE size (which maps to 1 pixel in final) to speed up
    
    r1, g1, b1 = BG_TOP
    r2, g2, b2 = BG_BOTTOM
    
    for y in range(0, h, 2): # Step 2 for speed, barely noticeable
        f = y / h
        r = int(r1 + (r2 - r1) * f)
        g = int(g1 + (g2 - g1) * f)
        b = int(b1 + (b2 - b1) * f)
        draw.line([(0, y), (w, y)], fill=(r, g, b), width=2)

def draw_tech_grid(draw, w, h):
    """Draws a subtle tactical grid overlay"""
    step = 80 * SCALE
    color = (255, 255, 255, 10) # Very faint
    
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=color, width=SCALE)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=color, width=SCALE)

def draw_pro_icon(draw, center_x, center_y, size):
    """Draws the anti-aliased LootPulse Gem"""
    s = size
    cx, cy = center_x, center_y
    
    # 1. Outer Pulse Rings (Fading opacity)
    for i in range(3):
        radius = (s * 0.7) + (i * s * 0.15)
        alpha = int(60 - (i * 20))
        width = int(s * 0.02)
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        draw.ellipse(bbox, outline=(167, 139, 250, alpha), width=width)
        
    # 2. Main Hexagon / Gem Background (Darker container)
    gem_r = s * 0.4
    poly_pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30) # Point up
        px = cx + gem_r * math.cos(angle)
        py = cy + gem_r * math.sin(angle)
        poly_pts.append((px, py))
    
    draw.polygon(poly_pts, fill=(20, 10, 30, 200), outline=(139, 92, 246, 255))
    
    # 3. Inner Diamond (The "Loot")
    d_r = s * 0.25
    diamond = [
        (cx, cy - d_r), (cx + d_r, cy), (cx, cy + d_r), (cx - d_r, cy)
    ]
    # Draw facets
    # Top Left
    draw.polygon([diamond[0], diamond[3], (cx,cy)], fill=(200, 180, 255, 255))
    # Top Right
    draw.polygon([diamond[0], diamond[1], (cx,cy)], fill=(160, 140, 250, 255))
    # Bottom Right
    draw.polygon([diamond[2], diamond[1], (cx,cy)], fill=(100, 60, 180, 255))
    # Bottom Left
    draw.polygon([diamond[2], diamond[3], (cx,cy)], fill=(120, 80, 200, 255))
    
    # 4. Highlight Sparkle
    sparkle_len = s * 0.3
    w = int(s * 0.01)
    draw.line([(cx, cy - sparkle_len), (cx, cy + sparkle_len)], fill=(255, 255, 255, 100), width=w)
    draw.line([(cx - sparkle_len, cy), (cx + sparkle_len, cy)], fill=(255, 255, 255, 100), width=w)
    draw.ellipse([cx - w*2, cy - w*2, cx + w*2, cy + w*2], fill=(255, 255, 255, 255))

def generate_assets():
    print("Generating Pro Assets with 4x Super-Sampling...")
    
    # --- 1. Small Tile (440x280) ---
    W, H = 440, 280
    img = Image.new('RGB', (W * SCALE, H * SCALE), BG_TOP)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Background
    draw_gradient_bg(draw, W*SCALE, H*SCALE)
    draw_tech_grid(draw, W*SCALE, H*SCALE)
    
    # Logo
    draw_pro_icon(draw, (W//2)*SCALE, (H//2 - 20)*SCALE, 140*SCALE)
    
    # Text
    f_title = get_font(50, True)
    text = "LootOps"
    bbox = draw.textbbox((0,0), text, font=f_title)
    tx = ((W*SCALE) - (bbox[2]-bbox[0])) // 2
    
    # Text Shadow (Glow)
    draw.text((tx, (H-60)*SCALE), text, font=f_title, fill=(139, 92, 246, 100), stroke_width=4*SCALE, stroke_fill=(139, 92, 246, 50))
    # Main Text
    draw.text((tx, (H-60)*SCALE), text, font=f_title, fill=TEXT_WHITE)
    
    # Downscale for smooth AA
    img = img.resize((W, H), resample=Image.LANCZOS)
    img.save("promo_small_tile.png")
    print("Saved promo_small_tile.png")

    # --- 2. Marquee Tile (1400x560) ---
    W, H = 1400, 560
    img = Image.new('RGB', (W * SCALE, H * SCALE), BG_TOP)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    draw_gradient_bg(draw, W*SCALE, H*SCALE)
    draw_tech_grid(draw, W*SCALE, H*SCALE)
    
    # Icon Left
    draw_pro_icon(draw, 350*SCALE, (H//2)*SCALE, 400*SCALE)
    
    # Text Right
    f_big = get_font(120, True)
    f_sub = get_font(40, True)
    
    title = "LootOps"
    draw.text((650*SCALE, 160*SCALE), title, font=f_big, fill=TEXT_WHITE)
    
    sub = "TACTICAL INTEL / EPIC & STEAM"
    draw.text((660*SCALE, 300*SCALE), sub, font=f_sub, fill=ACCENT_GLOW)
    
    # Badge
    badge_rect = [660*SCALE, 380*SCALE, 950*SCALE, 440*SCALE]
    draw.rounded_rectangle(badge_rect, radius=20*SCALE, fill=None, outline=ACCENT, width=3*SCALE)
    draw.text((690*SCALE, 390*SCALE), "100% FREE TRACKER", font=f_sub, fill=TEXT_WHITE)

    img = img.resize((W, H), resample=Image.LANCZOS)
    img.save("promo_marquee_tile.png")
    print("Saved promo_marquee_tile.png")

if __name__ == "__main__":
    generate_assets()
