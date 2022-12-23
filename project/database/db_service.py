from typing import Type

from database.base_connection import Base
from database.models.tables import Article, User, WebSite
from schemas.base import Filter
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class DbService:

    particular_model: Type[Base]

    @classmethod
    def get_all_elements(cls, session):
        statement = select(cls.particular_model)
        elements = session.scalars(statement).all()
        return elements

    @classmethod
    def get_all_elements_with_filter(cls, session, filter: Filter):
        stmt = select(cls.particular_model).where(
            getattr(cls.particular_model, filter.column) == filter.value
        )
        try:
            element = session.scalars(stmt).all()
            return element
        except NoResultFound:
            return None

    @classmethod
    def add_new_element(cls, session, new_element: Base) -> dict:
        session.add(new_element)
        return {"message": f"{new_element.__class__.__name__} added successfully"}

    @classmethod
    def get_element_by_id(cls, session, id: int):
        stmt = select(cls.particular_model).where(cls.particular_model.id == id)
        try:
            element = session.scalars(stmt).one()
            return element
        except NoResultFound:
            return None

    @classmethod
    def get_client_id_db(cls, session, chat_id: str):
        stmt = select(cls.particular_model).where(
            cls.particular_model.chat_id == chat_id
        )
        try:
            element = session.scalars(stmt).one()
            return element
        except NoResultFound:
            return None

    @classmethod
    def get_element_with_filter(cls, session, filter: Filter):
        stmt = select(cls.particular_model).where(
            getattr(cls.particular_model, filter.column) == filter.value
        )
        try:
            element = session.scalars(stmt).one()
            return element
        except NoResultFound:
            return None

    @classmethod
    def get_element_with_double_filter(
        cls, session, filter_1: Filter, filter_2: Filter
    ):
        stmt = select(cls.particular_model).where(
            (getattr(cls.particular_model, filter_1.column) == filter_1.value)
            & (getattr(cls.particular_model, filter_2.column) == filter_2.value)
        )
        try:
            element = session.scalars(stmt).one()
            return element
        except NoResultFound:
            return None


class UserDb(DbService):
    particular_model: Type[Base] = User


class WebSiteDb(DbService):
    particular_model: Type[Base] = WebSite


class ArticleDb(DbService):
    particular_model: Type[Base] = Article
