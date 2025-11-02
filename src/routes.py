from datetime import datetime
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Query, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config import get_settings
from src.models import HealthResponse, HelloResponse, ImagePostResponse, ImageUploadResponse
from src.database import get_db
from src.db_models import ImagePost

router = APIRouter()
settings = get_settings()

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify the service is running.

    Returns:
        HealthResponse: Service status and metadata
    """
    return HealthResponse(status="healthy", timestamp=datetime.now(), version=settings.app_version)


@router.get("/hello", response_model=HelloResponse, tags=["Greeting"])
async def hello(
    name: str | None = Query(None, description="Optional name for personalized greeting"),
) -> HelloResponse:
    """
    Simple hello endpoint with optional name parameter.

    Args:
        name: Optional name for personalized greeting

    Returns:
        HelloResponse: Greeting message
    """
    if name:
        message = f"Hello, {name}! Welcome to {settings.app_name}."
    else:
        message = f"Hello! Welcome to {settings.app_name}."

    return HelloResponse(message=message, name=name)


@router.post("/images", response_model=ImageUploadResponse, tags=["Images"])
async def upload_image(
    file: UploadFile = File(...),
    caption: str = Form(None),
    db: AsyncSession = Depends(get_db),
) -> ImageUploadResponse:
    """
    Upload an image with optional caption.

    Args:
        file: Image file to upload
        caption: Optional caption for the image
        db: Database session

    Returns:
        ImageUploadResponse: Upload confirmation with image details
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Generate unique filename
    file_ext = Path(file.filename or "image.jpg").suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Create database entry
    db_image = ImagePost(
        id=str(uuid.uuid4()),
        filename=unique_filename,
        caption=caption,
        likes=0,
        created_at=datetime.utcnow(),
    )

    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)

    # Create response
    image_post = ImagePostResponse(
        id=db_image.id,
        image_url=f"/api/v1/images/{unique_filename}",
        caption=db_image.caption,
        created_at=db_image.created_at,
        likes=db_image.likes,
    )

    return ImageUploadResponse(message="Image uploaded successfully", image=image_post)


@router.get("/images", response_model=List[ImagePostResponse], tags=["Images"])
async def get_images(db: AsyncSession = Depends(get_db)) -> List[ImagePostResponse]:
    """
    Get all uploaded images in reverse chronological order.

    Args:
        db: Database session

    Returns:
        List[ImagePostResponse]: List of all image posts
    """
    result = await db.execute(
        select(ImagePost).order_by(ImagePost.created_at.desc())
    )
    db_images = result.scalars().all()

    return [
        ImagePostResponse(
            id=img.id,
            image_url=f"/api/v1/images/{img.filename}",
            caption=img.caption,
            created_at=img.created_at,
            likes=img.likes,
        )
        for img in db_images
    ]


@router.get("/images/{filename}", tags=["Images"])
async def get_image(filename: str) -> FileResponse:
    """
    Serve an uploaded image file.

    Args:
        filename: Name of the image file

    Returns:
        FileResponse: The image file
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path)

