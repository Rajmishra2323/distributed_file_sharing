from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import os

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB
app.secret_key = "change-this-secret-key"

UPLOAD_FOLDER.mkdir(exist_ok=True)


def get_files(search=""):
    """Return uploaded files, optionally filtered by filename."""
    files = []

    for path in UPLOAD_FOLDER.iterdir():
        if not path.is_file():
            continue

        # Search is case-insensitive and works with partial filenames.
        if search and search.lower() not in path.name.lower():
            continue

        stat = path.stat()
        files.append({
            "name": path.name,
            "size": format_size(stat.st_size),
            "size_bytes": stat.st_size,
            "uploaded_at": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        })

    files.sort(key=lambda item: item["uploaded_at"], reverse=True)
    return files


def format_size(size):
    if size < 1024:
        return f"{size} B"
    if size < 1024 ** 2:
        return f"{size / 1024:.1f} KB"
    if size < 1024 ** 3:
        return f"{size / (1024 ** 2):.1f} MB"
    return f"{size / (1024 ** 3):.1f} GB"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename:
            flash("Please choose a file.", "error")
            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)

        if not filename:
            flash("Invalid filename.", "error")
            return redirect(url_for("upload"))

        # secure_filename removes unsafe path characters.
        # If the same name already exists, add a timestamp suffix.
        destination = UPLOAD_FOLDER / filename

        if destination.exists():
            stem = destination.stem
            suffix = destination.suffix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{stem}_{timestamp}{suffix}"
            destination = UPLOAD_FOLDER / filename

        file.save(destination)

        flash(f"'{filename}' uploaded successfully.", "success")
        return redirect(url_for("files"))

    return render_template("upload.html")


@app.route("/files")
def files():
    search = request.args.get("q", "").strip()
    file_list = get_files(search)
    return render_template(
        "files.html",
        files=file_list,
        search=search
    )


@app.route("/download/<path:filename>")
def download(filename):
    # send_from_directory prevents a user from using ../ to escape uploads.
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


@app.errorhandler(413)
def file_too_large(error):
    flash("File is too large. Maximum size is 100 MB.", "error")
    return redirect(url_for("upload"))


if __name__ == "__main__":
    print("Distributed File Sharing System")
    print("Open: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
