from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from typing import List
import logging
router = APIRouter()
# Endpoint to upload a document

def list_files_in_folder(folder_path):
    file_addresses = []

    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            # Create the full file path by joining the folder path and the filename
            file_path = os.path.join(folder_path, filename)
            
            # Append the file path to the list
            file_addresses.append(f"http://idxdubai.com:8000/{file_path}")

    return file_addresses

@router.post("/uploadfile")
async def upload_file(id: int = Form(...), files: List[UploadFile]= Form(...)):
    # Get the current working directory
    id_directory = os.path.join("files", str(id))
    os.makedirs(id_directory, exist_ok=True)

    # Save the uploaded file to the server

    for file in files:
        file_path = os.path.join(id_directory, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    
    file_urls = list_files_in_folder(f"files/{id}/")     
    # Return a response with the link to download the file
    return JSONResponse(content={"message": "Files uploaded successfully", "file_links": file_urls})

UPLOAD_DIR = "images"
@router.post("/uploadimage")
async def upload_files(id: int = Form(...), files: List[UploadFile] = Form(...)):
    # Create a directory for the ID if it doesn't exist
    id_directory = os.path.join(UPLOAD_DIR, str(id))
    os.makedirs(id_directory, exist_ok=True)

    # file_links = []

    for file in files:
        # Create a unique filename for the uploaded file within the ID's directory
        file_path = os.path.join(id_directory, file.filename)

        # Save the uploaded file to the server
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
    
    file_urls = list_files_in_folder(f"images/{id}/")
    return JSONResponse(content={"message": "Files uploaded successfully", "file_links": file_urls})

@router.get("{id}/{file_name}")
async def download_file(id: int,file_name: str):
    id_directory = os.path.join("images", str(id))
    file_path = os.path.join(id_directory, file_name)
      # Log the file_path to help with debugging
    logging.info(f"File path: {file_path}")
    # Check if the file exists
    if not os.path.exists(file_path):
        return JSONResponse(content={"message": "File not found"})

    # return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})
    return FileResponse(path=file_path, filename=file_path, media_type='application/octet-stream')


@router.get("{id}/{file_name}")
async def download_file(id: int, file_name: str):
    id_directory = os.path.join("files", str(id))
    file_path = os.path.join(id_directory, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        return JSONResponse(content={"message": "File not found"})

    # return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})
    return FileResponse(path=file_path, filename=file_path, media_type='application/octet-stream')
    