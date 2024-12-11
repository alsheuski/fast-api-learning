import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("")
def upload_image(file: UploadFile):
    img_path = f"src/static/images/{file.filename}"
    with open(img_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(img_path)
