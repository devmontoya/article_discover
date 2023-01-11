from api.routes.api_general import api_general
from api.routes.api_user import api_user
from database.base_connection import Session, create_metadata, init_database
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

init_database()

tags_metadata = [
    {
        "name": "API",
        "description": "Operations with Database and API.",
    },
    {
        "name": "API_USERS",
        "description": "Operations focused on users.",
    },
    {
        "name": "WebSite",
        "description": "Endpoint to deliver the website.",
    },
]


app = FastAPI(openapi_tags=tags_metadata)

app.include_router(api_general.api_general_router, prefix="/api", tags=["API"])

app.include_router(api_user.api_user_router, prefix="/api_user", tags=["API_USERS"])


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
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
    return templates.TemplateResponse(
        "home_page.html",
        {"request": request},
    )


@app.get("/invited_user_view.html", response_class=HTMLResponse, tags=["WebSite"])
async def invited_user_view(request: Request):
    return templates.TemplateResponse("invited_user_view.html", {"request": request})


@app.post("/registered_user_view.html", response_class=HTMLResponse, tags=["WebSite"])
async def registered_user_view(request: Request):
    return templates.TemplateResponse("registered_user_view.html", {"request": request})


@app.get("/news_view.html", response_class=HTMLResponse, tags=["WebSite"])
async def news_view(request: Request):
    return templates.TemplateResponse(
        "news_view.html",
        {
            "request": request,
        },
    )
