"""
KDP Notebook Cover Generator.
Generates front and back covers as PDF pages using ReportLab.
KDP full cover = front + spine + back in one landscape PDF.
"""

import math
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from themes import KDP_SPECS


def rgb(r, g, b):
    return Color(r / 255, g / 255, b / 255)


def hex_to_color(hex_str):
    return HexColor(hex_str)


def draw_brick_pattern(c, x, y, w, h, color, alpha=0.15):
    """Draw repeating brick pattern."""
    c.saveState()
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setFillAlpha(alpha)
    c.setStrokeAlpha(alpha)
    brick_w, brick_h = 40, 20
    gap = 3
    row = 0
    cy = y
    while cy < y + h:
        offset = (brick_w / 2) if row % 2 else 0
        cx = x - offset
        while cx < x + w:
            c.rect(cx, cy, brick_w - gap, brick_h - gap, fill=1, stroke=0)
            cx += brick_w
        cy += brick_h
        row += 1
    c.restoreState()


def draw_circuit_pattern(c, x, y, w, h, color, alpha=0.12):
    """Draw circuit board pattern."""
    c.saveState()
    c.setStrokeColor(color)
    c.setStrokeAlpha(alpha)
    c.setLineWidth(0.8)
    import random
    rng = random.Random(42)
    nodes = [(x + rng.uniform(20, w - 20), y + rng.uniform(20, h - 20)) for _ in range(30)]
    for i, (nx, ny) in enumerate(nodes):
        c.circle(nx, ny, 3, fill=0, stroke=1)
        for j in range(rng.randint(1, 3)):
            tx, ty = rng.choice(nodes)
            if rng.random() > 0.5:
                mid_x = nx
                c.line(nx, ny, mid_x, ty)
                c.line(mid_x, ty, tx, ty)
            else:
                mid_y = ny
                c.line(nx, ny, tx, mid_y)
                c.line(tx, mid_y, tx, ty)
    c.restoreState()


def draw_music_pattern(c, x, y, w, h, color, alpha=0.12):
    """Draw musical notes pattern."""
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setFillAlpha(alpha)
    c.setStrokeAlpha(alpha)
    import random
    rng = random.Random(7)
    for _ in range(20):
        nx = x + rng.uniform(10, w - 10)
        ny = y + rng.uniform(10, h - 10)
        size = rng.uniform(8, 20)
        c.ellipse(nx, ny, nx + size * 0.8, ny + size * 0.6, fill=1, stroke=0)
        c.line(nx + size * 0.8, ny + size * 0.6, nx + size * 0.8, ny + size * 2.5)
    c.restoreState()


def draw_leaf_pattern(c, x, y, w, h, color, alpha=0.12):
    """Draw simple leaf shapes."""
    c.saveState()
    c.setFillColor(color)
    c.setFillAlpha(alpha)
    import random
    rng = random.Random(13)
    for _ in range(25):
        lx = x + rng.uniform(0, w)
        ly = y + rng.uniform(0, h)
        size = rng.uniform(15, 35)
        angle = rng.uniform(0, 360)
        c.saveState()
        c.translate(lx, ly)
        c.rotate(angle)
        p = c.beginPath()
        p.moveTo(0, 0)
        p.curveTo(-size / 3, size / 2, size / 3, size / 2, 0, size)
        p.curveTo(size / 3, size / 2, -size / 3, size / 2, 0, 0)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()
    c.restoreState()


def draw_flame_pattern(c, x, y, w, h, color, alpha=0.12):
    """Draw flame shapes."""
    c.saveState()
    c.setFillColor(color)
    c.setFillAlpha(alpha)
    import random
    rng = random.Random(99)
    for _ in range(18):
        fx = x + rng.uniform(10, w - 10)
        fy = y + rng.uniform(10, h - 30)
        fw = rng.uniform(12, 25)
        fh = rng.uniform(20, 45)
        p = c.beginPath()
        p.moveTo(fx, fy)
        p.curveTo(fx - fw, fy + fh * 0.4, fx - fw * 0.3, fy + fh * 0.8, fx, fy + fh)
        p.curveTo(fx + fw * 0.3, fy + fh * 0.8, fx + fw, fy + fh * 0.4, fx, fy)
        c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def draw_geometric_pattern(c, x, y, w, h, color, alpha=0.1):
    """Draw geometric triangles pattern."""
    c.saveState()
    c.setFillColor(color)
    c.setFillAlpha(alpha)
    import random
    rng = random.Random(55)
    for _ in range(30):
        tx = x + rng.uniform(0, w)
        ty = y + rng.uniform(0, h)
        size = rng.uniform(15, 40)
        p = c.beginPath()
        p.moveTo(tx, ty)
        p.lineTo(tx + size, ty)
        p.lineTo(tx + size / 2, ty + size * 0.866)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def draw_medical_pattern(c, x, y, w, h, color, alpha=0.08):
    """Draw medical cross pattern."""
    c.saveState()
    c.setFillColor(color)
    c.setFillAlpha(alpha)
    import random
    rng = random.Random(22)
    for _ in range(15):
        cx2 = x + rng.uniform(20, w - 20)
        cy2 = y + rng.uniform(20, h - 20)
        size = rng.uniform(10, 25)
        t = size * 0.3
        c.rect(cx2 - t, cy2 - size, t * 2, size * 2, fill=1, stroke=0)
        c.rect(cx2 - size, cy2 - t, size * 2, t * 2, fill=1, stroke=0)
    c.restoreState()


def draw_legal_pattern(c, x, y, w, h, color, alpha=0.08):
    """Draw scales / column pattern."""
    c.saveState()
    c.setStrokeColor(color)
    c.setStrokeAlpha(alpha)
    c.setLineWidth(1)
    import random
    rng = random.Random(33)
    for _ in range(8):
        col_x = x + rng.uniform(10, w - 10)
        col_y = y + rng.uniform(10, h * 0.3)
        col_h = rng.uniform(60, 120)
        col_w = rng.uniform(8, 16)
        c.rect(col_x, col_y, col_w, col_h, fill=0, stroke=1)
    c.restoreState()


def draw_books_pattern(c, x, y, w, h, color, alpha=0.1):
    """Draw book spines pattern."""
    c.saveState()
    c.setFillColor(color)
    c.setFillAlpha(alpha)
    import random
    rng = random.Random(44)
    bx = x
    while bx < x + w:
        bw = rng.uniform(15, 30)
        bh = rng.uniform(50, 100)
        by = y + rng.uniform(0, h - bh)
        c.rect(bx, by, bw, bh, fill=1, stroke=0)
        bx += bw + rng.uniform(3, 8)
    c.restoreState()


def draw_kitchen_pattern(c, x, y, w, h, color, alpha=0.1):
    """Draw dots and circles for kitchen."""
    c.saveState()
    c.setStrokeColor(color)
    c.setStrokeAlpha(alpha)
    c.setLineWidth(1.5)
    import random
    rng = random.Random(66)
    for _ in range(20):
        cx2 = x + rng.uniform(10, w - 10)
        cy2 = y + rng.uniform(10, h - 10)
        r = rng.uniform(8, 25)
        c.circle(cx2, cy2, r, fill=0, stroke=1)
    c.restoreState()


PATTERN_DRAWERS = {
    "bricks": draw_brick_pattern,
    "circuit": draw_circuit_pattern,
    "music": draw_music_pattern,
    "leaves": draw_leaf_pattern,
    "flame": draw_flame_pattern,
    "geometric": draw_geometric_pattern,
    "medical": draw_medical_pattern,
    "legal": draw_legal_pattern,
    "books": draw_books_pattern,
    "kitchen": draw_kitchen_pattern,
}


def draw_big_icon(c, theme, cx, cy, size=80):
    """Draw a large decorative icon for the profession."""
    icon_color = rgb(*theme["accent"])
    c.setFillColor(icon_color)
    c.setStrokeColor(icon_color)
    name = theme["name_en"].lower()

    if "construction" in name:
        # Hard hat shape
        c.setFillAlpha(0.9)
        c.ellipse(cx - size * 0.7, cy - size * 0.1, cx + size * 0.7, cy + size * 0.5, fill=1, stroke=0)
        c.rect(cx - size * 0.8, cy - size * 0.25, size * 1.6, size * 0.2, fill=1, stroke=0)
        c.setFillColor(rgb(*theme["primary"]))
        c.rect(cx - size * 0.1, cy - size * 0.1, size * 0.2, size * 0.5, fill=1, stroke=0)

    elif "it" in name or "professional" in name:
        # Monitor shape
        c.setFillAlpha(0.9)
        c.roundRect(cx - size * 0.7, cy - size * 0.3, size * 1.4, size * 0.8, 8, fill=0, stroke=1)
        c.setLineWidth(2)
        # Code lines
        c.setFillColor(rgb(*theme["accent"]))
        c.setFillAlpha(0.7)
        for i, offset in enumerate([0.15, 0.05, -0.05, -0.15]):
            line_w = size * (0.7 - i * 0.08)
            c.rect(cx - size * 0.5, cy + offset * size, line_w, 4, fill=1, stroke=0)

    elif "doctor" in name or "medical" in name:
        # Cross
        c.setFillAlpha(0.9)
        t = size * 0.22
        c.rect(cx - t, cy - size * 0.55, t * 2, size * 1.1, fill=1, stroke=0)
        c.rect(cx - size * 0.55, cy - t, size * 1.1, t * 2, fill=1, stroke=0)

    elif "teacher" in name:
        # Open book
        c.setFillAlpha(0.9)
        p = c.beginPath()
        p.moveTo(cx, cy - size * 0.4)
        p.curveTo(cx - size * 0.7, cy - size * 0.3, cx - size * 0.7, cy + size * 0.4, cx, cy + size * 0.3)
        p.curveTo(cx + size * 0.7, cy + size * 0.4, cx + size * 0.7, cy - size * 0.3, cx, cy - size * 0.4)
        c.drawPath(p, fill=1, stroke=0)
        c.setFillColor(rgb(*theme["cover_bg"]))
        c.setFillAlpha(0.6)
        c.rect(cx - 2, cy - size * 0.35, 4, size * 0.65, fill=1, stroke=0)

    elif "chef" in name or "cook" in name:
        # Chef hat
        c.setFillAlpha(0.9)
        c.ellipse(cx - size * 0.5, cy, cx + size * 0.5, cy + size * 0.6, fill=1, stroke=0)
        c.rect(cx - size * 0.4, cy - size * 0.2, size * 0.8, size * 0.3, fill=1, stroke=0)
        c.ellipse(cx - size * 0.45, cy + size * 0.25, cx + size * 0.45, cy + size * 0.75, fill=1, stroke=0)

    elif "athlete" in name:
        # Dumbbell
        c.setFillAlpha(0.9)
        c.rect(cx - size * 0.9, cy - size * 0.35, size * 0.35, size * 0.7, fill=1, stroke=0)
        c.rect(cx + size * 0.55, cy - size * 0.35, size * 0.35, size * 0.7, fill=1, stroke=0)
        c.rect(cx - size * 0.55, cy - size * 0.12, size * 1.1, size * 0.24, fill=1, stroke=0)

    elif "lawyer" in name:
        # Scales of justice
        c.setFillAlpha(0)
        c.setStrokeAlpha(0.9)
        c.setLineWidth(3)
        c.line(cx, cy - size * 0.5, cx, cy + size * 0.5)
        c.line(cx - size * 0.6, cy + size * 0.2, cx + size * 0.6, cy + size * 0.2)
        c.line(cx - size * 0.6, cy + size * 0.2, cx - size * 0.6, cy)
        c.line(cx + size * 0.6, cy + size * 0.2, cx + size * 0.6, cy)
        c.arc(cx - size * 0.8, cy - size * 0.1, cx - size * 0.4, cy + size * 0.1)
        c.arc(cx + size * 0.4, cy - size * 0.1, cx + size * 0.8, cy + size * 0.1)

    elif "gardener" in name:
        # Leaf/sprout
        c.setFillAlpha(0.9)
        p = c.beginPath()
        p.moveTo(cx, cy - size * 0.6)
        p.curveTo(cx + size * 0.6, cy - size * 0.2, cx + size * 0.5, cy + size * 0.4, cx, cy + size * 0.5)
        p.curveTo(cx - size * 0.5, cy + size * 0.4, cx - size * 0.6, cy - size * 0.2, cx, cy - size * 0.6)
        c.drawPath(p, fill=1, stroke=0)
        c.setFillColor(rgb(*theme["cover_bg"]))
        c.setFillAlpha(0.6)
        c.rect(cx - 2, cy - size * 0.55, 4, size * 1.0, fill=1, stroke=0)

    elif "musician" in name:
        # Musical note
        c.setFillAlpha(0.9)
        c.ellipse(cx - size * 0.35, cy - size * 0.15, cx + size * 0.25, cy + size * 0.25, fill=1, stroke=0)
        c.rect(cx + size * 0.2, cy - size * 0.15, size * 0.1, size * 0.7, fill=1, stroke=0)
        c.ellipse(cx + size * 0.05, cy + size * 0.45, cx + size * 0.55, cy + size * 0.75, fill=1, stroke=0)

    elif "firefighter" in name:
        # Flame
        p = c.beginPath()
        p.moveTo(cx, cy - size * 0.6)
        p.curveTo(cx + size * 0.5, cy - size * 0.2, cx + size * 0.4, cy + size * 0.3, cx, cy + size * 0.5)
        p.curveTo(cx - size * 0.4, cy + size * 0.3, cx - size * 0.5, cy - size * 0.2, cx, cy - size * 0.6)
        c.drawPath(p, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFillAlpha(0.6)
        p2 = c.beginPath()
        p2.moveTo(cx, cy - size * 0.3)
        p2.curveTo(cx + size * 0.25, cy, cx + size * 0.2, cy + size * 0.25, cx, cy + size * 0.3)
        p2.curveTo(cx - size * 0.2, cy + size * 0.25, cx - size * 0.25, cy, cx, cy - size * 0.3)
        c.drawPath(p2, fill=1, stroke=0)


def generate_cover(theme_key, theme, output_path):
    """
    Generate full KDP cover PDF (front + spine + back).
    Returns: output_path
    """
    specs = KDP_SPECS
    # KDP cover dimensions
    trim_w = specs["trim_width"] * inch
    trim_h = specs["trim_height"] * inch
    bleed = specs["bleed"] * inch

    # Spine width calculation: pages / 444 inches for 60lb cream paper
    total_pages = specs["total_pages"]
    spine_w = (total_pages / 444.0) * inch

    # Full cover width: back + spine + front (all with bleeds)
    cover_w = bleed + trim_w + spine_w + trim_w + bleed
    cover_h = trim_h + 2 * bleed

    c = canvas.Canvas(output_path, pagesize=(cover_w, cover_h))

    primary = rgb(*theme["primary"])
    secondary = rgb(*theme["secondary"])
    accent = rgb(*theme["accent"])
    cover_bg = rgb(*theme["cover_bg"])
    text_dark = rgb(*theme["text_dark"])

    # === BACK COVER ===
    back_x = 0
    back_w = bleed + trim_w

    # Background gradient simulation with rectangles
    c.setFillColor(cover_bg)
    c.rect(back_x, 0, back_w, cover_h, fill=1, stroke=0)

    # Pattern on back
    pattern_fn = PATTERN_DRAWERS.get(theme.get("pattern", "bricks"), draw_brick_pattern)
    pattern_fn(c, back_x, 0, back_w, cover_h, primary, alpha=0.15)

    # Back cover: decorative horizontal band
    c.setFillColor(primary)
    c.setFillAlpha(0.25)
    c.rect(back_x, cover_h * 0.15, back_w, cover_h * 0.7, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Back cover text
    c.setFillColor(white)

    # ISBN barcode placeholder area
    barcode_w = 1.5 * inch
    barcode_h = 1.0 * inch
    bx = back_x + bleed + (trim_w - barcode_w) / 2
    by = 0.3 * inch
    c.setFillColor(white)
    c.rect(bx, by, barcode_w, barcode_h, fill=1, stroke=0)
    c.setFillColor(text_dark)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(bx + barcode_w / 2, by + barcode_h / 2 - 4, "ISBN")

    # Back cover tagline
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(back_x + back_w / 2, cover_h * 0.75, theme["tagline"])

    c.setFont("Helvetica", 11)
    c.setFillColor(rgb(*theme["accent"]))
    c.drawCentredString(back_x + back_w / 2, cover_h * 0.68, theme["subtitle"])

    # Back cover description
    c.setFillColor(white)
    c.setFont("Helvetica", 9)
    desc_lines = [
        f"• 120 stron wysokiej jakości",
        f"• 5 stron tematycznych dla {theme['name_pl']}",
        f"• 115 stron w linie do notatek",
        f"• Format: 6\" × 9\" (15.24 × 22.86 cm)",
        f"• Idealne na prezent dla {theme['name_pl']}a",
    ]
    for i, line in enumerate(desc_lines):
        c.drawString(back_x + bleed + 0.3 * inch, cover_h * 0.56 - i * 14, line)

    # Decorative icon on back
    draw_big_icon(c, theme, back_x + back_w / 2, cover_h * 0.45, size=35)

    # === SPINE ===
    spine_x = bleed + trim_w
    c.setFillColor(primary)
    c.setFillAlpha(1)
    c.rect(spine_x, 0, spine_w, cover_h, fill=1, stroke=0)

    # Spine text (rotated)
    c.saveState()
    c.translate(spine_x + spine_w / 2, cover_h / 2)
    c.rotate(90)
    c.setFillColor(white)
    spine_font_size = min(9, spine_w * 0.6)
    c.setFont("Helvetica-Bold", spine_font_size)
    c.drawCentredString(0, -3, theme["tagline"])
    c.restoreState()

    # === FRONT COVER ===
    front_x = bleed + trim_w + spine_w
    front_w = trim_w + bleed

    # Dark background
    c.setFillColor(cover_bg)
    c.setFillAlpha(1)
    c.rect(front_x, 0, front_w, cover_h, fill=1, stroke=0)

    # Top color band
    band_h = cover_h * 0.45
    c.setFillColor(primary)
    c.setFillAlpha(0.9)
    c.rect(front_x, cover_h - band_h, front_w, band_h, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Pattern on color band
    pattern_fn(c, front_x, cover_h - band_h, front_w, band_h, cover_bg, alpha=0.18)

    # Diagonal accent line
    c.setFillColor(accent)
    c.setFillAlpha(0.9)
    band_bottom_y = cover_h - band_h
    p = c.beginPath()
    p.moveTo(front_x, band_bottom_y)
    p.lineTo(front_x + front_w, band_bottom_y + 0.4 * inch)
    p.lineTo(front_x + front_w, band_bottom_y - 0.15 * inch)
    p.lineTo(front_x, band_bottom_y - 0.55 * inch)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Main icon in color band
    icon_cx = front_x + front_w * 0.65
    icon_cy = cover_h - band_h * 0.45
    draw_big_icon(c, theme, icon_cx, icon_cy, size=60)

    # Title text
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    # Split tagline into max 2 lines
    tagline = theme["tagline"]
    words = tagline.split()
    mid = len(words) // 2
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])
    title_y = cover_h - band_h * 0.72
    c.drawString(front_x + bleed + 0.2 * inch, title_y + 18, line1)
    c.drawString(front_x + bleed + 0.2 * inch, title_y - 10, line2)

    # Subtitle
    c.setFillColor(accent)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(front_x + bleed + 0.2 * inch, title_y - 28, theme["subtitle"])

    # Bottom section (dark background) – features list
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    features = [
        f"Zawiera strony tematyczne dla zawodu:",
        f"{theme['name_pl']} {theme['emoji']}",
        f"120 stron • Format 6×9\"",
    ]
    fy = band_bottom_y - 0.6 * inch
    for feat in features:
        c.setFillColor(white)
        c.setFont("Helvetica-Bold" if feat.startswith("Zawiera") or feat.startswith("120") else "Helvetica", 10)
        if theme['name_pl'] in feat:
            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 13)
        c.drawString(front_x + bleed + 0.25 * inch, fy, feat)
        fy -= 16

    # Decorative bottom bar
    c.setFillColor(primary)
    c.setFillAlpha(0.8)
    c.rect(front_x, bleed, front_w, 0.3 * inch, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Website/brand placeholder
    c.setFillColor(white)
    c.setFont("Helvetica", 8)
    c.drawCentredString(front_x + front_w / 2, bleed + 0.1 * inch, "Notatniki Zawodowe • Quality Notebooks")

    # Separator line between back and front visible on spine
    c.setStrokeColor(rgb(*theme["accent"]))
    c.setStrokeAlpha(0.5)
    c.setLineWidth(0.5)
    c.line(spine_x, 0, spine_x, cover_h)
    c.line(spine_x + spine_w, 0, spine_x + spine_w, cover_h)

    c.save()
    return output_path
