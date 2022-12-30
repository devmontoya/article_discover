from pydantic import BaseModel, Field


class NewWebSite(BaseModel):
    gen_id: int = Field(default=1)
    url: str = Field(max_length=100)


class WebSite_schema(BaseModel):
    id: int | None
    name: str
    url: str
    url_feed: str
    image_url: str | None


class Article_schema(BaseModel):
    id: int | None
    title: str
    url: str
    website_id: int | None
    web_data: str


class Article_schema_noid(BaseModel):
    title: str
    url: str
    website_id: int | None
    web_data: str


class Filter(BaseModel):
    column: str
    value: int | str
