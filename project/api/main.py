# from config import settings
from database.base_connection import Session, create_metadata
from database.db_service import ArticleDb, UserDb, WebSite, WebSiteDb
from database.models.tables import Article, User, WebSite
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from helpers.get_article import get_text_article
from helpers.get_urls_rss import get_news_rss
from schemas.base import Article_schema_noid, Filter, NewWebSite, WebSite_schema
from sqlalchemy import select, text

create_metadata()

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return True


@app.post("/web_site/get_news_website")
def get_news_website(website: NewWebSite):
    news = get_news_rss(website.url)
    return news


@app.post("/web_site/new_website")
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
                name=title_feed, url=website_info["link"], url_feed=website.url
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


@app.get("/web_site/get_websites_list")
async def get_websites_list():
    with Session() as session:
        websites = session.scalars(select(WebSite)).all()
    return websites


@app.post("/web_site/update_sites")
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
                        website_id=website_id,
                        web_data=content,
                    ).dict()
                )

            update_articles(result, website_id=website_id)
    return "True"


@app.post("/tests/add_news")
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
        session.execute(text(
            "CREATE temp TABLE IF NOT EXISTS article_temp_table (LIKE article_table INCLUDING ALL);"))
        session.execute(text(
            """INSERT INTO article_temp_table (title, url, website_id, web_data) VALUES(:title, :url, :website_id, :web_data)"""
        ))


def update_articles(new_articles, website_id):
    with Session() as session:

        statement_temp_table = text(
            "CREATE temp TABLE article_temp_table (LIKE article_table INCLUDING ALL);"
        )
        session.execute(statement_temp_table)

        statement_insert = text(
            """INSERT INTO article_temp_table (title, url, website_id, web_data) VALUES(:title, :url, :website_id, :web_data)"""
        )

        for new_art in new_articles:
            session.execute(statement_insert, new_art)

        statement_updates = text(
            """delete
                                        from
                                        	article_table
                                        where
                                        	id in (
                                        	select at2.id from article_temp_table att
                                        	right join article_table at2 on
                                        		att.url = at2.url
                                        	where
                                        		att.url is null and at2.website_id = :website_id);
                                    insert
                                    	into
                                    	article_table (
                                    	select
                                    		att.*
                                    	from
                                    		article_temp_table att
                                    	left join article_table at2 on
                                    		att.url = at2.url
                                    	where
                                    		at2.url is null  and att.website_id = :website_id);"""
        )

        session.execute(statement_updates, {"website_id": website_id})

        session.execute(text("DROP TABLE IF EXISTS article_temp_table;"))
        session.commit()
        return True


from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("news_list.html", {
        "request": request,
        "lista": []
    })

@app.post("/", response_class=HTMLResponse)
async def home(request: Request, num :int = Form(...)):
    with Session() as session:
        website_list = session.scalars(select(WebSite)).all()
        website = WebSiteDb.get_element_with_filter(
            session, Filter(column="id", value=num)
            )
        if (website is not None):
            articles = ArticleDb.get_all_elements_with_filter(session, Filter(column="website_id", value=website.id))
            lista = articles
        else:
            lista= []
    return templates.TemplateResponse("news_list.html", {
        "request": request,
        "num": num,
        "website_list": website_list,
        "lista":lista
    })