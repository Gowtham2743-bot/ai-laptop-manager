from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pathlib import Path

app = FastAPI(title="AI Laptop Manager Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


# ---------------- STORAGE ----------------

@app.get("/storage")
def storage():
    return [
        {
            "drive": "C:/",
            "total": 512 * 1024**3,
            "used": 356 * 1024**3,
            "free": 156 * 1024**3,
            "used_percent": 69.5
        },
        {
            "drive": "D:/",
            "total": 1024 * 1024**3,
            "used": 612 * 1024**3,
            "free": 412 * 1024**3,
            "used_percent": 59.8
        }
    ]


# ---------------- FILE SEARCH ----------------

@app.get("/search")
def search(keyword: str):
    keyword = keyword.lower()

    files = [
        {
            "name": "Gowtham_Resume.pdf",
            "path": "C:/Users/Gowtham/Documents/Gowtham_Resume.pdf",
            "size": 245760,
            "type": ".pdf",
            "mtime": 1758000000
        },
        {
            "name": "Gowtham_Resume_2026.pdf",
            "path": "C:/Users/Gowtham/Documents/Resume/Gowtham_Resume_2026.pdf",
            "size": 318000,
            "type": ".pdf",
            "mtime": 1758100000
        },
        {
            "name": "Gowtham_Java_Developer_Resume.pdf",
            "path": "C:/Users/Gowtham/Documents/Resume/Gowtham_Java_Developer_Resume.pdf",
            "size": 356000,
            "type": ".pdf",
            "mtime": 1757900000
        },
        {
            "name": "Gowtham_Full_Stack_Resume.pdf",
            "path": "C:/Users/Gowtham/Documents/Resume/Gowtham_Full_Stack_Resume.pdf",
            "size": 342000,
            "type": ".pdf",
            "mtime": 1757800000
        },
        {
            "name": "Software_Engineer_Resume.pdf",
            "path": "C:/Users/Gowtham/Documents/Resume/Software_Engineer_Resume.pdf",
            "size": 298000,
            "type": ".pdf",
            "mtime": 1757700000
        },
        {
            "name": "Resume_Updated.docx",
            "path": "C:/Users/Gowtham/Documents/Resume/Resume_Updated.docx",
            "size": 186000,
            "type": ".docx",
            "mtime": 1757600000
        },
        {
            "name": "Java_Full_Stack_Certificate.pdf",
            "path": "C:/Users/Gowtham/Documents/Certificates/Java_Full_Stack_Certificate.pdf",
            "size": 524288,
            "type": ".pdf",
            "mtime": 1757000000
        },
        {
            "name": "Capgemini_Industry_Certification.pdf",
            "path": "C:/Users/Gowtham/Documents/Certificates/Capgemini_Industry_Certification.pdf",
            "size": 480000,
            "type": ".pdf",
            "mtime": 1756900000
        },
        {
            "name": "Java_Internship_Certificate.pdf",
            "path": "C:/Users/Gowtham/Documents/Certificates/Java_Internship_Certificate.pdf",
            "size": 410000,
            "type": ".pdf",
            "mtime": 1756800000
        },
        {
            "name": "AI_SEVA_Project.pdf",
            "path": "D:/Projects/AI_SEVA_Project.pdf",
            "size": 1048576,
            "type": ".pdf",
            "mtime": 1756000000
        },
        {
            "name": "Job_Application_Tracker.pdf",
            "path": "D:/Projects/Job_Application_Tracker.pdf",
            "size": 734003,
            "type": ".pdf",
            "mtime": 1756500000
        },
        {
            "name": "Leo_2023.mp4",
            "path": "D:/Movies/Leo_2023.mp4",
            "size": 2147483648,
            "type": ".mp4",
            "mtime": 1749000000
        }
    ]

    return {
        "results": [
            file for file in files
            if keyword in file["name"].lower()
            or keyword in file["path"].lower()
        ]
    }


# ---------------- RECENT FILES ----------------

@app.get("/recent")
def recent():
    return {
        "results": [
            {
                "name": "Job_Application_Tracker.pdf",
                "path": "C:/Users/Gowtham/Documents/Projects/Job_Application_Tracker.pdf",
                "size": 734003,
                "type": ".pdf",
                "mtime": 1758200000
            },
            {
                "name": "Resume_2026.pdf",
                "path": "C:/Users/Gowtham/Documents/Resume_2026.pdf",
                "size": 320000,
                "type": ".pdf",
                "mtime": 1758100000
            }
        ]
    }


# ---------------- LARGE FILES ----------------

@app.get("/large-files")
def large_files():
    return {
        "results": [
            {
                "name": "Leo_2023.mp4",
                "path": "D:/Movies/Leo_2023.mp4",
                "size": 2147483648,
                "type": ".mp4",
                "mtime": 1749000000
            },
            {
                "name": "Project_Backup.zip",
                "path": "D:/Projects/Project_Backup.zip",
                "size": 1610612736,
                "type": ".zip",
                "mtime": 1755000000
            }
        ]
    }


# ---------------- CLEANUP ----------------

@app.get("/cleanup-recommendations")
def cleanup_recommendations():
    return {
        "recommendations": [
            {
                "id": "temp",
                "name": "Temporary files",
                "size_text": "2.4 GB",
                "safe": True,
                "description": "Temporary files that can normally be cleaned."
            },
            {
                "id": "recycle",
                "name": "Recycle Bin",
                "size_text": "850 MB",
                "safe": True,
                "description": "Files currently stored in the Recycle Bin."
            }
        ]
    }


@app.post("/cleanup/temp")
def cleanup_temp():
    return {
        "success": True,
        "freed": 2576980377
    }


@app.post("/cleanup/recycle-bin")
def cleanup_recycle():
    return {
        "success": True
    }


# ---------------- ORGANIZE ----------------

@app.get("/organize-preview")
def organize_preview():
    return {
        "results": [
            {
                "name": "Resume.pdf",
                "path": "C:/Users/Gowtham/Downloads/Resume.pdf",
                "category": "Documents",
                "size_text": "420 KB"
            },
            {
                "name": "Movie.mp4",
                "path": "C:/Users/Gowtham/Downloads/Movie.mp4",
                "category": "Movies",
                "size_text": "1.8 GB"
            },
            {
                "name": "Photo.jpg",
                "path": "C:/Users/Gowtham/Downloads/Photo.jpg",
                "category": "Images",
                "size_text": "3.2 MB"
            }
        ]
    }


@app.post("/organize-downloads")
def organize_downloads():
    return {
        "success": True,
        "count": 3
    }


# ---------------- SECURITY ----------------

@app.get("/security")
def security():
    return {
        "results": [
            {
                "name": "setup.exe",
                "path": "C:/Users/Gowtham/Downloads/setup.exe",
                "size": 7340032,
                "type": ".exe"
            },
            {
                "name": "update.ps1",
                "path": "C:/Users/Gowtham/Downloads/update.ps1",
                "size": 24576,
                "type": ".ps1"
            }
        ],
        "count": 2
    }


# ---------------- DUPLICATES ----------------

@app.get("/duplicates")
def duplicates():
    return {
        "groups": [
            {
                "hash": "a7f2c9demo123",
                "count": 2,
                "wasted_text": "850 MB",
                "files": [
                    {
                        "path": "C:/Users/Gowtham/Documents/Project_Backup.zip"
                    },
                    {
                        "path": "D:/Projects/Project_Backup.zip"
                    }
                ]
            }
        ],
        "count": 1
    }


# ---------------- OLD FILES ----------------

@app.get("/old-files")
def old_files():
    return {
        "results": [
            {
                "name": "Old_Project.zip",
                "path": "D:/Projects/Old_Project.zip",
                "size": 524288000,
                "type": ".zip",
                "mtime": 1690000000
            },
            {
                "name": "Old_Resume.pdf",
                "path": "C:/Users/Gowtham/Documents/Old_Resume.pdf",
                "size": 300000,
                "type": ".pdf",
                "mtime": 1685000000
            }
        ],
        "count": 2
    }


# ---------------- FRONTEND ----------------

if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=str(FRONTEND_DIST / "assets")),
        name="assets"
    )


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIST / "index.html")


@app.get("/{path:path}")
def fallback(path: str):
    requested = FRONTEND_DIST / path

    if requested.exists() and requested.is_file():
        return FileResponse(requested)

    return FileResponse(FRONTEND_DIST / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )