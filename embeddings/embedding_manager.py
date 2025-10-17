"""Embedding manager for OpenAI embeddings API."""
import numpy as np
from typing import List, Union
from openai import OpenAI
import config


class EmbeddingManager:
    """Manages embedding generation using OpenAI API."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize embedding manager.
        
        Args:
            api_key: OpenAI API key (defaults to config)
            model: Embedding model name (defaults to config)
        """
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model or config.OPENAI_EMBEDDING_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY in .env file")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def create_embedding(self, text: str) -> np.ndarray:
        """Create embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            embedding = response.data[0].embedding
            return np.array(embedding)
            
        except Exception as e:
            print(f"[!] Error creating embedding: {e}")
            raise
    
    def create_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[np.ndarray]:
        """Create embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process per API call
            
        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                
                # Extract embeddings in the same order
                batch_embeddings = [np.array(item.embedding) for item in response.data]
                all_embeddings.extend(batch_embeddings)
                
                print(f"[+] Processed {len(all_embeddings)}/{len(texts)} embeddings")
                
            except Exception as e:
                print(f"[!] Error in batch {i//batch_size + 1}: {e}")
                # Return what we have so far
                break
        
        return all_embeddings
    
    def embed_user_query(self, query: str) -> np.ndarray:
        """Create embedding for user query or preference.
        
        Args:
            query: User query text
            
        Returns:
            Query embedding vector
        """
        return self.create_embedding(query)
    
    def embed_movie(self, movie_description: str) -> np.ndarray:
        """Create embedding for movie description.
        
        Args:
            movie_description: Movie description text
            
        Returns:
            Movie embedding vector
        """
        return self.create_embedding(movie_description)

