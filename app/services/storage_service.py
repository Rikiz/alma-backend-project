import aiofiles
import os
import uuid
from ..core.config import settings

async def save_resume_file(upload_file) -> str:
    # upload_file is Starlette UploadFile (async)
    ext = os.path.splitext(upload_file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(settings.UPLOAD_DIR, filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    async with aiofiles.open(dest_path, 'wb') as out_file:
        while True:
            chunk = await upload_file.read(1024 * 64)
            if not chunk:
                break
            await out_file.write(chunk)
    # Reset file pointer if needed
    try:
        await upload_file.close()
    except Exception:
        pass
    return dest_path

def delete_resume_file(file_path: str):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
