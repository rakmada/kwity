#!/usr/bin/env python3
"""
KDP Notebook Generator — Main Orchestrator
==========================================
Generates 10 profession-specific notebooks for Amazon KDP, each containing:
  - Full KDP cover PDF (front + spine + back)
  - Interior PDF (5 thematic pages + 115 lined pages = 120 total)
  - Product mockup (PNG + PDF)

Output structure:
  output/
    01_budowlaniec/
      cover_budowlaniec.pdf       ← KDP ready cover
      interior_budowlaniec.pdf    ← KDP ready interior
      mockup_budowlaniec.png      ← Product presentation image
      mockup_budowlaniec.pdf      ← Mockup as PDF
    02_informatyk/
      ...
    ...

Usage:
  python generator.py              # Generate all 10 notebooks
  python generator.py --theme lekarz  # Generate specific notebook
  python generator.py --list       # List available themes
"""

import os
import sys
import time
import argparse
import traceback

from themes import THEMES, PROFESSION_ORDER
from cover_generator import generate_cover
from interior_generator import generate_interior
from mockup_generator import generate_mockup, generate_mockup_pdf


# ─── Output directory ────────────────────────────────────────────────────────

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


# ─── Progress display ─────────────────────────────────────────────────────────

def print_header():
    print()
    print("=" * 65)
    print("   KDP NOTEBOOK GENERATOR — Notatniki Zawodowe")
    print("=" * 65)
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Notebooks: {len(PROFESSION_ORDER)}")
    print("=" * 65)
    print()


def print_step(step, total, name, description):
    bar_w = 20
    filled = int(bar_w * step / total)
    bar = "█" * filled + "░" * (bar_w - filled)
    print(f"  [{bar}] {step}/{total}  {name}")
    print(f"        → {description}")


def print_done(theme_key, elapsed, files):
    print(f"        ✓ Done in {elapsed:.1f}s")
    for f in files:
        size = os.path.getsize(f) / 1024
        print(f"          {os.path.basename(f)} ({size:.0f} KB)")
    print()


def print_error(theme_key, error):
    print(f"        ✗ ERROR: {error}")
    print()


# ─── Single notebook generation ───────────────────────────────────────────────

def generate_notebook(theme_key, theme, notebook_dir, step, total):
    """Generate all files for a single profession notebook."""
    ensure_dir(notebook_dir)
    files_generated = []
    t0 = time.time()

    # 1. Cover PDF
    print_step(step, total, theme["name_pl"], "Generating cover PDF...")
    cover_path = os.path.join(notebook_dir, f"cover_{theme_key}.pdf")
    generate_cover(theme_key, theme, cover_path)
    files_generated.append(cover_path)

    # 2. Interior PDF
    print(f"        → Generating interior PDF (120 pages)...")
    interior_path = os.path.join(notebook_dir, f"interior_{theme_key}.pdf")
    generate_interior(theme_key, theme, interior_path)
    files_generated.append(interior_path)

    # 3. Mockup PNG
    print(f"        → Generating product mockup...")
    mockup_png_path = os.path.join(notebook_dir, f"mockup_{theme_key}.png")
    generate_mockup(theme_key, theme, output_path=mockup_png_path)
    files_generated.append(mockup_png_path)

    # 4. Mockup PDF
    mockup_pdf_path = os.path.join(notebook_dir, f"mockup_{theme_key}.pdf")
    generate_mockup_pdf(theme_key, theme, mockup_png_path, mockup_pdf_path)
    files_generated.append(mockup_pdf_path)

    elapsed = time.time() - t0
    print_done(theme_key, elapsed, files_generated)

    return {
        "theme_key": theme_key,
        "name": theme["name_pl"],
        "cover": cover_path,
        "interior": interior_path,
        "mockup_png": mockup_png_path,
        "mockup_pdf": mockup_pdf_path,
        "elapsed": elapsed,
    }


# ─── Summary ──────────────────────────────────────────────────────────────────

def print_summary(results, errors):
    print()
    print("=" * 65)
    print("   GENERATION SUMMARY")
    print("=" * 65)
    print()

    total_time = sum(r["elapsed"] for r in results)

    for i, r in enumerate(results, 1):
        theme = THEMES[r["theme_key"]]
        print(f"  {i:2}. {theme['emoji']}  {r['name']:20} ✓  ({r['elapsed']:.1f}s)")
        print(f"       Cover:    {os.path.basename(r['cover'])}")
        print(f"       Interior: {os.path.basename(r['interior'])}")
        print(f"       Mockup:   {os.path.basename(r['mockup_png'])}")
        print()

    if errors:
        print("  ERRORS:")
        for theme_key, err in errors:
            print(f"  ✗ {theme_key}: {err}")
        print()

    print(f"  Total notebooks generated: {len(results)}/{len(results) + len(errors)}")
    print(f"  Total time: {total_time:.1f}s")
    print()
    print(f"  Output directory: {OUTPUT_DIR}")
    print()
    print("  KDP UPLOAD INSTRUCTIONS:")
    print("  ─────────────────────────")
    print("  1. Go to kdp.amazon.com → Add New Title → Paperback")
    print("  2. Set book details (title, author, description)")
    print("  3. Upload interior_*.pdf as 'Manuscript'")
    print("  4. Upload cover_*.pdf as 'Book Cover'")
    print("  5. Use mockup_*.png for product listing images")
    print("  6. Pricing: recommended $6.99–$8.99 for 120-page notebooks")
    print("=" * 65)
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────

def list_themes():
    print()
    print("Available themes:")
    print("-" * 50)
    for key in PROFESSION_ORDER:
        theme = THEMES[key]
        print(f"  {key:15} {theme['emoji']}  {theme['name_pl']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="KDP Notebook Generator — Generate profession-specific notebooks"
    )
    parser.add_argument(
        "--theme", "-t",
        type=str,
        default=None,
        help="Generate only this theme (e.g., lekarz, informatyk)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available themes and exit"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output directory (default: ./output)"
    )
    args = parser.parse_args()

    if args.list:
        list_themes()
        return

    global OUTPUT_DIR
    if args.output:
        OUTPUT_DIR = os.path.abspath(args.output)

    ensure_dir(OUTPUT_DIR)

    if args.theme:
        if args.theme not in THEMES:
            print(f"ERROR: Theme '{args.theme}' not found.")
            list_themes()
            sys.exit(1)
        themes_to_generate = [args.theme]
    else:
        themes_to_generate = PROFESSION_ORDER

    print_header()
    print(f"  Generating {len(themes_to_generate)} notebook(s)...")
    print()

    results = []
    errors = []

    for i, theme_key in enumerate(themes_to_generate, 1):
        theme = THEMES[theme_key]
        # Folder: 01_budowlaniec, 02_informatyk, ...
        idx = PROFESSION_ORDER.index(theme_key) + 1
        folder_name = f"{idx:02d}_{theme_key}"
        notebook_dir = os.path.join(OUTPUT_DIR, folder_name)

        try:
            result = generate_notebook(theme_key, theme, notebook_dir, i, len(themes_to_generate))
            results.append(result)
        except Exception as e:
            print_error(theme_key, str(e))
            traceback.print_exc()
            errors.append((theme_key, str(e)))

    print_summary(results, errors)


if __name__ == "__main__":
    main()
