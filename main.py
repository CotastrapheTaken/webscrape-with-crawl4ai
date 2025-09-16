import asyncio
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime

from crawl4ai import AsyncWebCrawler

URL = "https://techcrunch.com/"  # <-- replace your desired website here


def safe_name_from_url(url: str) -> str:
    u = urlparse(url)
    domain = u.netloc.replace(";", "-")
    path = u.path.strip("/").replace("/", "-") or "home"
    return f"{domain}-{path}"


async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=URL)

        md = result.markdown or ""
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")

        out_dir = Path("scrapes")
        out_dir.mkdir(parents=True, exist_ok=True)

        filename = out_dir / f"{safe_name_from_url(URL)}-{ts}.md"
        filename.write_text(md, encoding="utf-8")

        print(f"wrote {len(md)} characters to {filename.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
