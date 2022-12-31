# from config import settings
from api.routes import api
from database.base_connection import Session, create_metadata
from database.db_service import ArticleDb, WebSiteDb
from database.models.tables import WebSite
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas.base import Filter
from sqlalchemy import select

create_metadata()

tags_metadata = [
    {
        "name": "API",
        "description": "Operations with Database and API.",
    },
    {
        "name": "WebSite",
        "description": "Endpoint to deliver the website",
    },
]


app = FastAPI(openapi_tags=tags_metadata)

app.include_router(api.api_router, prefix="/api", tags=["API"])

origins = [
    "http://localhost",
    "http://localhost:8000" "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
def healthcheck():
    return True


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, tags=["WebSite"])
async def home(request: Request):
    num = 2
    with Session() as session:
        website_list = session.scalars(select(WebSite)).all()
        website = WebSiteDb.get_element_with_filter(
            session, Filter(column="id", value=num)
        )
        if website is not None:
            articles = ArticleDb.get_all_elements_with_filter(
                session, Filter(column="website_id", value=website.id)
            )
            lista = articles
        else:
            lista = []
    return templates.TemplateResponse(
        "invited_user_view.html",
        {"request": request, "num": num, "website_list": website_list, "lista": lista},
    )


@app.get("/news_view.html", response_class=HTMLResponse, tags=["WebSite"])
async def news_view(request: Request):
    return templates.TemplateResponse(
        "news_view.html",
        {
            "request": request,
        },
    )
