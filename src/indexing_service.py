"""Service for indexing images using LlamaIndex and storing embeddings in PostgreSQL."""
import os
from pathlib import Path
from typing import List

from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core.schema import ImageDocument

from src.config import get_settings

settings = get_settings()


class ImageIndexingService:
    """Service for generating and managing image embeddings."""

    def __init__(self):
        """Initialize the indexing service with OpenAI embeddings."""
        # Initialize OpenAI embedding model
        self.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=settings.openai_api_key,
        )
        
        # Initialize multimodal LLM for image understanding
        self.mm_llm = OpenAIMultiModal(
            model="gpt-4o-mini",
            api_key=settings.openai_api_key,
            max_new_tokens=300,
        )

    async def generate_image_embedding(self, image_path: str) -> List[float]:
        """
        Generate embedding vector for an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of floats representing the embedding vector
        """
        # Read the image
        image_documents = SimpleDirectoryReader(
            input_files=[image_path]
        ).load_data()
        
        if not image_documents:
            raise ValueError(f"Could not load image from {image_path}")
        
        image_doc = image_documents[0]
        
        # Generate description using multimodal LLM
        response = await self.mm_llm.acomplete(
            prompt="Describe this image in detail, including objects, colors, mood, and context.",
            image_documents=[image_doc],
        )
        
        description = str(response)
        
        # Generate embedding from the description
        embedding = await self.embed_model.aget_text_embedding(description)
        
        return embedding

    async def generate_caption_from_image(self, image_path: str) -> str:
        """
        Generate a caption for an image using multimodal LLM.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Generated caption string
        """
        # Read the image
        image_documents = SimpleDirectoryReader(
            input_files=[image_path]
        ).load_data()
        
        if not image_documents:
            raise ValueError(f"Could not load image from {image_path}")
        
        image_doc = image_documents[0]
        
        # Generate caption
        response = await self.mm_llm.acomplete(
            prompt="Generate a brief, engaging caption for this image (max 2 sentences).",
            image_documents=[image_doc],
        )
        
        return str(response).strip()


# Singleton instance
_indexing_service: ImageIndexingService | None = None


def get_indexing_service() -> ImageIndexingService:
    """Get or create the indexing service singleton."""
    global _indexing_service
    if _indexing_service is None:
        _indexing_service = ImageIndexingService()
    return _indexing_service
