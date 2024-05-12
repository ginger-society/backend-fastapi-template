import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


meta = sa.MetaData()


class Model(DeclarativeBase):
    pass
