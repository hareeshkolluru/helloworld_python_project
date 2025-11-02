from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")


class HelloResponse(BaseModel):
    """Hello endpoint response model."""

    message: str = Field(..., description="Greeting message")
    name: str | None = Field(None, description="Name from query parameter")


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str = Field(..., description="Error details")


class ImagePostResponse(BaseModel):
    """Image post response model."""

    id: str = Field(..., description="Unique image ID")
    image_url: str = Field(..., description="URL to access the image")
    caption: str | None = Field(None, description="Image caption")
    created_at: datetime = Field(..., description="Upload timestamp")
    likes: int = Field(default=0, description="Number of likes")


class ImageUploadResponse(BaseModel):
    """Image upload success response."""

    message: str = Field(..., description="Success message")
    image: ImagePostResponse = Field(..., description="Uploaded image details")

