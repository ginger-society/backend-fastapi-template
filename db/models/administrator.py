from __future__ import annotations

from db.meta import Model
from sqlalchemy import String, Boolean, ForeignKey, Column, Table, Enum, Integer
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from .sql_models import choice_fieldEnum
import enum


# class Tenant(Model):
#     __tablename__ = "shared_tenant"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     expiry_date: Mapped[str] = mapped_column(String(50))
#     is_active: Mapped[bool] = mapped_column(Boolean)
#     users: Mapped[list["Administrator"]] = relationship(back_populates="tenant")


# class Administrator(Model):
#     __tablename__ = "shared_administrator"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     mobile: Mapped[str] = mapped_column(String(50))
#     email: Mapped[str] = mapped_column(String(50))
#     next_password_change_due: Mapped[str] = mapped_column(String(50))
#     is_active: Mapped[bool] = mapped_column(Boolean)
#     is_staff: Mapped[bool] = mapped_column(Boolean)
#     is_admin: Mapped[bool] = mapped_column(Boolean)
#     password_change_required: Mapped[bool] = mapped_column(Boolean)
#     tenant_id: Mapped[int] = mapped_column(ForeignKey("shared_tenant.id"))
#     tenant: Mapped["Tenant"] = relationship(back_populates="users")


# association_table = Table(
#     "shared_many2manytest_testModels",
#     Model.metadata,
#     Column("many2manytest_id", ForeignKey("shared_many2manytest.id"), primary_key=True),
#     Column("test_id", ForeignKey("shared_test.id"), primary_key=True),
# )
# association_table2 = Table(
#     "shared_many2manytest_crossAppModel",
#     Model.metadata,
#     Column("many2manytest_id", ForeignKey("shared_many2manytest.id"), primary_key=True),
#     Column(
#         "testappmodel1_id", ForeignKey("testApp_testappmodel1.id"), primary_key=True
#     ),
# )


# class Many2ManyTest(Model):
#     __tablename__ = "shared_many2manytest"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     testModels: Mapped[list["Test"]] = relationship(
#         secondary=association_table, back_populates="main_models"
#     )
#     crossAppModel: Mapped[list["TestAppModel1"]] = relationship(
#         secondary=association_table2, back_populates="cross_app_m2mtest"
#     )


# class CHOICES(enum.Enum):
#     choice1 = "choice1"
#     choice2 = "choice2"
#     choice3 = "choice3"


# class TestAppModel1(Model):
#     __tablename__ = "testApp_testappmodel1"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     char_field: Mapped[str] = mapped_column(String(50))
#     cross_app_m2mtest: Mapped[list["Many2ManyTest"]] = relationship(
#         back_populates="crossAppModel", secondary=association_table2
#     )


# class Test(Model):
#     __tablename__ = "shared_test"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     choice_field: Mapped[str] = mapped_column(Enum(CHOICES))
#     bool_field: Mapped[bool] = mapped_column()
#     char_field: Mapped[str] = mapped_column(String(50))
#     field3: Mapped[bool] = mapped_column()
#     main_models: Mapped[list["Many2ManyTest"]] = relationship(
#         back_populates="testModels", secondary=association_table
#     )


class Many2ManyTestT(BaseModel):
    id: int
    name: str
    testModels: list["TestT"]
    crossAppModel: list["TestAppModel1T"]

    class Config:
        orm_mode = True


class TestAppModel1T(BaseModel):
    id: int
    char_field: str

    class Config:
        orm_mode = True


class TestT(BaseModel):
    id: int
    choice_field: choice_fieldEnum
    bool_field: bool
    char_field: str
    field3: bool

    class Config:
        orm_mode = True


class AdministratorT(BaseModel):
    id: int
    name: str
    email: str
    mobile: Optional[str]
    is_active: bool
    is_admin: bool
    is_staff: bool
    password_change_required: bool
    next_password_change_due: Optional[str]
    tenant: Optional["TenantT"]

    class Config:
        orm_mode = True


class AdministratorSimplestT(BaseModel):
    id: int
    name: str
    email: str
    mobile: Optional[str]
    is_active: bool
    is_admin: bool
    is_staff: bool
    password_change_required: bool
    next_password_change_due: Optional[str]

    class Config:
        orm_mode = True


class AdministratorSimpleT(BaseModel):
    id: int
    name: str
    email: str
    mobile: Optional[str]
    is_active: bool
    is_admin: bool
    is_staff: bool
    password_change_required: bool
    next_password_change_due: Optional[str]
    tenant: Optional["TenantSimpleT"]

    class Config:
        orm_mode = True


class TenantT(BaseModel):
    id: int
    name: str
    is_active: bool
    expiry_date: Optional[str]
    users: list["AdministratorT"]


class TenantSimpleT(BaseModel):
    id: int
    name: str
    is_active: bool
    expiry_date: Optional[str]

    class Config:
        orm_mode = True


TenantT.update_forward_refs()
AdministratorT.update_forward_refs()
AdministratorSimpleT.update_forward_refs()
Many2ManyTestT.update_forward_refs()
