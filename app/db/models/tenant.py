from db.meta import meta, Model
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel


# Tenant = Table(
#     "shared_tenant",
#     meta,
#     Column("id", Integer, primary_key=True),
#     Column("name", String),
#     Column("is_active", Boolean),
#     Column("expiry_date", String),
# )
