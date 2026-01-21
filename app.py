import asyncio
from fastapi import FastAPI
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from pydantic import BaseModel
from typing import List

app = FastAPI()

class CrawlRequest(BaseModel):
    urls: List[str]

@app.post("/crawl")
async def crawl_urls(request: CrawlRequest):
    results = []
    crawler = PlaywrightCrawler(headless=True)

    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        title = await context.page.title()
        content = await context.page.text_content("body") or ""
        results.append({
            "url": context.request.url,
            "title": title,
            "content_length": len(content)
        })

    await crawler.run(request.urls)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
