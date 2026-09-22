import os

downloads = r"C:\Users\DELL\Downloads"

extensions = {
    "Movies/Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".iso"]
}

print("MOVIES & ARCHIVES")
print("=" * 50)

for root, dirs, files in os.walk(downloads):
    for file in files:
        ext = os.path.splitext(file)[1].lower()

        for category, exts in extensions.items():
            if ext in exts:
                try:
                    path = os.path.join(root, file)
                    size = os.path.getsize(path)
                    gb = size / (1024 ** 3)

                    print(f"{category} | {gb:.2f} GB | {file}")

                except (PermissionError, FileNotFoundError, OSError):
                    pass

print("\nScan completed.")
print("Nothing was deleted or moved.")