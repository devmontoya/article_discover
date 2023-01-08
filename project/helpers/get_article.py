import aiohttp
from bs4 import BeautifulSoup
from readability import Document


async def get_text_article(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            doc = Document(await response.text())
            # title = doc.title()
            simple_html = doc.summary()
            soup = BeautifulSoup(simple_html, "html.parser")

            p_tags = soup.find_all("p")

            p_text = " ".join([ptag.get_text() for ptag in p_tags])

    return p_text


if __name__ == "main":
    import asyncio

    URL = "https://www.python.org/downloads/release/python-3110/"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_text_article(URL))
