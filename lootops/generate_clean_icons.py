from PIL import Image, ImageDraw
import os

def create_icon(size, filename):
    # Create image with transparent background
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    center = (size // 2, size // 2)
    cx, cy = center
    
    # 1. Back Glow (Soft) - Adjusted for transparency
    # We want a subtle glow behind, not a solid background
    glow_r = size * 0.45
    for i in range(5):
        r = glow_r - (i * (glow_r/5))
        alpha = int(20 + i * 10)
        width = max(1, size // 20)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(168, 85, 247, alpha), width=width)

    # 2. Radar Rings (Sharp)
    max_r = size // 2.1
    for i in range(2):
        r = max_r - (i * (size // 8))
        if r <= 0: continue
        alpha = int(120 - (i * 40))
        width = max(1, size // 30)
        draw.ellipse(
            [cx-r + width//2, cy-r + width//2, cx+r - width//2, cy+r - width//2], 
            outline=(168, 85, 247, alpha), 
            width=width
        )

    # 3. Crystal / Diamond Shape
    gem_r = size // 2.5
    pts = [
        (cx, cy - gem_r),           # Top
        (cx + gem_r, cy),           # Right
        (cx, cy + gem_r),           # Bottom
        (cx - gem_r, cy)            # Left
    ]
    
    # Facets (Solid Fills for 3D look)
    # Top-Left (Brightest, facing light source)
    draw.polygon([pts[0], pts[3], center], fill=(216, 180, 254, 255))
    # Top-Right
    draw.polygon([pts[0], pts[1], center], fill=(192, 132, 252, 255))
    # Bottom-Left
    draw.polygon([pts[2], pts[3], center], fill=(147, 51, 234, 255))
    # Bottom-Right (Darkest)
    draw.polygon([pts[2], pts[1], center], fill=(126, 34, 206, 255))

    # 4. Core Highlight
    core_r = size // 12
    draw.ellipse([cx-core_r, cy-core_r, cx+core_r, cy+core_r], fill=(255, 255, 255, 180))

    # 5. Crisp Edge Highlights (The "Premium" touch)
    # Highlight top-left edges
    draw.line([pts[0], center], fill=(255, 255, 255, 150), width=max(1, size // 60))
    draw.line([pts[3], center], fill=(255, 255, 255, 80), width=max(1, size // 60))

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    image.save(filename)

sizes = [16, 32, 48, 128]
for s in sizes:
    create_icon(s, f"icons/icon{s}.png")

print("Icons generated successfully!")
