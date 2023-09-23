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
UPLOAD_DIR = "uploads"
# Endpoint to upload a document
@router.post("/uploadfile")
async def upload_file(id: int = Form(...), files: List[UploadFile]= Form(...)):
    # Get the current working directory
    id_directory = os.path.join("files", str(id))
    os.makedirs(id_directory, exist_ok=True)
    # Create a unique filename for the uploaded file by joining the current directory and the file name

    # Save the uploaded file to the server
    for file in files:
        file_path = os.path.join(id_directory, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    # Return a response with the link to download the file
    return {"message": "File uploaded successfully", "file_link": f"/download/{file.filename}"}


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
        file_links.append(f"/download/{id}/{file.filename}")

    return JSONResponse(content={"message": "Files uploaded successfully", "file_links": file_links})