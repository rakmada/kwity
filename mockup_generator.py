"""
Product Mockup Generator for KDP Notebooks.
Creates a realistic product presentation showing the notebook:
  1. Flat lay / perspective view
  2. "Hand holding" perspective using PIL compositing
Saves as high-quality PNG + PDF page.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from themes import KDP_SPECS


# Mockup canvas settings
MOCKUP_W = 2400
MOCKUP_H = 1800
DPI = 300


def rgb(r, g, b):
    return (r, g, b)


def rgb_a(r, g, b, a=255):
    return (r, g, b, a)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient_bg(draw, w, h, top_color, bottom_color):
    """Draw vertical gradient background."""
    for y in range(h):
        t = y / h
        color = lerp_color(top_color, bottom_color, t)
        draw.line([(0, y), (w, y)], fill=color)


def create_notebook_face(theme, face_w, face_h):
    """
    Create the front face of the notebook as a PIL Image.
    This is a simplified version of the cover design rendered in PIL.
    """
    img = Image.new("RGBA", (face_w, face_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cover_bg = theme["cover_bg"]
    primary = theme["primary"]
    accent = theme["accent"]
    white_c = (255, 255, 255)

    # Background
    draw.rectangle([0, 0, face_w, face_h], fill=cover_bg)

    # Top color band (~45% height)
    band_h = int(face_h * 0.45)
    band_y = face_h - band_h

    # Gradient band
    for y in range(band_h):
        t = y / band_h
        color = lerp_color(primary, lerp_color(primary, cover_bg, 0.3), t)
        draw.line([(0, band_y + y), (face_w, band_y + y)], fill=color)

    # Accent diagonal strip
    accent_pts = [
        (0, band_y),
        (face_w, band_y + int(face_h * 0.04)),
        (face_w, band_y - int(face_h * 0.015)),
        (0, band_y - int(face_h * 0.055)),
    ]
    draw.polygon(accent_pts, fill=accent)

    # Pattern overlay on band
    draw_cover_pattern(draw, theme, 0, band_y, face_w, band_h)

    # Large emoji/icon placeholder circle
    icon_x = int(face_w * 0.7)
    icon_y = int(face_h * 0.75)
    icon_r = int(face_w * 0.18)
    # Glow effect
    for r_off in range(15, 0, -1):
        alpha = int(30 * (1 - r_off / 15))
        glow_color = accent + (alpha,)
        circle_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle_img)
        circle_draw.ellipse(
            [icon_x - icon_r - r_off * 2, icon_y - icon_r - r_off * 2,
             icon_x + icon_r + r_off * 2, icon_y + icon_r + r_off * 2],
            fill=glow_color
        )
        img = Image.alpha_composite(img, circle_img)
        draw = ImageDraw.Draw(img)
    draw.ellipse([icon_x - icon_r, icon_y - icon_r, icon_x + icon_r, icon_y + icon_r],
                 fill=accent + (180,))

    # Try to add emoji text as icon
    try:
        fnt_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(icon_r * 1.0))
    except Exception:
        fnt_large = ImageFont.load_default()

    emoji_text = theme["emoji"]
    bbox = draw.textbbox((0, 0), emoji_text, font=fnt_large)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((icon_x - tw // 2, icon_y - th // 2), emoji_text, font=fnt_large, fill=white_c + (220,))

    # Title text
    try:
        fnt_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(face_w * 0.065))
        fnt_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(face_w * 0.038))
        fnt_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(face_w * 0.028))
    except Exception:
        fnt_title = fnt_sub = fnt_small = ImageFont.load_default()

    # Split tagline
    words = theme["tagline"].split()
    mid = len(words) // 2
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])

    tx = int(face_w * 0.06)
    ty = int(face_h * 0.79)

    draw.text((tx, ty), line1, font=fnt_title, fill=white_c)
    ty2 = ty + int(face_w * 0.075)
    draw.text((tx, ty2), line2, font=fnt_title, fill=white_c)
    ty3 = ty2 + int(face_w * 0.075)
    draw.text((tx, ty3), theme["subtitle"], font=fnt_sub, fill=accent)

    # Bottom bar
    bar_h = int(face_h * 0.06)
    draw.rectangle([0, 0, face_w, bar_h], fill=primary)
    draw.text((tx, int(bar_h * 0.2)), "120 stron • 6×9\" • Notatniki Zawodowe",
              font=fnt_small, fill=white_c)

    return img


def draw_cover_pattern(draw, theme, x, y, w, h):
    """Draw simple pattern elements on cover face."""
    import random
    pattern = theme.get("pattern", "bricks")
    rng = random.Random(42)
    accent_a = theme["accent"] + (25,)

    if pattern == "circuit":
        for _ in range(15):
            nx = x + rng.randint(10, w - 10)
            ny = y + rng.randint(10, h - 10)
            r = rng.randint(3, 8)
            draw.ellipse([nx - r, ny - r, nx + r, ny + r], outline=theme["accent"] + (30,), width=1)
    elif pattern == "bricks":
        bw, bh = w // 8, h // 12
        row = 0
        cy = y
        while cy < y + h:
            offset = bw // 2 if row % 2 else 0
            cx2 = x - offset
            while cx2 < x + w:
                draw.rectangle([cx2, cy, cx2 + bw - 2, cy + bh - 2],
                                outline=theme["cover_bg"] + (40,), width=1)
                cx2 += bw
            cy += bh
            row += 1
    elif pattern == "music":
        for _ in range(12):
            nx = x + rng.randint(20, w - 20)
            ny = y + rng.randint(20, h - 20)
            draw.ellipse([nx - 8, ny - 5, nx + 8, ny + 5], fill=theme["accent"] + (20,))
            draw.line([(nx + 8, ny + 5), (nx + 8, ny - 25)], fill=theme["accent"] + (25,), width=2)
    elif pattern == "leaves":
        for _ in range(15):
            lx = x + rng.randint(0, w)
            ly = y + rng.randint(0, h)
            size = rng.randint(15, 30)
            pts = [(lx, ly), (lx - size // 3, ly + size // 2),
                   (lx, ly + size), (lx + size // 3, ly + size // 2)]
            draw.polygon(pts, fill=theme["primary"] + (20,))
    else:
        # Generic dots
        for _ in range(20):
            dx = x + rng.randint(0, w)
            dy = y + rng.randint(0, h)
            r = rng.randint(2, 8)
            draw.ellipse([dx - r, dy - r, dx + r, dy + r], fill=theme["accent"] + (20,))


def apply_perspective_transform(img, top_left, top_right, bottom_right, bottom_left):
    """
    Apply a perspective (homographic) transform to map a rectangular image
    onto a quadrilateral using PIL's transform.
    """
    src_w, src_h = img.size

    # Destination quad points
    dst = [top_left, top_right, bottom_right, bottom_left]
    # Compute the bounding box of destination
    xs = [p[0] for p in dst]
    ys = [p[1] for p in dst]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    out_w = max_x - min_x
    out_h = max_y - min_y

    # Shift dst to origin
    dst_shifted = [(p[0] - min_x, p[1] - min_y) for p in dst]

    # PIL PERSPECTIVE transform: 8-coefficient transform
    # Solve the transform matrix
    # Using the 4-point perspective transform coefficients
    def find_coeffs(pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
        A = matrix
        b_vec = [p2[x] for p2 in pb for x in range(2)]
        import numpy as np
        res = np.linalg.solve(np.array(A, dtype=float), np.array(b_vec, dtype=float))
        return tuple(res)

    src_pts = [(0, 0), (src_w, 0), (src_w, src_h), (0, src_h)]
    try:
        coeffs = find_coeffs(dst_shifted, src_pts)
        warped = img.transform(
            (out_w, out_h),
            Image.PERSPECTIVE,
            coeffs,
            Image.BICUBIC
        )
    except Exception:
        # Fallback: simple resize
        warped = img.resize((out_w, out_h), Image.BICUBIC)

    return warped, (min_x, min_y)


def create_hand_silhouette(width, height, skin_color=(210, 170, 130)):
    """
    Create a simplified hand/fingers silhouette holding a book from below.
    Returns a PIL RGBA image.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw palm (bottom of image)
    palm_h = int(height * 0.45)
    palm_top = height - palm_h
    draw.rectangle([0, palm_top, width, height], fill=skin_color + (220,))

    # Thumb (left side, angled)
    thumb_w = int(width * 0.18)
    thumb_h = int(height * 0.40)
    thumb_pts = [
        (0, palm_top + int(palm_h * 0.3)),
        (thumb_w, palm_top - thumb_h + int(palm_h * 0.1)),
        (thumb_w + int(thumb_w * 0.3), palm_top - thumb_h + int(palm_h * 0.15)),
        (thumb_w * 2, palm_top + int(palm_h * 0.1)),
        (0, palm_top + int(palm_h * 0.05)),
    ]
    draw.polygon(thumb_pts, fill=skin_color + (215,))

    # 4 fingers (right side, pointing up)
    finger_w = int((width - int(width * 0.2)) / 5)
    finger_base_x = int(width * 0.2)
    finger_heights = [0.65, 0.72, 0.70, 0.58]  # relative heights
    for i, fh_ratio in enumerate(finger_heights):
        fx = finger_base_x + i * finger_w
        fh = int(height * fh_ratio)
        # Rounded finger tip
        draw.rectangle(
            [fx + 2, height - palm_h - fh, fx + finger_w - 2, height - palm_h],
            fill=skin_color + (215,)
        )
        draw.ellipse(
            [fx + 2, height - palm_h - fh - int(finger_w * 0.4),
             fx + finger_w - 2, height - palm_h - fh + int(finger_w * 0.4)],
            fill=skin_color + (215,)
        )
        # Knuckle lines
        knuckle_y = height - palm_h - int(fh * 0.3)
        draw.arc([fx + 3, knuckle_y - 3, fx + finger_w - 3, knuckle_y + 3],
                 start=0, end=180, fill=(skin_color[0] - 30, skin_color[1] - 25, skin_color[2] - 20, 100),
                 width=1)

    # Smooth palm area with ellipse at top of palm
    draw.ellipse([0, palm_top - int(palm_h * 0.1),
                  width, palm_top + int(palm_h * 0.2)],
                 fill=skin_color + (200,))

    # Add subtle shading
    for x in range(width):
        t = abs(x - width / 2) / (width / 2)
        shade = int(30 * t)
        draw.line([(x, palm_top), (x, height)],
                  fill=(max(0, skin_color[0] - shade),
                        max(0, skin_color[1] - shade),
                        max(0, skin_color[2] - shade), 40))

    return img


def generate_mockup(theme_key, theme, cover_image_path=None, output_path="mockup.png"):
    """
    Generate a product mockup showing the notebook in perspective.
    Creates a scene with:
      - Gradient background
      - Notebook shown at a slight angle (perspective)
      - Shadow underneath
      - Hand holding from below (optional)
      - Branding text
    """
    W, H = MOCKUP_W, MOCKUP_H
    mockup = Image.new("RGBA", (W, H), (255, 255, 255, 255))

    # --- Background ---
    bg = Image.new("RGB", (W, H))
    bg_draw = ImageDraw.Draw(bg)
    bg_top = lerp_color(theme["cover_bg"], (30, 30, 50), 0.3)
    bg_bot = lerp_color(theme["cover_bg"], (60, 60, 80), 0.5)
    draw_gradient_bg(bg_draw, W, H, bg_top, bg_bot)

    # Background subtle vignette
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for r in range(min(W, H) // 2, 0, -2):
        alpha = int(80 * (1 - r / (min(W, H) / 2)))
        v_draw.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                       outline=(0, 0, 0, alpha), width=2)
    bg_rgba = bg.convert("RGBA")
    bg_rgba = Image.alpha_composite(bg_rgba, vignette)

    # Subtle pattern on background
    bg_draw2 = ImageDraw.Draw(bg_rgba)
    import random
    rng = random.Random(theme_key.__hash__() % 1000)
    for _ in range(200):
        px = rng.randint(0, W)
        py = rng.randint(0, H)
        pr = rng.randint(1, 3)
        bg_draw2.ellipse([px - pr, py - pr, px + pr, py + pr],
                         fill=theme["accent"] + (8,))

    mockup = Image.alpha_composite(mockup.convert("RGBA"), bg_rgba)

    # --- Create notebook face ---
    # Notebook proportions: 6x9 inches
    nb_face_w = int(W * 0.32)
    nb_face_h = int(nb_face_w * 1.5)  # 9/6 ratio

    nb_face = create_notebook_face(theme, nb_face_w, nb_face_h)

    # --- Main notebook (slight right perspective) ---
    # Position: center-right area
    cx = int(W * 0.52)
    cy = int(H * 0.45)
    skew = int(nb_face_w * 0.04)

    top_left = (cx - nb_face_w // 2 + skew, cy - nb_face_h // 2 - skew)
    top_right = (cx + nb_face_w // 2 + skew, cy - nb_face_h // 2 + skew)
    bottom_right = (cx + nb_face_w // 2 - skew, cy + nb_face_h // 2 + skew)
    bottom_left = (cx - nb_face_w // 2 - skew, cy + nb_face_h // 2 - skew)

    nb_warped, nb_offset = apply_perspective_transform(
        nb_face, top_left, top_right, bottom_right, bottom_left
    )

    # Shadow for main notebook
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_offset = (15, 20)
    shadow_pts = [
        (top_left[0] + shadow_offset[0], top_left[1] + shadow_offset[1]),
        (top_right[0] + shadow_offset[0], top_right[1] + shadow_offset[1]),
        (bottom_right[0] + shadow_offset[0], bottom_right[1] + shadow_offset[1]),
        (bottom_left[0] + shadow_offset[0], bottom_left[1] + shadow_offset[1]),
    ]
    shadow_draw.polygon(shadow_pts, fill=(0, 0, 0, 80))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=12))
    mockup = Image.alpha_composite(mockup, shadow_layer)

    # Paste warped notebook
    nb_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nb_layer.paste(nb_warped, (nb_offset[0], nb_offset[1]), nb_warped)
    mockup = Image.alpha_composite(mockup, nb_layer)

    # Spine strip on left edge of notebook
    spine_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spine_draw = ImageDraw.Draw(spine_layer)
    spine_w_px = int(nb_face_w * 0.04)
    spine_color = theme["primary"] + (230,)
    spine_pts = [
        top_left,
        (top_left[0] + spine_w_px, top_left[1] + spine_w_px // 2),
        (bottom_left[0] + spine_w_px, bottom_left[1] - spine_w_px // 2),
        bottom_left,
    ]
    spine_draw.polygon(spine_pts, fill=spine_color)
    mockup = Image.alpha_composite(mockup, spine_layer)

    # --- Second notebook (slightly behind and to the left) ---
    cx2 = int(W * 0.32)
    cy2 = int(H * 0.47)
    scale2 = 0.88
    nb2_w = int(nb_face_w * scale2)
    nb2_h = int(nb_face_h * scale2)
    skew2 = int(nb2_w * 0.02)

    top_left2 = (cx2 - nb2_w // 2 + skew2, cy2 - nb2_h // 2)
    top_right2 = (cx2 + nb2_w // 2 + skew2, cy2 - nb2_h // 2 + skew2 * 2)
    bottom_right2 = (cx2 + nb2_w // 2 - skew2, cy2 + nb2_h // 2 + skew2 * 2)
    bottom_left2 = (cx2 - nb2_w // 2 - skew2, cy2 + nb2_h // 2)

    # Slightly darker/dimmer version
    nb_face2 = create_notebook_face(theme, nb2_w, nb2_h)
    nb_face2_dark = ImageEnhance.Brightness(nb_face2).enhance(0.7)

    nb2_warped, nb2_offset = apply_perspective_transform(
        nb_face2_dark, top_left2, top_right2, bottom_right2, bottom_left2
    )

    shadow2_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s2_draw = ImageDraw.Draw(shadow2_layer)
    s2_pts = [
        (top_left2[0] + 12, top_left2[1] + 15),
        (top_right2[0] + 12, top_right2[1] + 15),
        (bottom_right2[0] + 12, bottom_right2[1] + 15),
        (bottom_left2[0] + 12, bottom_left2[1] + 15),
    ]
    s2_draw.polygon(s2_pts, fill=(0, 0, 0, 60))
    shadow2_layer = shadow2_layer.filter(ImageFilter.GaussianBlur(radius=10))
    mockup = Image.alpha_composite(mockup, shadow2_layer)

    nb2_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nb2_layer.paste(nb2_warped, (nb2_offset[0], nb2_offset[1]), nb2_warped)
    mockup = Image.alpha_composite(mockup, nb2_layer)

    # --- Hand holding the main notebook from bottom ---
    hand_w = int(nb_face_w * 1.1)
    hand_h = int(nb_face_h * 0.55)
    hand_img = create_hand_silhouette(hand_w, hand_h)

    # Position hand below main notebook
    hand_x = cx - hand_w // 2
    hand_y = cy + nb_face_h // 2 - int(hand_h * 0.28)

    hand_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hand_s_draw = ImageDraw.Draw(hand_shadow)
    hand_s_draw.ellipse([hand_x, hand_y + int(hand_h * 0.7),
                          hand_x + hand_w, hand_y + hand_h + 30],
                         fill=(0, 0, 0, 60))
    hand_shadow = hand_shadow.filter(ImageFilter.GaussianBlur(radius=8))
    mockup = Image.alpha_composite(mockup, hand_shadow)

    hand_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hand_layer.paste(hand_img, (hand_x, hand_y), hand_img)
    mockup = Image.alpha_composite(mockup, hand_layer)

    # --- Text annotations ---
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)

    try:
        fnt_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
        fnt_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        fnt_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        fnt_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except Exception:
        fnt_big = fnt_med = fnt_small = fnt_tiny = ImageFont.load_default()

    # Product title (left side)
    title_x = int(W * 0.04)
    title_y = int(H * 0.15)
    t_draw.text((title_x, title_y), theme["tagline"],
                font=fnt_big, fill=(255, 255, 255, 230))
    title_bb = t_draw.textbbox((title_x, title_y), theme["tagline"], font=fnt_big)
    t_draw.text((title_x, title_bb[3] + 8), theme["subtitle"],
                font=fnt_med, fill=theme["accent"] + (200,))

    # Profession badge
    badge_x = title_x
    badge_y = int(H * 0.32)
    badge_text = f"Dla zawodu: {theme['name_pl']}  {theme['emoji']}"
    badge_bb = t_draw.textbbox((0, 0), badge_text, font=fnt_small)
    bw = badge_bb[2] + 30
    bh = badge_bb[3] + 16
    t_draw.rounded_rectangle([badge_x, badge_y, badge_x + bw, badge_y + bh],
                               radius=8, fill=theme["primary"] + (200,))
    t_draw.text((badge_x + 15, badge_y + 8), badge_text,
                font=fnt_small, fill=(255, 255, 255, 230))

    # Feature bullet points
    features = [
        f"✓  120 stron wysokiej jakości",
        f"✓  5 stron tematycznych",
        f"✓  115 stron w linie",
        f"✓  Format 6×9\" (KDP Standard)",
        f"✓  Idealne na prezent",
    ]
    fy = int(H * 0.44)
    for feat in features:
        t_draw.text((title_x, fy), feat, font=fnt_small, fill=(220, 220, 220, 200))
        fy += 38

    # Bottom branding
    brand_text = "NOTATNIKI ZAWODOWE  •  Quality Professional Notebooks"
    brand_bb = t_draw.textbbox((0, 0), brand_text, font=fnt_tiny)
    bx = (W - brand_bb[2]) // 2
    t_draw.text((bx, int(H * 0.93)), brand_text, font=fnt_tiny,
                fill=theme["accent"] + (150,))

    # Decorative line under title
    t_draw.rectangle([title_x, title_y - 8, title_x + int(W * 0.25), title_y - 4],
                     fill=theme["accent"] + (200,))

    mockup = Image.alpha_composite(mockup, text_layer)

    # Final: flatten to RGB and apply slight sharpening
    final = mockup.convert("RGB")
    final = ImageEnhance.Sharpness(final).enhance(1.2)

    # Save PNG
    final.save(output_path, "PNG", dpi=(DPI, DPI))
    return output_path


def generate_mockup_pdf(theme_key, theme, mockup_png_path, output_pdf_path):
    """
    Wrap the mockup PNG in a PDF page (A4 landscape or letter).
    """
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib.utils import ImageReader

    pdf_w, pdf_h = landscape(letter)
    c = rl_canvas.Canvas(output_pdf_path, pagesize=(pdf_w, pdf_h))

    # Load mockup image
    img = ImageReader(mockup_png_path)

    # Scale to fit page with margin
    margin = 0.3 * 72  # 0.3 inch in points
    avail_w = pdf_w - 2 * margin
    avail_h = pdf_h - 2 * margin

    img_w, img_h = MOCKUP_W, MOCKUP_H
    scale = min(avail_w / img_w, avail_h / img_h)
    drawn_w = img_w * scale
    drawn_h = img_h * scale

    x_pos = (pdf_w - drawn_w) / 2
    y_pos = (pdf_h - drawn_h) / 2

    c.drawImage(img, x_pos, y_pos, drawn_w, drawn_h)
    c.save()

    return output_pdf_path
