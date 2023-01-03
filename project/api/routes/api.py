from database.base_connection import Session
from database.db_service import WebSiteDb
from database.models.tables import Article, WebSite
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from helpers.get_article import get_text_article
from helpers.get_urls_rss import get_news_rss
from schemas.base import Article_schema_noid, Filter, NewWebSite
from sqlalchemy import select, text

api_router = APIRouter()


@api_router.post("/get_news_website")
def get_news_website(website: NewWebSite):
    news = get_news_rss(website.url)
    return news


@api_router.post("/new_website")
async def pass_website(website: NewWebSite):
    website_info = get_news_rss(website.url)
    title_feed = website_info["title_feed"]
    with Session() as session:
        if (
            WebSiteDb.get_element_with_filter(
                session, Filter(column="name", value=title_feed)
            )
            is None
        ):
            new_website = WebSite(
                name=title_feed,
                url=website_info["link"],
                url_feed=website.url,
                image_url=website_info["image_url"],
            )
            session.add(new_website)
            session.flush()
            new_articles = []
            news = get_news_rss(website.url)["entries"]
            for new in news[:5]:
                website_id = new_website.id
                url = new["link"]
                content = await get_text_article(url)
                new_articles.append(
                    Article(
                        title=new["title"],
                        url=new["link"],
                        website_id=new_website.id,
                        web_data=content,
                    )
                )
            print(new_articles)
            session.add_all(new_articles)
            session.flush()
        session.commit()
    return news


@api_router.get("/get_websites_list")
async def get_websites_list():
    with Session() as session:
        websites = session.scalars(select(WebSite)).all()
    return websites


@api_router.get("/get_news_list/{website_id}")
async def get_news_list(website_id: int):
    with Session() as session:
        website = WebSiteDb.get_element_by_id(session, website_id)
        articles = website.articles
    return [
        {
            "Title": art.title,
            "url": art.url,
            "published": art.published,
            "data": art.web_data,
        }
        for art in articles
    ]


@api_router.post("/update_sites")
async def update_sites():
    with Session() as session:
        websites = session.scalars(select(WebSite)).all()
        print(websites)
        for web in websites:
            result = []
            news = get_news_rss(web.url_feed)["entries"]
            for new in news[:5]:
                website_id = web.id
                url = new["link"]
                content = await get_text_article(url)
                result.append(
                    Article_schema_noid(
                        title=new["title"],
                        url=url,
                        published=new["published"],
                        website_id=website_id,
                        web_data=content,
                    ).dict()
                )

            update_articles(result, website_id=website_id)
    return "True"


@api_router.post("/tests/add_news")
def add_news(inicio: int):
    new_articles = [
        Article_schema_noid(
            title=f"titulo numero {i}",
            url=f"url numero {i}",
            website_id=100,
            web_data=f"text numero {i}",
        ).dict()
        for i in range(inicio, inicio + 10)
    ]
    print(new_articles)
    update_articles(new_articles, website_id=100)
    return new_articles


def get_new_news(new_articles):
    with Session() as session:
        session.execute(text("DROP FROM article_temp_table;"))
        session.execute(
            text(
                """INSERT INTO article_temp_table (title, url, published, website_id, web_data)
                VALUES(:title, :url, :published, :website_id, :web_data)"""
            )
        )


def update_articles(new_articles, website_id):
    with Session() as session:

        session.execute(
            text(
                """CREATE temp TABLE IF NOT EXISTS
                article_temp_table (LIKE article_table INCLUDING ALL);"""
            )
        )

        statement_insert = text(
            """INSERT INTO article_temp_table (title, url, published, website_id, web_data)
                VALUES(:title, :url, :published, :website_id, :web_data)"""
        )

        for new_art in new_articles:
            session.execute(statement_insert, new_art)

        statement_updates = text(
            """delete
                    from
                    	article_table
                    where
                    	id in (
                    	    select id
                            from get_rowstodelete(:website_id));
                insert
                	into
                	article_table (
                	select
                		*
                	from
                		get_rowstoupdate(:website_id));"""
        )

        session.execute(statement_updates, {"website_id": website_id})

        session.execute(text("DROP TABLE IF EXISTS article_temp_table;"))
        session.commit()
        return True
