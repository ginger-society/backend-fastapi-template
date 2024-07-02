from db.meta import meta
from sqlalchemy import Table, Column, Integer, String, Boolean
from pydantic import BaseModel


Note = Table(
    "notes",
    meta,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("completed", Boolean),
)


class NoteT(BaseModel):
    id: int
    text: str
    completed: bool
