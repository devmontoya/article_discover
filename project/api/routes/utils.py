from urllib.parse import urlparse

from database.models.tables import Article
from helpers.get_article import get_text_article


async def getwrite_article_content(session, articles, new_website_id: int):
    new_articles = []
    for article in articles[:5]:
        website_id = new_website_id
        url = article["link"]
        content = await get_text_article(url)
        new_articles.append(
            Article(
                title=article["title"],
                url=url,
                published=article["published"],
                website_id=website_id,
                web_data=content,
            )
        )
    session.add_all(new_articles)
    session.flush()


def prepare_url(website_info, website_feed):
    url = website_info["link"]

    if len(url) > 50:
        return urlparse(url).netloc
    if url is None:
        return website_feed
    return url
