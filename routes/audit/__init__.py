from fastapi import Request, APIRouter, UploadFile, File, Form
import os
import shutil
from services.vision_service import audit_image
from services.supabase_service import (
    get_latest_manual,
)

audit_image_route = APIRouter(prefix="/audit-image")

@audit_image_route.post("/audit-image")
async def audit_image_asset(
    brand_id: str = Form(...),
    file: UploadFile = File(...)
):

    manual = get_latest_manual(brand_id)

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = audit_image(manual, file_path)

    os.remove(file_path)

    return result