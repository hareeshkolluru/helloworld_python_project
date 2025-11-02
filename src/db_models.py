from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from src.database import Base


class ImagePost(Base):
    """Database model for image posts."""
    
    __tablename__ = "image_posts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536),  # OpenAI embedding dimension
        nullable=True
    )

    def to_response(self) -> dict:
        """Convert database model to API response format."""
        return {
            "id": self.id,
            "image_url": f"/api/v1/images/{self.filename}",
            "caption": self.caption,
            "created_at": self.created_at.isoformat(),
            "likes": self.likes,
        }
