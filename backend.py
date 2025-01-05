# command to run: 
# uvicorn backend:app --reload

import shutil
import uvicorn
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, Form


app = FastAPI()

# Serve the Dataset/Artist-work directory as static files
app.mount("/Dataset", StaticFiles(directory="Dataset"), name="Dataset")

@app.get("/")
async def root():
    # Serve the page.html as the home page
    return FileResponse("page.html")

# Define the dataset path
DATASET_PATH = Path("Dataset/Artist-work")
STATIC_PATH = Path("static")

# Ensure static directory exists
STATIC_PATH.mkdir(exist_ok=True)


@app.get("/artists")
def get_artists():
    if not DATASET_PATH.exists():
        return {"error": "Dataset path does not exist"}
    artist_names = [folder.name for folder in DATASET_PATH.iterdir() if folder.is_dir()]
    return {"artists": artist_names}

@app.get("/Artist-work/{artist_name}")
def get_works(artist_name: str):
    artworks_path = DATASET_PATH / artist_name
    if not artworks_path.exists():
        return {"error": "Artist not found"}
    artist_works = [img.name for img in artworks_path.iterdir() if img.is_file()]
    return {"works": artist_works}

@app.post("/upload")
async def upload_image(file: UploadFile):
    file_path = STATIC_PATH / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.post("/generate")
async def generate_image(artist: str = Form(...), work: str = Form(...), uploaded_image: str = Form(...)):
    # Placeholder for style transfer logic
    generated_image_path = STATIC_PATH / f"generated_{uploaded_image}"
    shutil.copy(STATIC_PATH / uploaded_image, generated_image_path)
    return FileResponse(generated_image_path)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


