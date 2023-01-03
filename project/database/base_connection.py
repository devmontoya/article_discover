from config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(settings.engine_db, echo=True)

Session = sessionmaker(engine)


def create_metadata():
    Base.metadata.create_all(engine)


class Base(DeclarativeBase):
    pass


def init_database():
    with Session() as session:
        init_statement = text(
            """ CREATE temp TABLE IF NOT EXISTS
                    article_temp_table (LIKE article_table INCLUDING ALL);

                CREATE OR REPLACE FUNCTION
                    get_rowstoupdate(websiteid integer) returns table(like article_table) AS
                    'SELECT att.* FROM article_temp_table att
                        LEFT JOIN article_table at2 ON
                        att.url = at2.url
                        WHERE at2.url is null AND att.website_id = websiteid;'
                    LANGUAGE SQL;

                CREATE OR REPLACE FUNCTION
                    get_rowstodelete(websiteid integer) returns table(like article_table) AS
                        'SELECT at2.* FROM article_temp_table att
                        RIGHT JOIN article_table at2 ON
                        att.url = at2.url
                        WHERE
                        att.url is null AND at2.website_id = websiteid;'
                    LANGUAGE SQL;
            """
        )
        session.execute(init_statement)
        session.commit()
