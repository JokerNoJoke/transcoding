import os
import shutil
import uuid
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.utils.ffmpeg_client import transcoding_video_to_dash
from app.utils.minio_client import fput_object

router = APIRouter(prefix="/os", tags=["Object Storage"])


@router.post("/")
async def put(file: Annotated[UploadFile, File()]):
    return {
        "size": file.size,
        "content_type": file.content_type,
    }


@router.post("/mp4")
async def put(file: Annotated[UploadFile, File()]):
    # Verify file is MP4
    if not file.content_type == "video/mp4":
        raise HTTPException(status_code=400, detail="Only MP4 files are allowed")

    output_dir = None
    try:
        # Generate unique directory name using UUID
        unique_dir = str(uuid.uuid4()).replace("-", "")
        output_dir = os.path.join("temp", unique_dir)
        os.makedirs(output_dir, exist_ok=True)

        # Save uploaded file with original filename
        input_file = os.path.join(output_dir, file.filename)

        # Replace async with for regular file write
        with open(input_file, "wb") as buffer:
            buffer.write(await file.read())

        # Convert video to DASH format
        transcoding_video_to_dash(input_file, output_dir)

        # Upload to MinIO
        fput_object(os.path.join("videos", unique_dir), output_dir)

        return {
            "message": "Video converted successfully",
            "manifest_url": f"videos/{unique_dir}/manifest.mpd",
        }

    except Exception as e:
        # Log the error here if needed
        raise HTTPException(
            status_code=500, detail=f"Video processing failed: {str(e)}"
        )
    finally:
        # Clean up temp files
        if output_dir and os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
            except Exception:
                # Log cleanup errors but don't fail
                print(f"Failed to cleanup directory {output_dir}")
