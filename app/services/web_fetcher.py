import asyncio
from typing import Dict, Any

from crawl4ai import AsyncWebCrawler
from fastapi import HTTPException

from app.utils.text_utils import preprocess_markdown

class WebFetcher:
    """Service class for fetching content from URLs using crawl4ai."""
    
    def __init__(self):
        """Initialize the WebFetcher service."""
        self.last_crawl_time = 0
        self.min_delay_between_crawls = 1  # 1 second minimum delay
    
    async def fetch_content(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from the specified URL using crawl4ai.
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            Dictionary containing the fetched content and metadata
        """
        try:
            # Calculate time since last crawl and add delay if needed
            current_time = asyncio.get_event_loop().time()
            time_since_last_crawl = current_time - self.last_crawl_time
            
            if time_since_last_crawl < self.min_delay_between_crawls:
                # Add a small delay to ensure previous browser has been properly cleaned up
                await asyncio.sleep(self.min_delay_between_crawls - time_since_last_crawl)
            
            # Update the last crawl time
            self.last_crawl_time = asyncio.get_event_loop().time()
            
            # Now proceed with the crawl
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
                
                # Get markdown content
                markdown_content = result.markdown if hasattr(result, 'markdown') else ""
                
                # Preprocess the markdown content
                processed_markdown = preprocess_markdown(markdown_content)
                
                # Structure the response
                response = {
                    "url": url,
                    "title": result.title if hasattr(result, 'title') else "",
                    "markdown": markdown_content,
                    "processed_markdown": processed_markdown,
                    "html": result.html if hasattr(result, 'html') else ""
                }
                
                return response
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch content from URL: {str(e)}"
            )