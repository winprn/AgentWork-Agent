import os
import asyncio
import json
from pydantic import BaseModel, Field
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from typing import Annotated

class Item(BaseModel):
    # name: Annotated[str,"the name of the News"]
    # href: Annotated[str,"The href that link to the News"]
    # time_post:Annotated[str,"The time that news posted"]
    content:str

async def main():
    # 1. Define the LLM extraction strategy
    llm_strategy = LLMExtractionStrategy(
        provider="openai/gpt-4o",            # e.g. "ollama/llama2"
        api_token=os.getenv('OPENAI_API_KEY'),
        schema=Item.model_json_schema(),            # Or use model_json_schema()
        extraction_type="schema",
        instruction="Read and Retrieve the information, after that, summary the content of that page for me",
        chunk_token_threshold=3000,
        overlap_rate=0,
        apply_chunking=True,
        input_format="html",   # or "html", "fit_markdown"
        extra_args={"temperature": 0.0,"max_tokens": 1000}
    )

    # 2. Build the crawler config
    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        wait_for = "js:() => window.loaded === true"
        
    )

    # 3. Create a browser config if needed
    browser_cfg = BrowserConfig(headless=True)
    

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 4. Let's say we want to crawl a single page
        result = await crawler.arun(
            url="https://blog.injective.com/introducing-the-injective-x-elizaos-ai-agent-hackathon/",
            config=crawl_config
        )

        if result.success:
            # 5. The extracted content is presumably JSON
            data = json.loads(result.extracted_content)
            print("Extracted items:", data)
            # print(result.html)

            # 6. Show usage stats
            llm_strategy.show_usage()  # prints token usage
        else:
            print("Error:", result.error_message)
from playwright.sync_api import sync_playwright

# url = "https://blog.injective.com/introducing-the-injective-x-elizaos-ai-agent-hackathon/"

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)
#     page = browser.new_page()
#     page.goto(url)
#     page.wait_for_load_state("networkidle",timeout=50000)
#     # page.wait_for_timeout(100000)  # Đợi 5 giây để JavaScript load
#     html_content = page.content()
#     print(html_content)
#     browser.close()

if __name__ == "__main__":
    asyncio.run(main())
    pass