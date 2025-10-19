from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid
import mimetypes

photo_router = APIRouter(prefix="/photos", tags=["Photo Management"])

base = os.path.dirname(os.path.abspath(__file__))
photos_dir = os.path.join(base, "photos")
os.makedirs(photos_dir, exist_ok=True)


class PhotoUploadResponse(BaseModel):
    identifier: str
    url: str

@photo_router.get("/all")
async def get_all_photos():
    entries = []
    for fname in os.listdir(photos_dir):
        file_path = os.path.join(photos_dir, fname)
        if os.path.isfile(file_path):
            try:
                ctime = os.path.getctime(file_path)
            except Exception:
                ctime = 0
            identifier = fname.split('.')[0]
            url = f"/photos/{identifier}"
            entries.append({"identifier": identifier, "url": url, "created": ctime})

    # sort by creation time (latest first)
    entries.sort(key=lambda e: e.get("created", 0), reverse=True)

    # strip creation timestamp from response (if you want timestamps included, keep them)
    photos = [{"identifier": e["identifier"], "url": e["url"]} for e in entries]
    return photos


@photo_router.post("/upload", response_model=PhotoUploadResponse)
async def upload_photo(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    if not ext:
        ext = mimetypes.guess_extension(file.content_type or "") or ""

    identifier = uuid.uuid4().hex
    filename = identifier + ext
    file_path = os.path.join(photos_dir, filename)

    # save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    url = f"/photos/{identifier}"
    return PhotoUploadResponse(identifier=identifier, url=url)


@photo_router.get("/{identifier}")
async def get_photo(identifier: str):
    for fname in os.listdir(photos_dir):
        if fname.startswith(identifier):
            file_path = os.path.join(photos_dir, fname)
            if os.path.isfile(file_path):
                media_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                return FileResponse(file_path, media_type=media_type)

    raise HTTPException(status_code=404, detail="Photo not found")
    