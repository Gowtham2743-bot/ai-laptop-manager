import os
import shutil
import ctypes
import tempfile
import hashlib
from datetime import datetime, timedelta


# ============================================================
# AI LAPTOP MANAGER
# ============================================================

HOME = os.path.expanduser("~")

PERSONAL_FOLDERS = [
    os.path.join(HOME, "Downloads"),
    os.path.join(HOME, "Desktop"),
    os.path.join(HOME, "Documents"),
    os.path.join(HOME, "OneDrive"),
]

SEARCH_FOLDERS = [
    os.path.join(HOME, "Downloads"),
    os.path.join(HOME, "Desktop"),
    os.path.join(HOME, "Documents"),
    os.path.join(HOME, "OneDrive"),
    "D:\\",
]

SKIP_FOLDERS = {
    "node_modules",
    ".git",
    ".gradle",
    ".idea",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".env",
    "dist",
    "build",
    "Recent",
    "Recent Items",
    "AppData",
}

SKIP_PATH_PARTS = {
    "AppData",
    ".p2",
    "node_modules",
    ".git",
    "Program Files",
    "Program Files (x86)",
    "ProgramData",
    "Windows",
    "$Recycle.Bin",
}

IGNORED_SEARCH_EXTENSIONS = {
    ".lnk",
    ".svg",
    ".dat",
    ".tmp",
    ".log",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    ".mpeg",
    ".mpg",
}

DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".csv",
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
}

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".aac",
    ".flac",
    ".m4a",
    ".ogg",
}

ARCHIVE_EXTENSIONS = {
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".iso",
}

SOFTWARE_EXTENSIONS = {
    ".exe",
    ".msi",
    ".apk",
    ".dmg",
}

SUSPICIOUS_EXTENSIONS = {
    ".exe",
    ".msi",
    ".bat",
    ".cmd",
    ".scr",
    ".vbs",
    ".vbe",
    ".js",
    ".jse",
    ".wsf",
    ".wsh",
    ".ps1",
    ".hta",
    ".com",
}


# ============================================================
# COMMON HELPERS
# ============================================================

def is_skipped_path(path):
    path_lower = path.lower()

    for part in SKIP_PATH_PARTS:
        if part.lower() in path_lower:
            return True

    return False


def safe_walk(base):
    if not os.path.exists(base):
        return

    try:
        for root, dirs, files in os.walk(base):
            dirs[:] = [
                d for d in dirs
                if d not in SKIP_FOLDERS
            ]

            if is_skipped_path(root):
                continue

            yield root, dirs, files

    except (PermissionError, OSError):
        return


def format_size(size):
    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"

    if size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"

    if size >= 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size} B"


def classify_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext in VIDEO_EXTENSIONS:
        return "Movie / Video"

    if ext in DOCUMENT_EXTENSIONS:
        return "Document"

    if ext in ARCHIVE_EXTENSIONS:
        return "Archive"

    if ext in SOFTWARE_EXTENSIONS:
        return "Software / Installer"

    if ext in IMAGE_EXTENSIONS:
        return "Image"

    if ext in AUDIO_EXTENSIONS:
        return "Audio"

    return "Other"


# ============================================================
# 1. SYSTEM SCAN
# ============================================================

def scan_laptop():
    print("\n" + "=" * 60)
    print("AI LAPTOP MANAGER - FULL SCAN")
    print("=" * 60)

    for drive in ["C:\\", "D:\\"]:
        if not os.path.exists(drive):
            continue

        print(f"\nScanning {drive} ...")

        total_files = 0
        total_folders = 0

        try:
            for root, dirs, files in os.walk(drive):
                total_folders += len(dirs)
                total_files += len(files)

        except (PermissionError, OSError):
            pass

        print(f"Folders : {total_folders:,}")
        print(f"Files   : {total_files:,}")

    print("\nScan completed.")
    print("No files were deleted or moved.")


# ============================================================
# 2. STORAGE
# ============================================================

def show_storage():
    print("\n" + "=" * 60)
    print("STORAGE STATUS")
    print("=" * 60)

    for drive in ["C:\\", "D:\\"]:
        if not os.path.exists(drive):
            continue

        try:
            total, used, free = shutil.disk_usage(drive)

            print(f"\n{drive}")
            print(f"Total : {format_size(total)}")
            print(f"Used  : {format_size(used)}")
            print(f"Free  : {format_size(free)}")

            free_gb = free / (1024 ** 3)

            if free_gb < 15:
                print("Status: VERY LOW FREE SPACE ⚠️")

            elif free_gb < 25:
                print("Status: Free space is getting low ⚠️")

            else:
                print("Status: Good ✅")

        except Exception as e:
            print(f"Could not read {drive}: {e}")


# ============================================================
# 3. LOW STORAGE ALERT
# ============================================================

def low_storage_alert():
    print("\n" + "=" * 60)
    print("LOW STORAGE ALERT")
    print("=" * 60)

    found_warning = False

    for drive in ["C:\\", "D:\\"]:
        if not os.path.exists(drive):
            continue

        try:
            total, used, free = shutil.disk_usage(drive)
            free_gb = free / (1024 ** 3)

            if free_gb < 15:
                print(
                    f"⚠️ {drive} has only {free_gb:.2f} GB free."
                )
                print("Recommendation: Review large files and Downloads.")
                found_warning = True

            elif free_gb < 25:
                print(
                    f"⚠️ {drive} has {free_gb:.2f} GB free."
                )
                print("Recommendation: Consider cleaning unnecessary files.")
                found_warning = True

            else:
                print(f"✅ {drive} has {free_gb:.2f} GB free.")

        except Exception:
            pass

    if not found_warning:
        print("\nYour available storage is currently healthy.")


# ============================================================
# 4. SMART STORAGE ANALYZER
# ============================================================

def smart_storage_analyzer():
    print("\n" + "=" * 60)
    print("SMART STORAGE ANALYZER")
    print("=" * 60)

    files_found = []

    scan_locations = [
        os.path.join(HOME, "Downloads"),
        os.path.join(HOME, "Desktop"),
        os.path.join(HOME, "Documents"),
        os.path.join(HOME, "OneDrive"),
        "D:\\",
    ]

    for base in scan_locations:

        if not os.path.exists(base):
            continue

        for root, dirs, files in safe_walk(base):

            for filename in files:

                path = os.path.join(root, filename)

                try:
                    size = os.path.getsize(path)

                    if size >= 500 * 1024 * 1024:
                        files_found.append((size, path))

                except (PermissionError, OSError):
                    continue

    files_found.sort(reverse=True)

    if not files_found:
        print("\nNo files larger than 500 MB found.")
        return

    print(f"\nFound {len(files_found)} files larger than 500 MB.\n")

    for index, (size, path) in enumerate(files_found[:20], 1):

        category = classify_file(path)

        print(
            f"{index}. {format_size(size)} | "
            f"{category}\n   {path}"
        )

    print("\nAnalysis only.")
    print("Nothing was deleted.")


# ============================================================
# 5. DOWNLOAD ANALYZER
# ============================================================

def analyze_downloads():
    downloads = os.path.join(HOME, "Downloads")

    print("\n" + "=" * 60)
    print("DOWNLOADS ANALYSIS")
    print("=" * 60)

    if not os.path.exists(downloads):
        print("Downloads folder not found.")
        return

    categories = {
        "Movies/Videos": [0, 0],
        "Documents": [0, 0],
        "Archives": [0, 0],
        "Software": [0, 0],
        "Images": [0, 0],
        "Audio": [0, 0],
        "Other": [0, 0],
    }

    total_size = 0
    total_files = 0

    for root, dirs, files in safe_walk(downloads):

        for filename in files:

            path = os.path.join(root, filename)

            try:
                size = os.path.getsize(path)
            except (PermissionError, OSError):
                continue

            total_files += 1
            total_size += size

            ext = os.path.splitext(filename)[1].lower()

            if ext in VIDEO_EXTENSIONS:
                category = "Movies/Videos"

            elif ext in DOCUMENT_EXTENSIONS:
                category = "Documents"

            elif ext in ARCHIVE_EXTENSIONS:
                category = "Archives"

            elif ext in SOFTWARE_EXTENSIONS:
                category = "Software"

            elif ext in IMAGE_EXTENSIONS:
                category = "Images"

            elif ext in AUDIO_EXTENSIONS:
                category = "Audio"

            else:
                category = "Other"

            categories[category][0] += 1
            categories[category][1] += size

    for category, values in categories.items():
        print(
            f"{category:<18} "
            f"{values[0]:>8,} files | "
            f"{format_size(values[1])}"
        )

    print("\nTotal Downloads:")
    print(f"Files : {total_files:,}")
    print(f"Size  : {format_size(total_size)}")


# ============================================================
# 6. SEARCH
# ============================================================

def search_files(keyword):
    print("\n" + "=" * 60)
    print(f"SEARCH: {keyword}")
    print("=" * 60)

    keyword = keyword.lower().strip()

    results = []

    for base in SEARCH_FOLDERS:

        if not os.path.exists(base):
            continue

        for root, dirs, files in safe_walk(base):

            for filename in files:

                if filename.lower().endswith(
                    tuple(IGNORED_SEARCH_EXTENSIONS)
                ):
                    continue

                if keyword in filename.lower():

                    path = os.path.join(root, filename)

                    try:
                        size = os.path.getsize(path)
                    except (PermissionError, OSError):
                        size = 0

                    starts = filename.lower().startswith(keyword)

                    results.append(
                        (
                            not starts,
                            filename.lower(),
                            size,
                            path
                        )
                    )

    results.sort()

    if not results:
        print("No matching files found.")
        return

    print(f"\nFound {len(results)} matching files.\n")

    for index, (_, _, size, path) in enumerate(results[:50], 1):
        print(
            f"{index}. {os.path.basename(path)} "
            f"({format_size(size)})"
        )
        print(f"   {path}")

    if len(results) > 50:
        print("\nShowing first 50 results.")


def search_resume(command):
    command = command.lower()

    if "java" in command:
        keyword = "Java_FullStack_Resume"

    elif "cloud" in command:
        keyword = "Cloud_Developer_Resume"

    elif "software" in command:
        keyword = "Software_Developer_Resume"

    else:
        keyword = "Gowtham"

    search_files(keyword)


def search_movies():
    print("\n" + "=" * 60)
    print("MOVIE SEARCH")
    print("=" * 60)

    found = []

    for base in SEARCH_FOLDERS:

        if not os.path.exists(base):
            continue

        for root, dirs, files in safe_walk(base):

            for filename in files:

                ext = os.path.splitext(filename)[1].lower()

                if ext not in VIDEO_EXTENSIONS:
                    continue

                path = os.path.join(root, filename)

                try:
                    size = os.path.getsize(path)
                except (PermissionError, OSError):
                    size = 0

                found.append((size, filename, path))

    found.sort(reverse=True)

    if not found:
        print("No movies/videos found.")
        return

    print(f"\nFound {len(found)} video files.\n")

    for index, (size, filename, path) in enumerate(found[:50], 1):
        print(
            f"{index}. {filename} "
            f"({format_size(size)})"
        )
        print(f"   {path}")


# ============================================================
# 7. DUPLICATE FILE FINDER
# ============================================================

def file_hash(path, chunk_size=1024 * 1024):
    sha256 = hashlib.sha256()

    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, OSError):
        return None


def duplicate_finder():
    print("\n" + "=" * 60)
    print("DUPLICATE FILE FINDER")
    print("=" * 60)

    print("\nScanning files...")
    print("This may take some time.")

    size_groups = {}

    for base in SEARCH_FOLDERS:

        if not os.path.exists(base):
            continue

        for root, dirs, files in safe_walk(base):

            for filename in files:

                path = os.path.join(root, filename)

                try:
                    size = os.path.getsize(path)
                except (PermissionError, OSError):
                    continue

                # Ignore tiny files
                if size < 1 * 1024 * 1024:
                    continue

                size_groups.setdefault(size, []).append(path)

    duplicate_groups = []

    for size, paths in size_groups.items():

        if len(paths) < 2:
            continue

        hashes = {}

        for path in paths:

            digest = file_hash(path)

            if digest:
                hashes.setdefault(digest, []).append(path)

        for digest, same_files in hashes.items():

            if len(same_files) > 1:
                duplicate_groups.append(
                    (size, same_files)
                )

    if not duplicate_groups:
        print("\nNo duplicate files found.")
        return

    duplicate_groups.sort(
        key=lambda x: x[0] * (len(x[1]) - 1),
        reverse=True
    )

    total_wasted = 0

    print(
        f"\nFound {len(duplicate_groups)} duplicate groups.\n"
    )

    for index, (size, paths) in enumerate(
        duplicate_groups[:30], 1
    ):

        wasted = size * (len(paths) - 1)
        total_wasted += wasted

        print(
            f"{index}. {len(paths)} identical files | "
            f"{format_size(size)} each"
        )

        for path in paths:
            print(f"   {path}")

        print()

    print(
        f"Potential duplicate space: "
        f"{format_size(total_wasted)}"
    )

    print("\nNothing was deleted.")


# ============================================================
# 8. SUSPICIOUS FILE CHECKER
# ============================================================

def suspicious_file_checker():
    print("\n" + "=" * 60)
    print("SUSPICIOUS FILE CHECKER")
    print("=" * 60)

    print(
        "\nThis is a safety review, not a virus scanner."
    )

    suspicious = []

    for base in SEARCH_FOLDERS:

        if not os.path.exists(base):
            continue

        for root, dirs, files in safe_walk(base):

            for filename in files:

                ext = os.path.splitext(filename)[1].lower()

                if ext not in SUSPICIOUS_EXTENSIONS:
                    continue

                path = os.path.join(root, filename)

                try:
                    size = os.path.getsize(path)
                    modified = datetime.fromtimestamp(
                        os.path.getmtime(path)
                    )

                    suspicious.append(
                        (
                            modified,
                            size,
                            filename,
                            path
                        )
                    )

                except (PermissionError, OSError):
                    continue

    suspicious.sort(reverse=True)

    if not suspicious:
        print("\nNo files requiring this basic review were found.")
        return

    print(
        f"\nFound {len(suspicious)} executable/script files "
        f"for review.\n"
    )

    for index, (modified, size, filename, path) in enumerate(
        suspicious[:50], 1
    ):

        print(
            f"{index}. {filename} | "
            f"{format_size(size)}"
        )
        print(f"   Modified: {modified}")
        print(f"   {path}")

    print("\n⚠️ Important:")
    print("- An executable file is NOT automatically a virus.")
    print("- Do not delete Windows/program files based only on this list.")
    print("- Review unknown files before taking action.")


# ============================================================
# 9. OLD FILE ANALYZER
# ============================================================

def old_file_analyzer():
    print("\n" + "=" * 60)
    print("OLD FILE ANALYZER")
    print("=" * 60)

    print("\nChecking files older than 1 year...")

    cutoff = datetime.now() - timedelta(days=365)

    old_files = []

    for base in SEARCH_FOLDERS:

        if not os.path.exists(base):
            continue

        for root, dirs, files in safe_walk(base):

            for filename in files:

                path = os.path.join(root, filename)

                try:
                    modified = datetime.fromtimestamp(
                        os.path.getmtime(path)
                    )

                    if modified < cutoff:

                        size = os.path.getsize(path)

                        old_files.append(
                            (
                                size,
                                modified,
                                path
                            )
                        )

                except (PermissionError, OSError):
                    continue

    old_files.sort(reverse=True)

    if not old_files:
        print("\nNo files older than one year found.")
        return

    print(
        f"\nFound {len(old_files):,} files older than one year."
    )

    print("\nLargest old files:\n")

    for index, (size, modified, path) in enumerate(
        old_files[:50], 1
    ):

        print(
            f"{index}. {format_size(size)} | "
            f"{modified.date()}"
        )
        print(f"   {path}")

    print("\nThese are recommendations only.")
    print("Nothing was deleted.")


# ============================================================
# 10. SMART FILE ORGANIZER
# ============================================================

def organizer_category(filename):
    ext = os.path.splitext(filename)[1].lower()

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


def smart_file_organizer():
    print("\n" + "=" * 60)
    print("SMART FILE ORGANIZER")
    print("=" * 60)

    downloads = os.path.join(HOME, "Downloads")

    if not os.path.exists(downloads):
        print("Downloads folder not found.")
        return

    suggestions = []

    try:
        for filename in os.listdir(downloads):

            source = os.path.join(downloads, filename)

            if not os.path.isfile(source):
                continue

            category = organizer_category(filename)

            if category == "Other":
                continue

            suggestions.append(
                (filename, category, source)
            )

    except (PermissionError, OSError):
        print("Could not read Downloads.")
        return

    if not suggestions:
        print("\nNo files need organization.")
        return

    print(
        f"\nFound {len(suggestions)} files that could be organized.\n"
    )

    for index, (filename, category, source) in enumerate(
        suggestions[:50], 1
    ):
        print(
            f"{index}. {filename}"
        )
        print(
            f"   Suggested folder: Downloads\\{category}"
        )

    if len(suggestions) > 50:
        print("\nShowing first 50 suggestions.")

    print(
        "\n⚠️ Nothing will be moved automatically."
    )

    answer = input(
        "\nDo you want AI Laptop Manager to move these "
        "files into category folders? (yes/no): "
    ).strip().lower()

    if answer not in {"yes", "y"}:
        print("\nNo files were moved.")
        return

    moved = 0

    for filename, category, source in suggestions:

        destination_folder = os.path.join(
            downloads,
            category
        )

        try:
            os.makedirs(
                destination_folder,
                exist_ok=True
            )

            destination = os.path.join(
                destination_folder,
                filename
            )

            # Never overwrite existing files
            if os.path.exists(destination):
                continue

            shutil.move(source, destination)
            moved += 1

        except (PermissionError, OSError):
            continue

    print(f"\nMoved {moved} files.")
    print("Project folders were not touched.")


# ============================================================
# 11. CLEANUP
# ============================================================

def get_folder_size(folder):
    total = 0

    if not os.path.exists(folder):
        return 0

    for root, dirs, files in os.walk(folder):

        for filename in files:

            path = os.path.join(root, filename)

            try:
                total += os.path.getsize(path)
            except (PermissionError, OSError):
                pass

    return total


def get_recycle_bin_size():
    total = 0

    for drive in ["C:\\", "D:\\"]:

        recycle = os.path.join(
            drive,
            "$Recycle.Bin"
        )

        if not os.path.exists(recycle):
            continue

        total += get_folder_size(recycle)

    return total


def get_cleanup_info():
    temp_folder = tempfile.gettempdir()

    temp_size = get_folder_size(temp_folder)
    recycle_size = get_recycle_bin_size()

    return temp_size, recycle_size


def cleanup_temp():
    temp_folder = tempfile.gettempdir()

    removed = 0
    recovered = 0

    for root, dirs, files in os.walk(temp_folder):

        for filename in files:

            path = os.path.join(root, filename)

            try:
                size = os.path.getsize(path)

                os.remove(path)

                removed += 1
                recovered += size

            except (PermissionError, OSError):
                continue

    return removed, recovered


def empty_recycle_bin():

    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(
            None,
            None,
            0x00000007
        )

        return True

    except Exception:
        return False


def cleanup_laptop():

    print("\n" + "=" * 60)
    print("SAFE CLEANUP")
    print("=" * 60)

    temp_size, recycle_size = get_cleanup_info()

    print("\nCleanup candidates:")

    print(
        f"User temporary files : "
        f"{format_size(temp_size)}"
    )

    print(
        f"Recycle Bin          : "
        f"{format_size(recycle_size)}"
    )

    total = temp_size + recycle_size

    print(
        f"\nPotential recovery   : "
        f"{format_size(total)}"
    )

    print("\nThe following will NOT be touched:")
    print("- Downloads")
    print("- Documents")
    print("- Personal files")
    print("- Project folders")
    print("- Windows system files")
    print("- Installed programs")

    answer = input(
        "\nProceed with safe cleanup? (yes/no): "
    ).strip().lower()

    if answer not in {"yes", "y"}:
        print("\nCleanup cancelled.")
        return

    removed, recovered = cleanup_temp()

    print(
        f"\nTemporary files removed: {removed}"
    )

    print(
        f"Space recovered: {format_size(recovered)}"
    )

    if recycle_size > 0:

        if empty_recycle_bin():
            print("Recycle Bin emptied.")
        else:
            print("Could not empty Recycle Bin.")

    print("\nCleanup completed safely.")


# ============================================================
# 12. HELP
# ============================================================

def show_help():

    print("\n" + "=" * 60)
    print("AI LAPTOP MANAGER - COMMANDS")
    print("=" * 60)

    print("""
SYSTEM
------

scan
scan my laptop


STORAGE
-------

storage
check storage
how much space is left
analyze storage
show largest files
low storage


DOWNLOADS
---------

downloads
check downloads
analyze downloads
download categories


SEARCH
------

find resume
where is my resume
find my java resume
find my cloud resume
find my software resume
find certificate
find project


MOVIES
------

show my movies
find my movies
where are my movies


SMART FEATURES
---------------

find duplicates
duplicate files
check duplicate files

check suspicious files
suspicious files
security check

show old files
find old files
files older than one year

organize downloads
organize files
smart organizer


CLEANUP
-------

clean my laptop
cleanup


OTHER
-----

help
exit
""")

    print("=" * 60)
    print("IMPORTANT SAFETY")
    print("=" * 60)

    print("""
AI Laptop Manager will NOT automatically delete:

- Personal files
- Documents
- Downloads
- Project folders
- Windows system files
- Installed programs

Cleanup requires your confirmation.

The organizer also requires confirmation before moving files.
""")

    print("=" * 60)


# ============================================================
# 13. NATURAL LANGUAGE COMMAND HANDLER
# ============================================================

def handle_command(command):

    command = command.strip()

    if not command:
        return True

    lower = command.lower()

    # EXIT
    if lower in {
        "exit",
        "quit",
        "close",
        "bye"
    }:
        print("\nAI Laptop Manager closed.")
        return False

    # HELP
    if lower in {
        "help",
        "commands",
        "show commands"
    }:
        show_help()
        return True

    # CLEANUP
    if (
        lower in {"clean", "cleanup", "clean laptop"}
        or "clean my laptop" in lower
        or "clean my computer" in lower
    ):
        cleanup_laptop()
        return True

    # DUPLICATES
    if (
        "duplicate" in lower
        or "duplicates" in lower
    ):
        duplicate_finder()
        return True

    # SUSPICIOUS FILES
    if (
        "suspicious" in lower
        or "security check" in lower
        or "unsafe files" in lower
    ):
        suspicious_file_checker()
        return True

    # OLD FILES
    if (
        "old files" in lower
        or "older than one year" in lower
        or "old file" in lower
    ):
        old_file_analyzer()
        return True

    # ORGANIZER
    if (
        "organize downloads" in lower
        or "organize files" in lower
        or "smart organizer" in lower
    ):
        smart_file_organizer()
        return True

    # LOW STORAGE
    if (
        "low storage" in lower
        or "storage alert" in lower
        or "space alert" in lower
    ):
        low_storage_alert()
        return True

    # RESUME
    if (
        "resume" in lower
        or "cv" in lower
    ):
        search_resume(command)
        return True

    # MOVIES
    if (
        "movie" in lower
        or "movies" in lower
    ):
        search_movies()
        return True

    # STORAGE
    if (
        lower in {
            "storage",
            "check storage",
            "how much space is left",
            "space left",
            "free space",
            "disk space",
            "analyze storage",
            "analyse storage",
            "show largest files",
            "largest files",
            "biggest files"
        }
        or "how much space" in lower
        or "what is taking most space" in lower
        or "what takes most space" in lower
    ):
        show_storage()
        smart_storage_analyzer()
        low_storage_alert()
        return True

    # DOWNLOADS
    if (
        lower in {
            "downloads",
            "check downloads",
            "analyze downloads",
            "analyse downloads",
            "download categories",
            "categorize downloads"
        }
    ):
        analyze_downloads()
        return True

    # SCAN
    if (
        lower in {
            "scan",
            "scan laptop",
            "scan my laptop",
            "scan computer",
            "scan my computer"
        }
    ):
        scan_laptop()
        return True

    # SEARCH COMMAND
    if lower.startswith("find "):

        keyword = command[5:].strip()

        if keyword:
            search_files(keyword)

        return True

    if lower.startswith("search "):

        keyword = command[7:].strip()

        if keyword:
            search_files(keyword)

        return True

    if "where is my" in lower:

        if "resume" in lower:
            search_resume(command)

        elif "movie" in lower:
            search_movies()

        else:
            keyword = lower.replace(
                "where is my",
                ""
            ).strip()

            if keyword:
                search_files(keyword)

        return True

    # CERTIFICATE
    if "certificate" in lower:
        search_files("certificate")
        return True

    # PROJECT
    if "project" in lower:
        search_files("project")
        return True

    # NATURAL SEARCH
    if lower.startswith("locate "):

        keyword = command[7:].strip()

        if keyword:
            search_files(keyword)

        return True

    print(
        "\nI don't understand that command yet."
    )

    print(
        "Type 'help' to see available commands."
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 60)
    print("        AI LAPTOP MANAGER")
    print("=" * 60)

    print("\nYour local AI laptop assistant is ready.")
    print("Type 'help' to see all commands.")
    print("Type 'exit' to close.")

    while True:

        try:

            command = input(
                "\nYou: "
            )

            if not handle_command(command):
                break

        except KeyboardInterrupt:

            print("\n\nAI Laptop Manager closed.")
            break

        except Exception as e:

            print(
                f"\nSomething went wrong: {e}"
            )


if __name__ == "__main__":
    main()