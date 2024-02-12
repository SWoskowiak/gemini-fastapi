"""Main API module that contains our FastAPI routes."""
# pylint: disable=line-too-long

import os
import base64
from typing import Annotated

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from gemini import query_gemini
from gemini_queries_controller import fetch_gemini_queries, insert_gemini_query
import google_cloud
import image_util

# Our Primary FastAPI app instance
app = FastAPI()

# Mount static files to the /img path
app.mount("/img", StaticFiles(directory="img"), name="img")

@app.get("/")
async def read_index():
    """Base landing page"""
    return FileResponse("static/index.html")

@app.post("/upload/")
async def upload_image(prompt: Annotated[str, Form()], image: UploadFile = File(...)):
    """Takes an image and passes it along directly to gemini for processing"""
    response: str = await query_gemini(image, prompt)

    # If we are using cloud storage, upload the thumbnail to our bucket and capture the filename used on upload
    if os.environ.get("USE_CLOUD_STORAGE") == "True":
        thumbnail_image_bytes = image_util.make_thumbnail(image.file, (128, 128))
        cloud_filename = await google_cloud.upload_file_bytestream(thumbnail_image_bytes, image.filename)

    insert_gemini_query(original_filename=image.filename, cloud_filename=cloud_filename, prompt=prompt, response=response)
    headers = {"HX-Trigger": "newQuery"}
    return HTMLResponse(content=response, status_code=200, headers=headers)

@app.get("/query_history/")
async def get_queries():
    """Fetches the latest user queries from the database and returns them as HTML."""
    queries = fetch_gemini_queries()
    content = ""

    if not queries:
        content = "<p>No previous queries</p>"
    else:
        content = "\n".join([f"""
        <details>
            {f'<img hx-get="/thumbnails/{query.cloud_filename}" hx-swap="outerHTML" hx-trigger="load" alt="Thumbnail">' if os.environ.get("USE_CLOUD_STORAGE") == "True" else ""}
            <summary>{query.original_filename}</summary>
            <p>{query.prompt}</p>
            <em>{query.response}</em>
        </details>
""" for query in queries])
    return HTMLResponse(content=content, status_code=200)

@app.get("/thumbnails/{cloud_filename}")
async def get_thumbnail(cloud_filename: str):
    """Fetches the provided image from."""
    try:
        # Download the image from cloud storage
        image_bytes = google_cloud.download_file(cloud_filename)

        # Convert the image bytes to a data URL
        image_data_url = "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode()

        # Return the image data URL embedded in an img tag
        return HTMLResponse(content=f'<img src="{image_data_url}" alt="Thumbnail">', status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image not found") from e
