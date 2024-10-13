from fastapi import FastAPI, File, UploadFile, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
import shutil
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from googly.process_image import Model
import numpy as np
import cv2
import io
import base64
import re
import schemas
from .config import settings, setup_app_logging
from fastapi.middleware.cors import CORSMiddleware


setup_app_logging(config=settings)

app = FastAPI( title=settings.PROJECT_NAME)
root_router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Folder to save uploaded files
UPLOAD_FOLDER = "uploads"
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

model = Model()

@root_router.get("/", response_class=HTMLResponse)
async def main():
    # Serve the HTML file to upload images
    with open("templates/image.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@root_router.post("/upload-canvas-image", response_model=schemas.PredictionResults, status_code=200)
async def upload_image(image: str = Form(...)): 
    """
        This function gets the request from the client, passes it to get the modified image and returns the output
    """
    # Extract base64 image data
    image_data = re.sub('^data:image/.+;base64,', '', image)
    
    # Decode the base64 string to bytes
    img_bytes = base64.b64decode(image_data)
    
    # Convert bytes data to a numpy array
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    
    # Decode the image using OpenCV
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    output_image = model.get_output(img)

    _, buffer = cv2.imencode(".png", output_image)
    io_buf = base64.b64encode(buffer).decode('utf-8')
    image_url = f"data:image/png;base64,{io_buf}"

    return {"image_url": image_url}

app.include_router(root_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    # logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run(app, host="localhost", port=3000, log_level="info")

