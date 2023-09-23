from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import shutil
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import os
from typing import List

router = APIRouter()
# Endpoint to upload a document
@router.post("/uploadfile")
async def upload_file(id: int = Form(...), files: List[UploadFile]= Form(...)):
    # Get the current working directory
    id_directory = os.path.join("files", str(id))
    os.makedirs(id_directory, exist_ok=True)
    # Create a unique filename for the uploaded file by joining the current directory and the file name

    # Save the uploaded file to the server
    file_links = []

    for file in files:
        file_path = os.path.join(id_directory, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_links.append(f"http://idxdubai.com/{id}/{file.filename}")
        
    # Return a response with the link to download the file
    return JSONResponse(content={"message": "Files uploaded successfully", "file_links": file_links})

UPLOAD_DIR = "images"
@router.post("/uploadimage")
async def upload_files(id: int = Form(...), files: List[UploadFile] = Form(...)):
    # Create a directory for the ID if it doesn't exist
    id_directory = os.path.join(UPLOAD_DIR, str(id))
    os.makedirs(id_directory, exist_ok=True)

    file_links = []

    for file in files:
        # Create a unique filename for the uploaded file within the ID's directory
        file_path = os.path.join(id_directory, file.filename)

        # Save the uploaded file to the server
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Add the file's link to the list of file links
        file_links.append(f"http://idxdubai.com/{id}/{file.filename}")

    return JSONResponse(content={"message": "Files uploaded successfully", "file_links": file_links})

@router.get("/images/{id}/{file_name}")
async def download_file(id: int, file_name: str):
    id_directory = os.path.join("images", str(id))
    file_path = os.path.join(id_directory, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        return JSONResponse(content={"message": "File not found"})

    return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})

@router.get("/files/{id}/{file_name}")
async def download_file(id: int, file_name: str):
    id_directory = os.path.join("files", str(id))
    file_path = os.path.join(id_directory, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        return JSONResponse(content={"message": "File not found"})

    return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})