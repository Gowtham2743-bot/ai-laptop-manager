# COMPLETE server.py
# AI LAPTOP MANAGER
# FastAPI + React frontend + EXE launcher

import os
import shutil
import hashlib
import ctypes
import tempfile
import threading
import time
import webbrowser

from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import uvicorn


# ============================================================
# APP
# ============================================================

app = FastAPI(title="AI Laptop Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

HOME = Path.home()

BASE_DIR = Path(__file__).resolve().parent

FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


SEARCH_FOLDERS = [
    HOME / "Desktop",
    HOME / "Documents",
    HOME / "Downloads",
    HOME / "OneDrive",
    Path("C:/"),
    Path("D:/"),
]


IGNORED_SEARCH_EXTENSIONS = {
    ".lnk",
    ".svg",
    ".dat",
    ".tmp",
    ".log",
}


VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov",
    ".wmv", ".flv", ".webm", ".m4v"
}


DOCUMENT_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".txt",
    ".rtf", ".xls", ".xlsx",
    ".ppt", ".pptx", ".csv"
}


IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png",
    ".gif", ".bmp", ".webp", ".tiff"
}


AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".aac",
    ".m4a", ".flac", ".ogg"
}


ARCHIVE_EXTENSIONS = {
    ".zip", ".rar", ".7z",
    ".tar", ".gz", ".iso"
}


SOFTWARE_EXTENSIONS = {
    ".exe", ".msi", ".apk"
}


SUSPICIOUS_EXTENSIONS = {
    ".exe", ".msi", ".bat", ".cmd",
    ".scr", ".vbs", ".vbe", ".js",
    ".jse", ".wsf", ".wsh", ".ps1",
    ".hta", ".com"
}


# ============================================================
# SAFETY
# ============================================================

def is_skipped_path(path):

    text = str(path).replace("\\", "/").lower()

    skip_patterns = [
        "/windows/",
        "/program files/",
        "/program files (x86)/",
        "/programdata/",
        "/$recycle.bin/",
        "/system volume information/",
        "/appdata/local/temp/",
        "/node_modules/",
        "/.git/",
        "/__pycache__/",
    ]

    return any(x in text for x in skip_patterns)


def safe_walk(base):

    try:

        for root, dirs, files in os.walk(
            base,
            topdown=True,
            onerror=lambda e: None
        ):

            dirs[:] = [
                d for d in dirs
                if not is_skipped_path(Path(root) / d)
            ]

            yield Path(root), files

    except Exception:
        return


# ============================================================
# HELPERS
# ============================================================

def format_size(size):

    size = float(size)

    if size < 1024:
        return f"{size:.0f} B"

    if size < 1024 ** 2:
        return f"{size / 1024:.1f} KB"

    if size < 1024 ** 3:
        return f"{size / (1024 ** 2):.1f} MB"

    if size < 1024 ** 4:
        return f"{size / (1024 ** 3):.2f} GB"

    return f"{size / (1024 ** 4):.2f} TB"


def classify_file(path):

    ext = path.suffix.lower()

    if ext in VIDEO_EXTENSIONS:
        return "Movies"

    if ext in DOCUMENT_EXTENSIONS:
        return "Documents"

    if ext in IMAGE_EXTENSIONS:
        return "Images"

    if ext in AUDIO_EXTENSIONS:
        return "Audio"

    if ext in ARCHIVE_EXTENSIONS:
        return "Archives"

    if ext in SOFTWARE_EXTENSIONS:
        return "Software"

    return "Other"


def file_info(path):

    try:

        stat = path.stat()

        return {
            "name": path.name,
            "path": str(path),
            "size": stat.st_size,
            "size_text": format_size(stat.st_size),
            "type": path.suffix.lower() or "File",
            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }

    except Exception:
        return None


# ============================================================
# FRONTEND
# ============================================================

@app.get("/")
def frontend_home():

    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():
        return FileResponse(index_file)

    return {
        "app": "AI Laptop Manager",
        "status": "running",
        "message": "Frontend build not found. Run npm run build."
    }


if FRONTEND_DIST.exists():

    app.mount(
        "/assets",
        StaticFiles(directory=str(FRONTEND_DIST / "assets")),
        name="assets"
    )


# ============================================================
# STORAGE
# ============================================================

@app.get("/storage")
def storage():

    result = []

    for drive in ["C:/", "D:/"]:

        try:

            total, used, free = shutil.disk_usage(drive)

            result.append({
                "drive": drive,
                "total": total,
                "used": used,
                "free": free,
                "total_text": format_size(total),
                "used_text": format_size(used),
                "free_text": format_size(free),
                "used_percent": round(
                    used / total * 100,
                    1
                )
            })

        except Exception:
            pass

    return result


@app.get("/storage-alert")
def storage_alert():

    alerts = []

    for drive in ["C:/", "D:/"]:

        try:

            total, used, free = shutil.disk_usage(drive)

            free_gb = free / (1024 ** 3)

            if free_gb < 15:

                level = "critical"
                message = "VERY LOW FREE SPACE"

            elif free_gb < 25:

                level = "warning"
                message = "Free space is getting low"

            else:

                level = "good"
                message = "Storage is healthy"

            alerts.append({
                "drive": drive,
                "free_gb": round(free_gb, 2),
                "level": level,
                "message": message
            })

        except Exception:
            pass

    return alerts


# ============================================================
# SEARCH
# ============================================================

@app.get("/search")
def search_files(keyword: str = Query(...)):

    keyword = keyword.strip().lower()

    if not keyword:
        return []

    results = []

    for folder in SEARCH_FOLDERS:

        if not folder.exists():
            continue

        for root, files in safe_walk(folder):

            for filename in files:

                try:

                    path = root / filename

                    if path.suffix.lower() in IGNORED_SEARCH_EXTENSIONS:
                        continue

                    if keyword in filename.lower():

                        info = file_info(path)

                        if info:

                            info["priority"] = (
                                0
                                if filename.lower().startswith(keyword)
                                else 1
                            )

                            results.append(info)

                except Exception:
                    continue

                if len(results) >= 50:
                    break

            if len(results) >= 50:
                break

        if len(results) >= 50:
            break

    results.sort(
        key=lambda x: (
            x["priority"],
            -x["size"]
        )
    )

    return results[:50]


# ============================================================
# OPEN
# ============================================================

@app.post("/open")
def open_file(path: str):

    try:

        target = Path(path)

        if not target.exists():

            return {
                "success": False,
                "message": "File not found."
            }

        os.startfile(str(target))

        return {
            "success": True,
            "message": f"Opened {target.name}"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


@app.post("/open-folder")
def open_folder(path: str):

    try:

        target = Path(path)

        if not target.exists():

            return {
                "success": False,
                "message": "Folder not found."
            }

        folder = (
            target
            if target.is_dir()
            else target.parent
        )

        os.startfile(str(folder))

        return {
            "success": True,
            "message": "Folder opened."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# RECENT
# ============================================================

@app.get("/recent")
def recent_files():

    results = []

    folders = [
        HOME / "Downloads",
        HOME / "Desktop",
        HOME / "Documents"
    ]

    for folder in folders:

        if not folder.exists():
            continue

        for root, files in safe_walk(folder):

            for filename in files:

                try:

                    info = file_info(
                        root / filename
                    )

                    if info:
                        results.append(info)

                except Exception:
                    continue

    results.sort(
        key=lambda x: x["modified"],
        reverse=True
    )

    return results[:50]


# ============================================================
# LARGE FILES
# ============================================================

@app.get("/large-files")
def large_files():

    results = []

    folders = [
        HOME / "Downloads",
        HOME / "Desktop",
        HOME / "Documents",
        Path("D:/")
    ]

    for folder in folders:

        if not folder.exists():
            continue

        for root, files in safe_walk(folder):

            for filename in files:

                try:

                    path = root / filename

                    if path.stat().st_size >= (
                        500 * 1024 * 1024
                    ):

                        info = file_info(path)

                        if info:
                            results.append(info)

                except Exception:
                    continue

    results.sort(
        key=lambda x: x["size"],
        reverse=True
    )

    return results[:50]


# ============================================================
# DOWNLOADS
# ============================================================

@app.get("/downloads")
def analyze_downloads():

    folder = HOME / "Downloads"

    categories = {}

    if not folder.exists():
        return []

    for root, files in safe_walk(folder):

        for filename in files:

            try:

                path = root / filename
                category = classify_file(path)
                size = path.stat().st_size

                if category not in categories:

                    categories[category] = {
                        "files": 0,
                        "bytes": 0
                    }

                categories[category]["files"] += 1
                categories[category]["bytes"] += size

            except Exception:
                continue

    result = []

    for category, data in categories.items():

        result.append({
            "category": category,
            "files": data["files"],
            "bytes": data["bytes"],
            "size_text": format_size(
                data["bytes"]
            )
        })

    result.sort(
        key=lambda x: x["bytes"],
        reverse=True
    )

    return result


# ============================================================
# CLEANUP
# ============================================================

def get_temp_size():

    total = 0

    folder = Path(tempfile.gettempdir())

    for root, files in safe_walk(folder):

        for filename in files:

            try:
                total += (
                    root / filename
                ).stat().st_size

            except Exception:
                continue

    return total


def get_recycle_bin_size():

    total = 0

    for drive in ["C:/", "D:/"]:

        folder = Path(drive) / "$Recycle.Bin"

        if not folder.exists():
            continue

        for root, files in safe_walk(folder):

            for filename in files:

                try:
                    total += (
                        root / filename
                    ).stat().st_size

                except Exception:
                    continue

    return total


@app.get("/cleanup-recommendations")
def cleanup_recommendations():

    temp_size = get_temp_size()
    recycle_size = get_recycle_bin_size()

    recommendations = []

    if temp_size > 0:

        recommendations.append({
            "type": "temp",
            "name": "Temporary files",
            "size": temp_size,
            "size_text": format_size(temp_size),
            "safe": True,
            "description":
                "User temporary files that can normally be cleaned."
        })

    if recycle_size > 0:

        recommendations.append({
            "type": "recycle_bin",
            "name": "Recycle Bin",
            "size": recycle_size,
            "size_text": format_size(recycle_size),
            "safe": True,
            "description":
                "Files currently stored in the Recycle Bin."
        })

    return recommendations


@app.post("/cleanup/temp")
def cleanup_temp():

    deleted = 0
    freed = 0

    folder = Path(tempfile.gettempdir())

    for root, files in safe_walk(folder):

        for filename in files:

            try:

                path = root / filename
                size = path.stat().st_size

                path.unlink()

                deleted += 1
                freed += size

            except Exception:
                continue

    return {
        "success": True,
        "deleted_files": deleted,
        "freed_bytes": freed,
        "freed_text": format_size(freed),
        "message":
            f"Cleaned {format_size(freed)} of temporary files."
    }


@app.post("/cleanup/recycle-bin")
def empty_recycle_bin():

    try:

        if os.name != "nt":

            return {
                "success": False,
                "message":
                    "Recycle Bin cleanup is supported on Windows."
            }

        result = ctypes.windll.shell32.SHEmptyRecycleBinW(
            None,
            None,
            0x00000001 |
            0x00000002 |
            0x00000004
        )

        if result == 0:

            return {
                "success": True,
                "message":
                    "Recycle Bin emptied successfully."
            }

        return {
            "success": False,
            "message":
                "Could not empty Recycle Bin."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# ORGANIZER
# ============================================================

@app.get("/organize-preview")
def organize_preview():

    downloads = HOME / "Downloads"

    results = []

    if not downloads.exists():
        return results

    for item in downloads.iterdir():

        if not item.is_file():
            continue

        category = classify_file(item)

        if category == "Other":
            continue

        try:

            size = item.stat().st_size

        except Exception:
            continue

        results.append({
            "name": item.name,
            "path": str(item),
            "category": category,
            "size": size,
            "size_text": format_size(size)
        })

    return results[:300]


@app.post("/organize-downloads")
def organize_downloads():

    downloads = HOME / "Downloads"

    moved = 0

    folders = {
        "Movies": downloads / "Movies",
        "Documents": downloads / "Documents",
        "Images": downloads / "Images",
        "Audio": downloads / "Audio",
        "Archives": downloads / "Archives",
        "Software": downloads / "Software"
    }

    for folder in folders.values():
        folder.mkdir(
            exist_ok=True
        )

    for item in downloads.iterdir():

        if not item.is_file():
            continue

        category = classify_file(item)

        if category not in folders:
            continue

        destination = (
            folders[category] /
            item.name
        )

        if destination.exists():
            continue

        try:

            shutil.move(
                str(item),
                str(destination)
            )

            moved += 1

        except Exception:
            continue

    return {
        "success": True,
        "moved": moved,
        "message":
            f"Organized {moved} file(s)."
    }


# ============================================================
# SECURITY
# ============================================================

@app.get("/security")
def security_check():

    results = []

    folders = [
        HOME / "Downloads",
        HOME / "Desktop",
        HOME / "Documents"
    ]

    for folder in folders:

        if not folder.exists():
            continue

        for root, files in safe_walk(folder):

            for filename in files:

                try:

                    path = root / filename

                    if (
                        path.suffix.lower()
                        in SUSPICIOUS_EXTENSIONS
                    ):

                        info = file_info(path)

                        if info:

                            info["reason"] = (
                                "Executable or script file. "
                                "Review before running."
                            )

                            results.append(info)

                except Exception:
                    continue

                if len(results) >= 300:
                    return results

    return results


# ============================================================
# DUPLICATES
# ============================================================

def sha256_file(path):

    sha = hashlib.sha256()

    try:

        with open(
            path,
            "rb"
        ) as f:

            while True:

                chunk = f.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()

    except Exception:
        return None


@app.get("/duplicates")
def duplicates():

    size_groups = {}

    folders = [
        HOME / "Downloads",
        HOME / "Desktop",
        HOME / "Documents",
        Path("D:/")
    ]

    for folder in folders:

        if not folder.exists():
            continue

        for root, files in safe_walk(folder):

            for filename in files:

                try:

                    path = root / filename
                    size = path.stat().st_size

                    if size < 1024 * 1024:
                        continue

                    size_groups.setdefault(
                        size,
                        []
                    ).append(path)

                except Exception:
                    continue

    duplicate_groups = []

    for size, paths in size_groups.items():

        if len(paths) < 2:
            continue

        hashes = {}

        for path in paths:

            digest = sha256_file(path)

            if digest:

                hashes.setdefault(
                    digest,
                    []
                ).append(path)

        for digest, same_files in hashes.items():

            if len(same_files) < 2:
                continue

            files = []

            for path in same_files:

                info = file_info(path)

                if info:
                    files.append(info)

            if len(files) >= 2:

                wasted = (
                    size *
                    (len(files) - 1)
                )

                duplicate_groups.append({
                    "hash": digest,
                    "size": size,
                    "size_text": format_size(size),
                    "files": files,
                    "count": len(files),
                    "wasted_bytes": wasted,
                    "wasted_text": format_size(wasted)
                })

    duplicate_groups.sort(
        key=lambda x: x["wasted_bytes"],
        reverse=True
    )

    return duplicate_groups[:50]


# ============================================================
# OLD FILES
# ============================================================

@app.get("/old-files")
def old_files():

    cutoff = (
        datetime.now() -
        timedelta(days=365)
    )

    results = []

    folders = [
        HOME / "Downloads",
        HOME / "Desktop",
        HOME / "Documents",
        Path("D:/")
    ]

    for folder in folders:

        if not folder.exists():
            continue

        for root, files in safe_walk(folder):

            for filename in files:

                try:

                    path = root / filename

                    modified = datetime.fromtimestamp(
                        path.stat().st_mtime
                    )

                    if modified < cutoff:

                        info = file_info(path)

                        if info:
                            results.append(info)

                except Exception:
                    continue

    results.sort(
        key=lambda x: x["size"],
        reverse=True
    )

    return results[:100]


# ============================================================
# COMMAND
# ============================================================

@app.get("/command")
def command(text: str = Query(...)):

    command_text = text.lower().strip()

    if "storage" in command_text:

        return {
            "action": "storage",
            "message":
                "Showing storage information."
        }

    if "download" in command_text:

        return {
            "action": "downloads",
            "message":
                "Analyzing Downloads."
        }

    if "duplicate" in command_text:

        return {
            "action": "duplicates",
            "message":
                "Searching for duplicates."
        }

    if (
        "security" in command_text
        or "suspicious" in command_text
    ):

        return {
            "action": "security",
            "message":
                "Checking suspicious files."
        }

    if "old file" in command_text:

        return {
            "action": "old-files",
            "message":
                "Finding old files."
        }

    if "clean" in command_text:

        return {
            "action": "cleanup",
            "message":
                "Checking safe cleanup options."
        }

    if "organize" in command_text:

        return {
            "action": "organize",
            "message":
                "Preparing Downloads organization."
        }

    return {
        "action": "search",
        "keyword": text,
        "message":
            f"Searching for {text}."
    }


# ============================================================
# SPA FALLBACK
# ============================================================

@app.get("/{full_path:path}")
def spa_fallback(full_path: str):

    requested = FRONTEND_DIST / full_path

    if requested.exists() and requested.is_file():

        return FileResponse(requested)

    index_file = FRONTEND_DIST / "index.html"

    if index_file.exists():

        return FileResponse(index_file)

    return {
        "error": "Frontend not found"
    }


# ============================================================
# EXE LAUNCHER
# ============================================================

def start_server():

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="warning"
    )


def open_browser():

    time.sleep(2)

    webbrowser.open(
        "http://127.0.0.1:8000/"
    )


if __name__ == "__main__":

    print("=" * 50)
    print("AI LAPTOP MANAGER")
    print("=" * 50)
    print("Starting server...")
    print("Opening AI Laptop Manager...")
    print("=" * 50)

    server_thread = threading.Thread(
        target=start_server,
        daemon=True
    )

    server_thread.start()

    open_browser()

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("AI Laptop Manager stopped.")