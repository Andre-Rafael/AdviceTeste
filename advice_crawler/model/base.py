from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    "sqlite:///tjmg.db", echo=True, connect_args={"autocommit": False}
)
Base = declarative_base()
Base.metadata.create_all(engine)