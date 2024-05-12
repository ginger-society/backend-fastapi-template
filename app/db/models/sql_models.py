from __future__ import annotations

from db.meta import Model
from sqlalchemy import String, Boolean, ForeignKey, Column, Table, Enum, Integer, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import enum


Group_Permission = Table(
    "auth_group_permissions",
    Model.metadata,
    Column("group_id", ForeignKey("auth_group.id"), primary_key=True),
    Column("permission_id", ForeignKey("auth_permission.id"), primary_key=True),
)

Many2ManyTest_Test = Table(
    "shared_many2manytest_testModels",
    Model.metadata,
    Column("many2manytest_id", ForeignKey("shared_many2manytest.id"), primary_key=True),
    Column("test_id", ForeignKey("shared_test.id"), primary_key=True),
)

Many2ManyTest_TestAppModel1 = Table(
    "shared_many2manytest_crossAppModel",
    Model.metadata,
    Column("many2manytest_id", ForeignKey("shared_many2manytest.id"), primary_key=True),
    Column("testappmodel1_id", ForeignKey("testApp_testappmodel1.id"), primary_key=True),
)




class action_flagEnum(enum.Enum):

    
    _1 = "Addition"
    _2 = "Change"
    _3 = "Deletion"



class choice_fieldEnum(enum.Enum):

    choice1 = "choice1"
    choice2 = "choice2"
    choice3 = "choice3"
    




class LogEntry(Model):
    __tablename__ = "django_admin_log"
    action_time: Mapped[str] = mapped_column(DateTime)
    user: Mapped["Administrator"] = relationship(back_populates="logentry_set")
    user_id: Mapped[int] = mapped_column(ForeignKey("shared_administrator.id"))
    content_type: Mapped["ContentType"] = relationship(back_populates="logentry_set")
    content_type_id: Mapped[int] = mapped_column(ForeignKey("django_content_type.id"))
    object_id: Mapped[str] = mapped_column(String)
    object_repr: Mapped[str] = mapped_column(String(200))
    action_flag: Mapped[int] = mapped_column(Enum(action_flagEnum))
    change_message: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)


class Group(Model):
    __tablename__ = "auth_group"
    name: Mapped[str] = mapped_column(String(150))
    permissions: Mapped[list["Permission"]] = relationship(back_populates="group_set",secondary=Group_Permission)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)


class Session(Model):
    __tablename__ = "django_session"
    session_key: Mapped[str] = mapped_column(String,primary_key=True)
    session_data: Mapped[str] = mapped_column(String)
    expire_date: Mapped[str] = mapped_column(DateTime)


class Tenant(Model):
    __tablename__ = "shared_tenant"
    name: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(Boolean)
    expiry_date: Mapped[str] = mapped_column(Date)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    users: Mapped[list["Administrator"]] = relationship(back_populates="tenant")


class Administrator(Model):
    __tablename__ = "shared_administrator"
    name: Mapped[str] = mapped_column(String(200))
    mobile: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    tenant: Mapped["Tenant"] = relationship(back_populates="users")
    tenant_id: Mapped[int] = mapped_column(ForeignKey("shared_tenant.id"))
    is_active: Mapped[bool] = mapped_column(Boolean)
    is_staff: Mapped[bool] = mapped_column(Boolean)
    is_admin: Mapped[bool] = mapped_column(Boolean)
    password_change_required: Mapped[bool] = mapped_column(Boolean)
    next_password_change_due: Mapped[str] = mapped_column(Date)
    password: Mapped[str] = mapped_column(String(128))
    last_login: Mapped[str] = mapped_column(DateTime)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    logentry_set: Mapped[list["LogEntry"]] = relationship(back_populates="user")


class Test(Model):
    __tablename__ = "shared_test"
    choice_field: Mapped[str] = mapped_column(Enum(choice_fieldEnum))
    bool_field: Mapped[bool] = mapped_column(Boolean)
    char_field: Mapped[str] = mapped_column(String(50))
    positive_integer_field: Mapped[int] = mapped_column(Integer)
    field3: Mapped[bool] = mapped_column(Boolean)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    main_models: Mapped[list["Many2ManyTest"]] = relationship(back_populates="testModels",secondary=Many2ManyTest_Test)


class Many2ManyTest(Model):
    __tablename__ = "shared_many2manytest"
    name: Mapped[str] = mapped_column(String(200))
    testModels: Mapped[list["Test"]] = relationship(back_populates="main_models",secondary=Many2ManyTest_Test)
    crossAppModel: Mapped[list["TestAppModel1"]] = relationship(back_populates="cross_app_m2mtest",secondary=Many2ManyTest_TestAppModel1)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)


class ContentType(Model):
    __tablename__ = "django_content_type"
    app_label: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    logentry_set: Mapped[list["LogEntry"]] = relationship(back_populates="content_type")
    permission_set: Mapped[list["Permission"]] = relationship(back_populates="content_type")


class Permission(Model):
    __tablename__ = "auth_permission"
    name: Mapped[str] = mapped_column(String(255))
    content_type: Mapped["ContentType"] = relationship(back_populates="permission_set")
    content_type_id: Mapped[int] = mapped_column(ForeignKey("django_content_type.id"))
    codename: Mapped[str] = mapped_column(String(100))
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    group_set: Mapped[list["Group"]] = relationship(back_populates="permissions",secondary=Group_Permission)


class TestAppModel1(Model):
    __tablename__ = "testApp_testappmodel1"
    char_field: Mapped[str] = mapped_column(String(200))
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    cross_app_m2mtest: Mapped[list["Many2ManyTest"]] = relationship(back_populates="crossAppModel",secondary=Many2ManyTest_TestAppModel1)


