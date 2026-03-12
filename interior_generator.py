"""
KDP Notebook Interior Generator.
Generates:
  - Thematic pages (profession-specific forms, checklists, trackers)
  - Lined notebook pages (with subtle header/footer branding)
"""

from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white, black
from reportlab.lib.utils import ImageReader
from themes import KDP_SPECS


def rgb(r, g, b):
    return Color(r / 255, g / 255, b / 255)


# --- Page constants ---
def page_size():
    s = KDP_SPECS
    return s["trim_width"] * inch, s["trim_height"] * inch


def margins():
    s = KDP_SPECS
    return {
        "inner": s["margin_inner"] * inch,
        "outer": s["margin_outer"] * inch,
        "top": s["margin_top"] * inch,
        "bottom": s["margin_bottom"] * inch,
    }


def draw_header(c, theme, page_w, page_h, m, page_num=None, is_left=False):
    """Subtle header with profession name and decorative line."""
    primary = rgb(*theme["primary"])
    accent = rgb(*theme["accent"])

    header_y = page_h - m["top"] + 4
    c.setStrokeColor(primary)
    c.setStrokeAlpha(0.4)
    c.setLineWidth(0.5)
    c.line(m["inner"], header_y - 2, page_w - m["outer"], header_y - 2)

    c.setFillColor(primary)
    c.setFillAlpha(0.7)
    c.setFont("Helvetica", 7)
    text = f"{theme['tagline']}  {theme['emoji']}"
    if is_left:
        c.drawString(m["inner"], header_y, text)
    else:
        c.drawRightString(page_w - m["outer"], header_y, text)

    if page_num is not None:
        c.setFont("Helvetica", 7)
        c.setFillColor(rgb(*theme["secondary"]) if theme["secondary"] != (255, 255, 255) else rgb(100, 100, 100))
        if is_left:
            c.drawRightString(page_w - m["outer"], header_y, str(page_num))
        else:
            c.drawString(m["inner"], header_y, str(page_num))

    c.setFillAlpha(1)
    c.setStrokeAlpha(1)


def draw_footer(c, theme, page_w, page_h, m):
    """Subtle footer."""
    primary = rgb(*theme["primary"])
    footer_y = m["bottom"] - 6
    c.setStrokeColor(primary)
    c.setStrokeAlpha(0.3)
    c.setLineWidth(0.4)
    c.line(m["inner"], footer_y + 8, page_w - m["outer"], footer_y + 8)
    c.setFillAlpha(1)
    c.setStrokeAlpha(1)


def draw_field_line(c, label, x, y, line_width, label_font="Helvetica-Bold", label_size=9, line_color=None):
    """Draw a labeled form field with underline."""
    if line_color is None:
        line_color = Color(0.6, 0.6, 0.6)
    c.setFont(label_font, label_size)
    c.setFillColor(black)
    c.drawString(x, y, label)
    label_w = c.stringWidth(label, label_font, label_size)
    c.setStrokeColor(line_color)
    c.setLineWidth(0.5)
    c.line(x + label_w + 4, y - 2, x + label_w + 4 + line_width, y - 2)


def draw_checkbox(c, x, y, size=8):
    """Draw a small checkbox."""
    c.setStrokeColor(Color(0.4, 0.4, 0.4))
    c.setLineWidth(0.6)
    c.rect(x, y - size * 0.15, size, size, fill=0, stroke=1)


def draw_thematic_page(c, theme, page_config, page_w, page_h, m, page_num):
    """Draw a single thematic page based on page_config type."""
    primary = rgb(*theme["primary"])
    accent = rgb(*theme["accent"])
    text_dark = rgb(*theme["text_dark"])
    cover_bg = rgb(*theme["cover_bg"])

    # Header band
    band_h = 0.75 * inch
    c.setFillColor(primary)
    c.setFillAlpha(1)
    c.rect(0, page_h - band_h, page_w, band_h, fill=1, stroke=0)

    # Accent diagonal
    c.setFillColor(accent)
    c.setFillAlpha(0.8)
    p = c.beginPath()
    p.moveTo(0, page_h - band_h)
    p.lineTo(page_w * 0.55, page_h - band_h)
    p.lineTo(page_w * 0.5, page_h - band_h - 0.12 * inch)
    p.lineTo(0, page_h - band_h - 0.12 * inch)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Page title
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(m["inner"] + 4, page_h - band_h + 0.28 * inch, page_config["title"])

    # Profession name tag
    c.setFont("Helvetica", 8)
    c.setFillColor(accent)
    c.drawRightString(page_w - m["outer"], page_h - band_h + 0.28 * inch,
                      f"{theme['emoji']}  {theme['name_pl']}")

    # Content area
    content_top = page_h - band_h - 0.25 * inch
    content_left = m["inner"] + 4
    content_right = page_w - m["outer"] - 4
    content_w = content_right - content_left
    line_color = Color(0.75, 0.75, 0.75)

    ptype = page_config.get("type", "fields")

    if ptype == "fields" or ptype not in ("sprint", "schedule", "weekly_menu", "shopping",
                                           "grade_table", "workout", "measurements",
                                           "deadline_tracker", "setlist", "planting_calendar",
                                           "staff_lines", "garden_plan", "shift", "reference",
                                           "diagram_space", "ideas"):
        # Standard form fields
        y = content_top
        fields = page_config.get("fields", [])
        checks = page_config.get("checks", [])

        if checks:
            # Checkbox list
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, "Lista kontrolna:")
            y -= 0.2 * inch
            for i, item in enumerate(checks):
                draw_checkbox(c, content_left, y, size=9)
                c.setFont("Helvetica", 9)
                c.setFillColor(black)
                c.drawString(content_left + 14, y, item)
                y -= 0.22 * inch
                if y < m["bottom"] + 0.1 * inch:
                    break
        else:
            line_h = 0.32 * inch
            for field in fields:
                if y < m["bottom"] + 0.1 * inch:
                    break
                if not field:
                    y -= 0.15 * inch
                    continue
                if field.endswith(":"):
                    # Label above line
                    c.setFont("Helvetica-Bold", 9)
                    c.setFillColor(text_dark)
                    c.drawString(content_left, y, field)
                    y -= 6
                    c.setStrokeColor(line_color)
                    c.setLineWidth(0.5)
                    c.line(content_left, y, content_right, y)
                    y -= line_h - 6
                else:
                    # Just a line (for □ checkboxes etc)
                    c.setFont("Helvetica", 8)
                    c.setFillColor(rgb(100, 100, 100))
                    c.drawString(content_left, y, field)
                    y -= 0.2 * inch

    elif ptype == "sprint":
        y = content_top
        fields = page_config.get("fields", [])
        for field in fields[:5]:
            if y < m["bottom"] + 0.3 * inch:
                break
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, field)
            y -= 6
            c.setStrokeColor(line_color)
            c.setLineWidth(0.5)
            c.line(content_left, y, content_right, y)
            y -= 0.3 * inch
        # Task rows
        n_tasks = page_config.get("tasks", 8)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(text_dark)
        c.drawString(content_left, y, "Zadania (Story | SP | Status | Opis):")
        y -= 0.18 * inch
        for i in range(n_tasks):
            if y < m["bottom"] + 0.15 * inch:
                break
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            c.line(content_left, y, content_right, y)
            # Column dividers
            col_sp = content_left + content_w * 0.45
            col_st = content_left + content_w * 0.6
            col_desc = content_left + content_w * 0.75
            c.line(col_sp, y - 0.18 * inch, col_sp, y)
            c.line(col_st, y - 0.18 * inch, col_st, y)
            c.line(col_desc, y - 0.18 * inch, col_desc, y)
            y -= 0.22 * inch

    elif ptype == "schedule":
        y = content_top
        slots = page_config.get("slots", [])
        for slot in slots:
            if y < m["bottom"] + 0.1 * inch:
                break
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, slot)
            y -= 6
            c.setStrokeColor(line_color)
            c.setLineWidth(0.5)
            c.line(content_left + 90, y, content_right, y)
            y -= 0.3 * inch

    elif ptype == "weekly_menu":
        y = content_top
        days = page_config.get("days", [])
        meals = page_config.get("meals", [])
        row_h = (content_top - m["bottom"] - 0.1 * inch) / (len(days) + 1)
        col_w = content_w / (len(meals) + 1)
        # Header row
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(primary)
        for j, meal in enumerate(meals):
            c.drawCentredString(content_left + col_w * (j + 1) + col_w / 2, y, meal)
        y -= row_h
        for i, day in enumerate(days):
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(text_dark)
            c.drawString(content_left + 2, y, day)
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            c.line(content_left, y - 2, content_right, y - 2)
            for j in range(len(meals) + 1):
                c.line(content_left + col_w * j, y + row_h * 0.7, content_left + col_w * j, y - 2)
            y -= row_h

    elif ptype == "shopping":
        y = content_top
        categories = page_config.get("categories", [])
        for cat in categories:
            if y < m["bottom"] + 0.3 * inch:
                break
            c.setFillColor(primary)
            c.setFillAlpha(0.15)
            c.rect(content_left - 2, y - 2, content_w + 4, 14, fill=1, stroke=0)
            c.setFillAlpha(1)
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(primary)
            c.drawString(content_left, y, cat)
            y -= 0.2 * inch
            for _ in range(4):
                if y < m["bottom"] + 0.1 * inch:
                    break
                c.setStrokeColor(line_color)
                c.setLineWidth(0.4)
                c.line(content_left, y, content_right, y)
                draw_checkbox(c, content_left - 12, y, size=8)
                y -= 0.22 * inch
            y -= 0.05 * inch

    elif ptype == "grade_table":
        y = content_top
        c.setFont("Helvetica", 8)
        c.setFillColor(rgb(100, 100, 100))
        c.drawString(content_left, y, "Imię i Nazwisko | Ocena 1 | Ocena 2 | Ocena 3 | Śr.")
        y -= 0.15 * inch
        col_name = content_w * 0.45
        n_cols = 4
        col_w_score = (content_w - col_name) / n_cols
        row_h = 0.26 * inch
        num_rows = int((y - m["bottom"] - 0.1 * inch) / row_h)
        for i in range(num_rows):
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            c.line(content_left, y, content_right, y)
            c.line(content_left + col_name, y, content_left + col_name, y - row_h + 4)
            for j in range(1, n_cols):
                lx = content_left + col_name + col_w_score * j
                c.line(lx, y, lx, y - row_h + 4)
            y -= row_h

    elif ptype == "workout":
        y = content_top
        fields = page_config.get("fields", [])
        for field in fields:
            if y < m["bottom"] + 0.5 * inch:
                break
            if not field:
                y -= 0.12 * inch
                continue
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, field)
            y -= 6
            c.setStrokeColor(line_color)
            c.setLineWidth(0.5)
            c.line(content_left, y, content_right, y)
            y -= 0.27 * inch
        # Exercise table
        n_rows = page_config.get("exercise_rows", 8)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(primary)
        headers = ["Ćwiczenie", "Serie", "Powt.", "Ciężar (kg)", "Przerwa", "Uwagi"]
        col_widths = [content_w * 0.28, content_w * 0.1, content_w * 0.1,
                      content_w * 0.18, content_w * 0.12, content_w * 0.22]
        cx = content_left
        for h, cw in zip(headers, col_widths):
            c.drawString(cx + 2, y, h)
            cx += cw
        y -= 0.18 * inch
        for _ in range(n_rows):
            if y < m["bottom"] + 0.1 * inch:
                break
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            c.line(content_left, y, content_right, y)
            cx = content_left
            for cw in col_widths[:-1]:
                c.line(cx + cw, y, cx + cw, y - 0.22 * inch)
                cx += cw
            y -= 0.24 * inch

    elif ptype == "measurements":
        y = content_top
        fields = page_config.get("fields", [])
        row_h = 0.28 * inch
        for field in fields:
            if y < m["bottom"] + 0.1 * inch:
                break
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, field)
            c.setStrokeColor(line_color)
            c.setLineWidth(0.5)
            label_w = c.stringWidth(field, "Helvetica-Bold", 9)
            c.line(content_left + label_w + 4, y - 2, content_right, y - 2)
            y -= row_h

    elif ptype == "deadline_tracker":
        y = content_top
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(primary)
        headers = ["Sprawa", "Czynność", "Termin", "Status", "Uwagi"]
        col_widths = [content_w * 0.22, content_w * 0.28, content_w * 0.18,
                      content_w * 0.12, content_w * 0.20]
        cx = content_left
        for h, cw in zip(headers, col_widths):
            c.drawString(cx + 2, y, h)
            cx += cw
        y -= 0.16 * inch
        rows = page_config.get("rows", 10)
        row_h = 0.28 * inch
        for _ in range(rows):
            if y < m["bottom"] + 0.1 * inch:
                break
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            c.line(content_left, y, content_right, y)
            cx = content_left
            for cw in col_widths[:-1]:
                c.line(cx + cw, y, cx + cw, y - row_h + 4)
                cx += cw
            y -= row_h

    elif ptype == "setlist":
        y = content_top
        fields = page_config.get("fields", [])
        for field in fields:
            if y < m["bottom"] + 0.6 * inch:
                break
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, field)
            y -= 6
            c.setStrokeColor(line_color)
            c.setLineWidth(0.5)
            c.line(content_left, y, content_right, y)
            y -= 0.27 * inch
        rows = page_config.get("rows", 15)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(primary)
        c.drawString(content_left, y, "#  Tytuł / Utwór")
        c.drawRightString(content_right, y, "Tonacja  Czas")
        y -= 0.15 * inch
        for i in range(1, rows + 1):
            if y < m["bottom"] + 0.1 * inch:
                break
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(rgb(180, 180, 180))
            c.drawString(content_left, y, str(i))
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            c.line(content_left + 15, y, content_right - 80, y)
            c.line(content_right - 75, y, content_right - 40, y)
            c.line(content_right - 35, y, content_right, y)
            y -= 0.26 * inch

    elif ptype == "planting_calendar":
        y = content_top
        months = page_config.get("months", [])
        plants = ["Pomidor", "Ogórek", "Marchew", "Pietruszka", "Sałata",
                  "Kapusta", "Cebula", "Buraki", "Papryka", "Ziemniaki",
                  "Fasola", "Groch", "Szpinak", "Rzodkiewka", "Dynia"]
        col_w_label = content_w * 0.3
        col_w_month = (content_w - col_w_label) / len(months)
        # Header
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(primary)
        cx = content_left + col_w_label
        for m_name in months:
            c.drawCentredString(cx + col_w_month / 2, y, m_name)
            cx += col_w_month
        y -= 0.18 * inch
        avail_h = y - m["bottom"] - 0.1 * inch
        row_h = avail_h / min(len(plants), 15)
        for plant in plants:
            if y < m["bottom"] + 0.1 * inch:
                break
            c.setFont("Helvetica", 8)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, plant)
            c.setStrokeColor(line_color)
            c.setLineWidth(0.3)
            cx = content_left + col_w_label
            for _ in months:
                c.rect(cx, y - row_h + 3, col_w_month - 1, row_h - 3, fill=0, stroke=1)
                cx += col_w_month
            y -= row_h

    elif ptype == "staff_lines":
        y = content_top
        desc = page_config.get("description", "")
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(rgb(150, 150, 150))
        c.drawString(content_left, y, desc)
        y -= 0.3 * inch
        staves = page_config.get("staves", 6)
        stave_h = (y - m["bottom"] - 0.2 * inch) / staves
        for s in range(staves):
            sy = y - s * stave_h
            # 5 staff lines
            for line_i in range(5):
                ly = sy - line_i * 5
                c.setStrokeColor(Color(0.3, 0.3, 0.3))
                c.setLineWidth(0.5)
                c.line(content_left, ly, content_right, ly)
            # Tab lines below staff
            tab_y = sy - 30
            for t in range(6):
                c.setStrokeColor(Color(0.5, 0.5, 0.5))
                c.setLineWidth(0.4)
                c.line(content_left, tab_y - t * 6, content_right, tab_y - t * 6)

    elif ptype == "garden_plan":
        y = content_top
        labels = page_config.get("labels", [])
        desc = page_config.get("description", "")
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(rgb(150, 150, 150))
        c.drawString(content_left, y, desc)
        y -= 0.2 * inch
        # Grid for garden plan
        grid_h = y - m["bottom"] - 1.2 * inch
        grid_w = content_w
        c.setStrokeColor(Color(0.8, 0.8, 0.8))
        c.setLineWidth(0.3)
        step = 0.25 * inch
        gx = content_left
        while gx <= content_left + grid_w:
            c.line(gx, m["bottom"] + 1.2 * inch, gx, m["bottom"] + 1.2 * inch + grid_h)
            gx += step
        gy = m["bottom"] + 1.2 * inch
        while gy <= m["bottom"] + 1.2 * inch + grid_h:
            c.line(content_left, gy, content_left + grid_w, gy)
            gy += step
        # Labels below
        ly = m["bottom"] + 1.0 * inch
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(text_dark)
        for label in labels:
            if ly < m["bottom"] + 0.05 * inch:
                break
            c.drawString(content_left, ly, label)
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            lw = c.stringWidth(label, "Helvetica-Bold", 8)
            c.line(content_left + lw + 4, ly - 2, content_right, ly - 2)
            ly -= 0.18 * inch

    elif ptype == "shift":
        y = content_top
        fields = page_config.get("fields", [])
        for field in fields:
            if y < m["bottom"] + 0.1 * inch:
                break
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, field)
            y -= 6
            c.setStrokeColor(line_color)
            c.setLineWidth(0.5)
            c.line(content_left, y, content_right, y)
            y -= 0.35 * inch

    elif ptype == "reference":
        y = content_top
        content_list = page_config.get("content", [])
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(primary)
        for line in content_list:
            if y < m["bottom"] + 0.1 * inch:
                break
            if not line:
                y -= 0.1 * inch
                continue
            if line.isupper():
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(primary)
                c.setFillAlpha(0.15)
                c.rect(content_left - 2, y - 2, content_w + 4, 13, fill=1, stroke=0)
                c.setFillAlpha(1)
                c.setFillColor(primary)
            else:
                c.setFont("Helvetica", 8)
                c.setFillColor(text_dark)
            c.drawString(content_left, y, line)
            y -= 0.2 * inch

    elif ptype == "diagram_space":
        y = content_top
        desc = page_config.get("description", "")
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(rgb(150, 150, 150))
        c.drawString(content_left, y, desc)
        y -= 0.25 * inch
        # Large blank area for diagram
        diagram_h = (y - m["bottom"] - 1.2 * inch)
        c.setStrokeColor(Color(0.85, 0.85, 0.85))
        c.setLineWidth(0.4)
        c.setDash([3, 3])
        c.rect(content_left, m["bottom"] + 1.2 * inch, content_w, diagram_h, fill=0, stroke=1)
        c.setDash([])
        # Dot grid
        c.setFillColor(Color(0.8, 0.8, 0.8))
        dot_step = 0.2 * inch
        dx = content_left + dot_step
        while dx < content_left + content_w:
            dy = m["bottom"] + 1.2 * inch + dot_step
            while dy < m["bottom"] + 1.2 * inch + diagram_h:
                c.circle(dx, dy, 1, fill=1, stroke=0)
                dy += dot_step
            dx += dot_step
        # Labels below
        ly = m["bottom"] + 1.0 * inch
        labels = page_config.get("labels", [])
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(text_dark)
        for label in labels:
            if ly < m["bottom"] + 0.05 * inch:
                break
            c.drawString(content_left, ly, label)
            lw = c.stringWidth(label, "Helvetica-Bold", 8)
            c.setStrokeColor(line_color)
            c.setLineWidth(0.4)
            c.line(content_left + lw + 4, ly - 2, content_right, ly - 2)
            ly -= 0.18 * inch

    elif ptype == "ideas":
        y = content_top
        fields = page_config.get("fields", [])
        # Idea icon
        c.setFillColor(accent)
        c.setFillAlpha(0.2)
        c.circle(content_left + content_w - 0.4 * inch, content_top - 0.3 * inch, 0.35 * inch, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setFillColor(accent)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(content_left + content_w - 0.4 * inch, content_top - 0.38 * inch, "!")
        for field in fields:
            if y < m["bottom"] + 0.1 * inch:
                break
            if not field:
                y -= 0.12 * inch
                continue
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(text_dark)
            c.drawString(content_left, y, field)
            y -= 6
            c.setStrokeColor(line_color)
            c.setLineWidth(0.5)
            c.line(content_left, y, content_right, y)
            y -= 0.28 * inch

    # Footer
    draw_footer(c, theme, page_w, page_h, m)


def draw_lined_page(c, theme, page_w, page_h, m, page_num, is_left=False):
    """Draw a standard lined notebook page."""
    primary = rgb(*theme["primary"])
    accent = rgb(*theme["accent"])

    # Subtle top decoration
    c.setFillColor(primary)
    c.setFillAlpha(0.08)
    c.rect(0, page_h - 0.15 * inch, page_w, 0.15 * inch, fill=1, stroke=0)
    c.setFillAlpha(1)

    draw_header(c, theme, page_w, page_h, m, page_num, is_left)

    # Left margin red line (classic notebook style)
    margin_line_x = m["inner"] - 0.1 * inch if not is_left else m["outer"] - 0.1 * inch
    # Use inner margin as the margin line
    ml_x = m["inner"] - 0.05 * inch
    c.setStrokeColor(rgb(*theme["accent"]))
    c.setStrokeAlpha(0.25)
    c.setLineWidth(0.6)
    c.line(ml_x, m["bottom"], ml_x, page_h - m["top"] - 8)
    c.setStrokeAlpha(1)

    # Horizontal lines
    line_spacing = KDP_SPECS["line_spacing"] * inch
    line_color = Color(0.75, 0.75, 0.85)
    c.setStrokeColor(line_color)
    c.setLineWidth(0.4)

    y = page_h - m["top"] - 0.15 * inch
    while y > m["bottom"] + 0.1 * inch:
        c.line(m["inner"], y, page_w - m["outer"], y)
        y -= line_spacing

    draw_footer(c, theme, page_w, page_h, m)


def generate_interior(theme_key, theme, output_path):
    """
    Generate the full interior PDF for a notebook.
    Returns: output_path
    """
    page_w, page_h = page_size()
    m = margins()

    c = canvas.Canvas(output_path, pagesize=(page_w, page_h))

    total_pages = KDP_SPECS["total_pages"]
    thematic = theme.get("thematic_pages", [])

    # Page 1: Title page
    draw_title_page(c, theme, page_w, page_h, m)
    c.showPage()

    # Page 2: Table of contents / usage guide
    draw_contents_page(c, theme, page_w, page_h, m)
    c.showPage()

    pages_used = 2

    # Thematic pages (5 pages)
    for i, page_config in enumerate(thematic[:5]):
        draw_thematic_page(c, theme, page_config, page_w, page_h, m, page_num=pages_used + 1)
        c.showPage()
        pages_used += 1

    # Fill remaining with lined pages
    lined_count = total_pages - pages_used
    for i in range(lined_count):
        page_num = pages_used + i + 1
        is_left = (page_num % 2 == 0)
        draw_lined_page(c, theme, page_w, page_h, m, page_num, is_left)
        c.showPage()

    c.save()
    return output_path


def draw_title_page(c, theme, page_w, page_h, m):
    """Draw the interior title page."""
    primary = rgb(*theme["primary"])
    accent = rgb(*theme["accent"])
    cover_bg = rgb(*theme["cover_bg"])
    text_dark = rgb(*theme["text_dark"])

    # Top color block
    c.setFillColor(primary)
    c.rect(0, page_h * 0.65, page_w, page_h * 0.35, fill=1, stroke=0)

    # Accent diagonal
    c.setFillColor(accent)
    c.setFillAlpha(0.8)
    p = c.beginPath()
    p.moveTo(0, page_h * 0.65)
    p.lineTo(page_w, page_h * 0.65 + 0.3 * inch)
    p.lineTo(page_w, page_h * 0.65 - 0.1 * inch)
    p.lineTo(0, page_h * 0.65 - 0.1 * inch)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillAlpha(1)

    # Main title
    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_w / 2, page_h * 0.82, theme["tagline"])

    c.setFont("Helvetica-Oblique", 13)
    c.setFillColor(accent)
    c.drawCentredString(page_w / 2, page_h * 0.76, theme["subtitle"])

    c.setFont("Helvetica", 11)
    c.setFillColor(rgb(200, 200, 200))
    c.drawCentredString(page_w / 2, page_h * 0.71, theme["emoji"] + "  " + theme["name_pl"])

    # Owner section
    c.setFillColor(text_dark)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(m["inner"] + 0.2 * inch, page_h * 0.57, "Ten notatnik należy do:")
    c.setStrokeColor(primary)
    c.setLineWidth(0.6)
    c.line(m["inner"] + 0.2 * inch, page_h * 0.52, page_w - m["outer"] - 0.2 * inch, page_h * 0.52)

    c.drawString(m["inner"] + 0.2 * inch, page_h * 0.46, "Kontakt:")
    c.line(m["inner"] + 0.2 * inch, page_h * 0.41, page_w - m["outer"] - 0.2 * inch, page_h * 0.41)

    c.drawString(m["inner"] + 0.2 * inch, page_h * 0.35, "Data rozpoczęcia:")
    c.line(m["inner"] + 0.2 * inch, page_h * 0.30, page_w / 2 - 0.1 * inch, page_h * 0.30)

    c.drawString(page_w / 2 + 0.2 * inch, page_h * 0.35, "Notatnik #:")
    c.line(page_w / 2 + 0.2 * inch, page_h * 0.30, page_w - m["outer"] - 0.2 * inch, page_h * 0.30)

    # Bottom
    c.setFillColor(cover_bg)
    c.rect(0, 0, page_w, m["bottom"] + 0.15 * inch, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w / 2, m["bottom"] * 0.4, "Notatniki Zawodowe • 120 stron • Format 6×9\"")


def draw_contents_page(c, theme, page_w, page_h, m):
    """Draw a usage guide / contents page."""
    primary = rgb(*theme["primary"])
    accent = rgb(*theme["accent"])
    text_dark = rgb(*theme["text_dark"])

    draw_header(c, theme, page_w, page_h, m, page_num=2)

    y = page_h - m["top"] - 0.35 * inch
    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(m["inner"], y, "Zawartość Notatnika")
    y -= 0.1 * inch
    c.setStrokeColor(accent)
    c.setLineWidth(2)
    c.line(m["inner"], y, m["inner"] + 2.5 * inch, y)
    y -= 0.35 * inch

    thematic = theme.get("thematic_pages", [])
    entries = [
        ("1", "Strona tytułowa", 1),
        ("2", "Zawartość notatnika (ta strona)", 2),
    ]
    for i, pg in enumerate(thematic[:5]):
        entries.append((str(i + 3), pg["title"], i + 3))

    entries.append(("8–120", "Strony w linie do notatek", 8))

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(primary)
    c.drawString(m["inner"], y, "Nr")
    c.drawString(m["inner"] + 0.5 * inch, y, "Zawartość")
    c.drawRightString(page_w - m["outer"], y, "Strona")
    y -= 0.08 * inch
    c.setStrokeColor(primary)
    c.setLineWidth(0.8)
    c.line(m["inner"], y, page_w - m["outer"], y)
    y -= 0.25 * inch

    for num, title, pg_num in entries:
        if y < m["bottom"] + 0.3 * inch:
            break
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(primary)
        c.drawString(m["inner"], y, num)
        c.setFont("Helvetica", 9)
        c.setFillColor(text_dark)
        c.drawString(m["inner"] + 0.5 * inch, y, title)
        c.setFont("Helvetica", 9)
        c.drawRightString(page_w - m["outer"], y, str(pg_num))
        c.setStrokeColor(Color(0.85, 0.85, 0.85))
        c.setLineWidth(0.3)
        c.setDash([2, 3])
        c.line(m["inner"] + 0.5 * inch + c.stringWidth(title, "Helvetica", 9) + 5,
               y - 2, page_w - m["outer"] - 20, y - 2)
        c.setDash([])
        y -= 0.28 * inch

    # Usage tips
    y -= 0.2 * inch
    c.setFillColor(primary)
    c.setFillAlpha(0.1)
    c.roundRect(m["inner"], y - 1.4 * inch, page_w - m["inner"] - m["outer"], 1.6 * inch, 6, fill=1, stroke=0)
    c.setFillAlpha(1)

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(primary)
    c.drawString(m["inner"] + 0.15 * inch, y + 0.12 * inch, f"Wskazówki dla {theme['name_pl']}a:")
    y -= 0.1 * inch

    tips = [
        "Korzystaj z tematycznych stron na początku do strukturyzowania pracy.",
        "Strony w linie służą do swobodnych notatek, szkiców i planowania.",
        "Numeruj strony i dodawaj daty dla łatwego wyszukiwania informacji.",
    ]
    for tip in tips:
        c.setFont("Helvetica", 8)
        c.setFillColor(text_dark)
        c.drawString(m["inner"] + 0.15 * inch, y, f"• {tip}")
        y -= 0.22 * inch

    draw_footer(c, theme, page_w, page_h, m)
