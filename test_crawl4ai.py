import asyncio
from crawl4ai import *

async def main():
    # Add a small delay before creating a new crawler instance
    # This helps prevent the "Target page, context or browser has been closed" error
    # when running the script multiple times in succession
    await asyncio.sleep(1)
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://vnexpress.net/hon-10-000-nguoi-lan-dau-hop-luyen-o-duong-le-duan-4875887.html",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
