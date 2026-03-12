#!/usr/bin/env python3
"""
KDP Notebook Generator — Web Interface
Flask backend serving the UI and generation API.
"""

import os
import json
import time
import copy
import threading
import traceback
from flask import Flask, render_template, request, jsonify, send_file, Response, stream_with_context

from themes import THEMES, PROFESSION_ORDER, KDP_SPECS
from cover_generator import generate_cover
from interior_generator import generate_interior
from mockup_generator import generate_mockup, generate_mockup_pdf

app = Flask(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# In-memory job store: job_id -> {status, progress, messages, files, error}
jobs = {}
jobs_lock = threading.Lock()


def new_job():
    job_id = str(int(time.time() * 1000))
    with jobs_lock:
        jobs[job_id] = {
            "status": "pending",
            "progress": 0,
            "messages": [],
            "files": [],
            "error": None,
        }
    return job_id


def job_log(job_id, msg, progress=None):
    with jobs_lock:
        jobs[job_id]["messages"].append(msg)
        if progress is not None:
            jobs[job_id]["progress"] = progress


def job_done(job_id, files):
    with jobs_lock:
        jobs[job_id]["status"] = "done"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["files"] = files


def job_fail(job_id, error):
    with jobs_lock:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = error


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html",
                           themes=THEMES,
                           profession_order=PROFESSION_ORDER,
                           kdp_specs=KDP_SPECS)


@app.route("/api/themes", methods=["GET"])
def api_themes():
    """Return all theme configs (without heavy data)."""
    result = {}
    for key in PROFESSION_ORDER:
        t = THEMES[key]
        result[key] = {
            "name_pl": t["name_pl"],
            "emoji": t["emoji"],
            "tagline": t["tagline"],
            "subtitle": t["subtitle"],
            "primary": t["primary"],
            "secondary": t["secondary"],
            "accent": t["accent"],
            "cover_bg": t["cover_bg"],
            "bg_light": t["bg_light"],
            "text_dark": t["text_dark"],
            "pattern": t["pattern"],
            "thematic_pages": [p["title"] for p in t.get("thematic_pages", [])],
        }
    return jsonify(result)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """
    Start an async generation job.
    Body (JSON):
    {
      "themes": ["budowlaniec", "lekarz"],   // or ["all"]
      "overrides": {
        "budowlaniec": {
          "tagline": "...",
          "subtitle": "...",
          "primary": [r, g, b],
          "accent": [r, g, b],
          "cover_bg": [r, g, b],
          "total_pages": 120,
          "line_spacing": 0.3
        }
      },
      "options": {
        "generate_cover": true,
        "generate_interior": true,
        "generate_mockup": true
      }
    }
    Returns: { "job_id": "..." }
    """
    data = request.get_json() or {}
    selected = data.get("themes", ["all"])
    overrides = data.get("overrides", {})
    options = data.get("options", {})

    if selected == ["all"] or selected == "all":
        selected = PROFESSION_ORDER[:]

    job_id = new_job()
    thread = threading.Thread(
        target=run_generation,
        args=(job_id, selected, overrides, options),
        daemon=True
    )
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/api/job/<job_id>", methods=["GET"])
def api_job_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)


@app.route("/api/job/<job_id>/stream")
def api_job_stream(job_id):
    """Server-Sent Events stream for real-time progress."""
    def event_stream():
        last_msg_idx = 0
        while True:
            with jobs_lock:
                job = jobs.get(job_id, {})
                status = job.get("status", "pending")
                progress = job.get("progress", 0)
                messages = job.get("messages", [])
                files = job.get("files", [])
                error = job.get("error")

            new_msgs = messages[last_msg_idx:]
            last_msg_idx = len(messages)

            payload = json.dumps({
                "status": status,
                "progress": progress,
                "messages": new_msgs,
                "files": files,
                "error": error,
            })
            yield f"data: {payload}\n\n"

            if status in ("done", "error"):
                break
            time.sleep(0.3)

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.route("/api/download/<path:rel_path>")
def api_download(rel_path):
    """Download a generated file by relative path."""
    full_path = os.path.join(OUTPUT_DIR, rel_path)
    if not os.path.exists(full_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(full_path, as_attachment=True)


@app.route("/api/files", methods=["GET"])
def api_files():
    """List all generated files grouped by notebook."""
    result = []
    if os.path.exists(OUTPUT_DIR):
        for folder in sorted(os.listdir(OUTPUT_DIR)):
            folder_path = os.path.join(OUTPUT_DIR, folder)
            if not os.path.isdir(folder_path):
                continue
            files = []
            for fname in sorted(os.listdir(folder_path)):
                fpath = os.path.join(folder_path, fname)
                files.append({
                    "name": fname,
                    "rel_path": f"{folder}/{fname}",
                    "size_kb": round(os.path.getsize(fpath) / 1024),
                    "type": "cover" if "cover" in fname
                             else "interior" if "interior" in fname
                             else "mockup_pdf" if fname.endswith(".pdf")
                             else "mockup_png",
                })
            result.append({"folder": folder, "files": files})
    return jsonify(result)


# ─── Generation worker ────────────────────────────────────────────────────────

def run_generation(job_id, selected_themes, overrides, options):
    try:
        do_cover = options.get("generate_cover", True)
        do_interior = options.get("generate_interior", True)
        do_mockup = options.get("generate_mockup", True)

        all_files = []
        total = len(selected_themes)

        for i, theme_key in enumerate(selected_themes):
            pct_base = int(i / total * 100)
            job_log(job_id, f"▶ [{i+1}/{total}] Rozpoczynam: {THEMES[theme_key]['name_pl']} {THEMES[theme_key]['emoji']}", pct_base)

            # Build theme with overrides
            theme = build_theme(theme_key, overrides.get(theme_key, {}))

            # Output folder
            idx = PROFESSION_ORDER.index(theme_key) + 1
            folder_name = f"{idx:02d}_{theme_key}"
            notebook_dir = os.path.join(OUTPUT_DIR, folder_name)
            os.makedirs(notebook_dir, exist_ok=True)

            files = []

            if do_cover:
                job_log(job_id, f"  → Generuję okładkę...", pct_base + 5)
                cover_path = os.path.join(notebook_dir, f"cover_{theme_key}.pdf")
                generate_cover(theme_key, theme, cover_path)
                rel = f"{folder_name}/cover_{theme_key}.pdf"
                files.append({"name": f"cover_{theme_key}.pdf", "rel": rel,
                               "size_kb": round(os.path.getsize(cover_path) / 1024),
                               "type": "cover", "theme": theme_key})

            if do_interior:
                job_log(job_id, f"  → Generuję wnętrze (120 stron)...", pct_base + 8)
                interior_path = os.path.join(notebook_dir, f"interior_{theme_key}.pdf")

                # Temporarily patch KDP_SPECS if custom page count
                custom_pages = theme.get("_total_pages")
                custom_spacing = theme.get("_line_spacing")
                if custom_pages:
                    KDP_SPECS["total_pages"] = custom_pages
                if custom_spacing:
                    KDP_SPECS["line_spacing"] = custom_spacing

                generate_interior(theme_key, theme, interior_path)

                # Restore defaults
                KDP_SPECS["total_pages"] = 120
                KDP_SPECS["line_spacing"] = 0.3

                rel = f"{folder_name}/interior_{theme_key}.pdf"
                files.append({"name": f"interior_{theme_key}.pdf", "rel": rel,
                               "size_kb": round(os.path.getsize(interior_path) / 1024),
                               "type": "interior", "theme": theme_key})

            if do_mockup:
                job_log(job_id, f"  → Generuję mockup produktu...", pct_base + 14)
                mockup_png = os.path.join(notebook_dir, f"mockup_{theme_key}.png")
                mockup_pdf = os.path.join(notebook_dir, f"mockup_{theme_key}.pdf")
                generate_mockup(theme_key, theme, output_path=mockup_png)
                generate_mockup_pdf(theme_key, theme, mockup_png, mockup_pdf)
                rel_png = f"{folder_name}/mockup_{theme_key}.png"
                rel_pdf = f"{folder_name}/mockup_{theme_key}.pdf"
                files.append({"name": f"mockup_{theme_key}.png", "rel": rel_png,
                               "size_kb": round(os.path.getsize(mockup_png) / 1024),
                               "type": "mockup_png", "theme": theme_key})
                files.append({"name": f"mockup_{theme_key}.pdf", "rel": rel_pdf,
                               "size_kb": round(os.path.getsize(mockup_pdf) / 1024),
                               "type": "mockup_pdf", "theme": theme_key})

            all_files.extend(files)
            pct_done = int((i + 1) / total * 100)
            job_log(job_id, f"  ✓ Gotowe: {theme['name_pl']} ({len(files)} pliki)", pct_done)

        job_log(job_id, f"✅ Wygenerowano {total} zeszyt(ów)!", 100)
        job_done(job_id, all_files)

    except Exception as e:
        tb = traceback.format_exc()
        job_log(job_id, f"❌ Błąd: {e}")
        job_fail(job_id, str(e))


def build_theme(theme_key, override):
    """Deep-copy base theme and apply user overrides."""
    theme = copy.deepcopy(THEMES[theme_key])

    if "tagline" in override:
        theme["tagline"] = override["tagline"]
    if "subtitle" in override:
        theme["subtitle"] = override["subtitle"]
    if "primary" in override:
        theme["primary"] = tuple(override["primary"])
    if "accent" in override:
        theme["accent"] = tuple(override["accent"])
    if "cover_bg" in override:
        theme["cover_bg"] = tuple(override["cover_bg"])
    if "total_pages" in override:
        theme["_total_pages"] = int(override["total_pages"])
    if "line_spacing" in override:
        theme["_line_spacing"] = float(override["line_spacing"])

    return theme


if __name__ == "__main__":
    print("=" * 55)
    print("  KDP Notebook Generator — Web Interface")
    print("  Otwórz: http://localhost:5000")
    print("=" * 55)
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
