from database.base_connection import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    gen_id: Mapped[int] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, genID={self.chat_id!r})"


class WebSite(Base):
    __tablename__ = "website_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(50))
    url_feed: Mapped[str] = mapped_column(String(50))

    # articles: Mapped[list["Article"]] = relationship("article_table", cascade="all, delete")
    # clients: Mapped[list["ClientChannel"]] = relationship(back_populates="channel")

    def __repr__(self) -> str:
        return f"WebSite(id={self.id!r}, name={self.name!r}, url={self.url!r}, url_feed={self.url_feed!r})"


# class ClientChannel(Base):
#     __tablename__ = "clientchannel_table"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     client_id: Mapped[int] = mapped_column(ForeignKey("client_table.id"))
#     channel_id: Mapped[int] = mapped_column(ForeignKey("channel_table.id"))
#     last_id: Mapped[int] = mapped_column(default=0)

#     client: Mapped["Client"] = relationship(back_populates="channels")
#     channel: Mapped["Channel"] = relationship(back_populates="clients")

#     def __repr__(self) -> str:
#         return f"ClientChannel(id={self.id!r}, client_id={self.client_id!r}, channel_id={self.channel_id!r}, last_id={self.client_id!r})"


class Article(Base):
    __tablename__ = "article_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(5000))
    url: Mapped[str] = mapped_column(String(5000))
    website_id: Mapped[int] = mapped_column(ForeignKey("website_table.id"))
    web_data: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Article(id={self.id!r}, title={self.title!r}, website_id={self.website_id!r})"

    def __eq__(self, other) -> bool:
        return (
            (self.title == other.title)
            and (self.url == other.url)
            and (self.website_id == other.website_id)
        )
