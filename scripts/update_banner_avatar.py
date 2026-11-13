"""
Banner Customizer & Avatar Remover Script
Author: Satyanand Gupta / Antigravity Assistant

This script automatically detects the circular avatar in GitHub-Profile-banner.png,
removes the photo, and replaces it with a clean, high-resolution glowing neon cyber
developer emblem (< / >) that blends with the surrounding neon circuitry.
"""

import math
import os
from PIL import Image, ImageDraw

def process_banner(
    input_path="GitHub-Profile-banner.original.png",
    output_path="GitHub-Profile-banner.png",
    emblem_type="code"
):
    if not os.path.exists(input_path):
        if os.path.exists("GitHub-Profile-banner.png"):
            input_path = "GitHub-Profile-banner.png"
        else:
            raise FileNotFoundError(f"Input banner not found at {input_path}")

    orig = Image.open(input_path).convert('RGBA')
    w, h = orig.size
    print(f"Loaded banner: {w}x{h}")

    # Circle center and radius on the banner
    cx, cy, r = 784.0, 177.0, 121.0

    # 4x Super-sampling for razor-sharp rendering
    scale = 4
    R = int(r * scale)
    size = R * 2 + 20 * scale
    ocx, ocy = size // 2, size // 2

    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    # Radial background gradient from dark cyber blue to deeper navy
    for y in range(size):
        for x in range(size):
            dist = math.hypot(x - ocx, y - ocy)
            if dist <= R:
                t = dist / R
                red = int(13 * (1 - t) + 7 * t)
                green = int(39 * (1 - t) + 21 * t)
                blue = int(76 * (1 - t) + 39 * t)
                canvas.putpixel((x, y), (red, green, blue, 255))

    draw = ImageDraw.Draw(canvas)

    # Concentric cyber rings
    rings = [
        (int(R * 0.90), (0, 247, 255, 140), 3 * scale),
        (int(R * 0.82), (0, 180, 255, 90), 2 * scale),
        (int(R * 0.70), (0, 247, 255, 60), 2 * scale),
        (int(R * 0.55), (0, 180, 255, 50), 2 * scale)
    ]
    for rad, col, width in rings:
        draw.ellipse([ocx - rad, ocy - rad, ocx + rad, ocy + rad], outline=col, width=width)

    # Outer tech ticks
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        r_in = R * 0.88
        r_out = R * 0.93
        x1 = ocx + r_in * math.cos(rad)
        y1 = ocy + r_in * math.sin(rad)
        x2 = ocx + r_out * math.cos(rad)
        y2 = ocy + r_out * math.sin(rad)
        draw.line([x1, y1, x2, y2], fill=(0, 247, 255, 180 if deg % 30 == 0 else 80), width=2 * scale)

    # Neon glowing dots on compass points
    for deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(deg)
        px = ocx + (R * 0.82) * math.cos(rad)
        py = ocy + (R * 0.82) * math.sin(rad)
        dot_r = 5 * scale
        draw.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r], fill=(0, 255, 255, 230))

    if emblem_type == "code":
        # Draw code symbol: < / >
        emblem_scale = scale * 1.6
        bracket_w = int(14 * emblem_scale)
        bracket_h = int(24 * emblem_scale)
        slash_h = int(32 * emblem_scale)
        sep = int(22 * emblem_scale)

        # Glow and Core for '<'
        draw.line([(ocx - sep, ocy), (ocx - sep + bracket_w, ocy - bracket_h)], fill=(0, 247, 255, 100), width=10 * scale)
        draw.line([(ocx - sep, ocy), (ocx - sep + bracket_w, ocy + bracket_h)], fill=(0, 247, 255, 100), width=10 * scale)
        draw.line([(ocx - sep, ocy), (ocx - sep + bracket_w, ocy - bracket_h)], fill=(255, 255, 255, 255), width=5 * scale)
        draw.line([(ocx - sep, ocy), (ocx - sep + bracket_w, ocy + bracket_h)], fill=(255, 255, 255, 255), width=5 * scale)

        # Glow and Core for '/'
        draw.line([(ocx + 8 * scale, ocy - slash_h), (ocx - 8 * scale, ocy + slash_h)], fill=(0, 210, 255, 120), width=10 * scale)
        draw.line([(ocx + 8 * scale, ocy - slash_h), (ocx - 8 * scale, ocy + slash_h)], fill=(255, 255, 255, 255), width=5 * scale)

        # Glow and Core for '>'
        draw.line([(ocx + sep, ocy), (ocx + sep - bracket_w, ocy - bracket_h)], fill=(0, 247, 255, 100), width=10 * scale)
        draw.line([(ocx + sep, ocy), (ocx + sep - bracket_w, ocy + bracket_h)], fill=(0, 247, 255, 100), width=10 * scale)
        draw.line([(ocx + sep, ocy), (ocx + sep - bracket_w, ocy - bracket_h)], fill=(255, 255, 255, 255), width=5 * scale)
        draw.line([(ocx + sep, ocy), (ocx + sep - bracket_w, ocy + bracket_h)], fill=(255, 255, 255, 255), width=5 * scale)

    # Outer border circle
    draw.ellipse([ocx - R, ocy - R, ocx + R, ocy + R], outline=(0, 247, 255, 255), width=3 * scale)

    # Mask for smooth downsampling
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([ocx - R, ocy - R, ocx + R, ocy + R], fill=255)

    final_size = size // scale
    patch = canvas.resize((final_size, final_size), Image.Resampling.LANCZOS)
    patch_mask = mask.resize((final_size, final_size), Image.Resampling.LANCZOS)

    result = orig.copy()
    paste_x = int(cx - final_size // 2)
    paste_y = int(cy - final_size // 2)
    result.paste(patch, (paste_x, paste_y), patch_mask)
    result.save(output_path)
    print(f"Banner saved successfully to {output_path}")

if __name__ == "__main__":
    process_banner()

