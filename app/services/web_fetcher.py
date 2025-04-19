import asyncio
import os
from typing import Dict, Any

from fastapi import HTTPException
from fetchfox_sdk import FetchFox

from app.utils.text_utils import preprocess_markdown

class WebFetcher:
    """Service class for fetching content from URLs using fetchfox."""
    
    def __init__(self):
        """Initialize the WebFetcher service."""
        self.api_key = os.getenv("FETCHFOX_API_KEY", "")
        if not self.api_key:
            print("Warning: FETCHFOX_API_KEY environment variable is not set")
        self.fox = FetchFox(api_key=self.api_key)
    
    async def fetch_content(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from the specified URL using fetchfox.
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            Dictionary containing the fetched content and metadata
        """
        try:
            # Create extraction request for fetchfox
            items = self.fox.extract(
                url,
                {
                    'title': 'What is the article title?', 
                    'description': 'What is the meta description?', 
                    'content': 'What is the full article content?'
                }
            )
            
            # Extract the first result
            result = items.limit(1)[0]
            
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No content could be extracted from the provided URL"
                )
            
            # Structure the response
            response = {
                "url": url,
                "title": result.get('title', ""),
                "description": result.get('description', ""),
                "content": result.get('content', "")
            }
            
            return response
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch content from URL: {str(e)}"
            )