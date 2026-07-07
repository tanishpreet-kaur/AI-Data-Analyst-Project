from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_uploaded_database(uploaded_file):
    destination = UPLOAD_DIR / uploaded_file.name

    with open(destination, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)

    return destination