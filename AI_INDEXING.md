# AI-Powered Image Indexing with LlamaIndex

## Overview

This application now includes intelligent image indexing using LlamaIndex and OpenAI, storing vector embeddings in PostgreSQL with pgvector extension.

## Architecture

### Components

1. **LlamaIndex** - Framework for connecting LLMs with your data
2. **OpenAI GPT-4o-mini** - Multimodal model for understanding images
3. **OpenAI text-embedding-3-small** - Generates 1536-dimension embeddings
4. **pgvector** - PostgreSQL extension for vector similarity search
5. **SQLAlchemy** - ORM with native pgvector support

### Data Flow

```
Image Upload → LlamaIndex Processing → Embedding Generation → PostgreSQL Storage
     ↓              ↓                        ↓                      ↓
  Save File    Analyze Image          Create Vector         Store in pgvector
                    ↓                        
              Generate Caption         
```

## Implementation Details

### 1. Database Schema (`src/db_models.py`)

Added an embedding column to the `ImagePost` model:

```python
from pgvector.sqlalchemy import Vector

class ImagePost(Base):
    # ... other fields ...
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536),  # OpenAI embedding dimension
        nullable=True
    )
```

### 2. Indexing Service (`src/indexing_service.py`)

Created a dedicated service for image processing:

**Key Functions:**
- `generate_image_embedding(image_path)` - Creates vector embedding from image
- `generate_caption_from_image(image_path)` - Auto-generates caption

**Process:**
1. Load image using LlamaIndex `SimpleDirectoryReader`
2. Pass image to GPT-4o-mini multimodal model
3. Generate detailed description of image content
4. Convert description to 1536-dimension embedding vector
5. Return embedding for storage

### 3. Upload Integration (`src/routes.py`)

Modified the `/api/v1/images` POST endpoint to:

```python
# After saving the image file:
embedding = None
try:
    indexing_service = get_indexing_service()
    embedding = await indexing_service.generate_image_embedding(str(file_path))
    
    # Optionally generate caption if none provided
    if not caption:
        caption = await indexing_service.generate_caption_from_image(str(file_path))
except Exception as e:
    # Log error but continue - embedding is optional
    print(f"Warning: Failed to generate embedding: {str(e)}")

# Store with embedding
db_image = ImagePost(..., embedding=embedding)
```

### 4. Database Configuration (`src/database.py`)

Added pgvector extension initialization:

```python
async def init_db() -> None:
    """Initialize database tables and enable pgvector extension."""
    async with engine.begin() as conn:
        # Enable pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
```

## Configuration

### Required Environment Variables

Add to your `.env` file:

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### Optional Configuration

The system gracefully handles missing API keys - images will upload successfully but without embeddings or auto-generated captions.

## Features Enabled

### 1. Automatic Embedding Generation
- Every uploaded image gets a semantic vector representation
- 1536-dimension vector stored in PostgreSQL with pgvector
- Enables similarity searches and recommendations

### 2. Automatic Caption Generation
- If you don't provide a caption, GPT-4o-mini generates one
- Creates engaging, descriptive captions automatically
- Uses multimodal understanding of image content

### 3. Semantic Search (Future Enhancement)
With embeddings stored, you can easily add:
- **Find similar images**: Compare vectors using cosine similarity
- **Search by description**: "Find images with sunsets"
- **Content recommendations**: Suggest related images

## Future Enhancements

### Add Vector Search Endpoint

```python
@router.post("/images/search", response_model=List[ImagePostResponse])
async def search_similar_images(
    query: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """Search images by semantic similarity to query."""
    indexing_service = get_indexing_service()
    
    # Generate embedding for search query
    query_embedding = await indexing_service.embed_model.aget_text_embedding(query)
    
    # Use pgvector to find similar images
    result = await db.execute(
        select(ImagePost)
        .order_by(ImagePost.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    
    return [img.to_response() for img in result.scalars().all()]
```

### Add Image-to-Image Search

```python
@router.post("/images/{image_id}/similar")
async def find_similar_images(image_id: str, limit: int = 5):
    """Find images similar to a given image."""
    # Get the source image's embedding
    # Query pgvector for nearest neighbors
    # Return similar images
```

## Performance Considerations

### Embedding Generation Time
- Takes ~2-5 seconds per image (depends on OpenAI API)
- Runs asynchronously to not block upload
- Consider adding a background job queue for production

### Storage
- Each embedding: ~6KB (1536 floats × 4 bytes)
- Indexed for fast similarity search
- PostgreSQL handles millions of vectors efficiently

### Optimization Tips
1. **Batch Processing**: Process multiple images in parallel
2. **Caching**: Cache embeddings for duplicate images
3. **Background Jobs**: Use Celery or similar for async processing
4. **Rate Limiting**: Respect OpenAI API rate limits

## Testing

### Test Embedding Generation

```python
import asyncio
from src.indexing_service import get_indexing_service

async def test_embedding():
    service = get_indexing_service()
    embedding = await service.generate_image_embedding("path/to/image.jpg")
    print(f"Generated embedding with {len(embedding)} dimensions")

asyncio.run(test_embedding())
```

### Test Caption Generation

```python
async def test_caption():
    service = get_indexing_service()
    caption = await service.generate_caption_from_image("path/to/image.jpg")
    print(f"Generated caption: {caption}")
```

## Troubleshooting

### Error: "pgvector extension not found"
- Ensure PostgreSQL has pgvector installed
- Docker image `postgres:16-alpine` may need pgvector added
- Consider using `ankane/pgvector` Docker image

### Error: "OpenAI API key not set"
- Add `OPENAI_API_KEY` to your `.env` file
- Verify the key is valid at https://platform.openai.com

### Slow Upload Times
- Embedding generation adds 2-5 seconds to uploads
- Consider moving to background processing
- Or make embedding optional with a flag

### Rate Limiting
- OpenAI has rate limits on API usage
- Add retry logic with exponential backoff
- Consider caching for duplicate images

## Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [OpenAI Platform](https://platform.openai.com/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

## Cost Considerations

### OpenAI API Costs (as of 2024)

- **GPT-4o-mini**: ~$0.000015 per image (for description)
- **text-embedding-3-small**: ~$0.00002 per image
- **Total per image**: ~$0.000035

For 1,000 images: ~$0.035
For 10,000 images: ~$0.35
For 100,000 images: ~$3.50

Very cost-effective for most applications!
