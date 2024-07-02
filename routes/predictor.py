from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request

from db.dependencies import get_db_session
from db.models.notes import Note, NoteT
from db.models.sql_models import *
from db.models.administrator import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from cache.dependency import get_redis_pool
from redis.asyncio import ConnectionPool, Redis
from core.monitoring import COUNT_METRIC

router = APIRouter()


class TestResponse(BaseModel):
    var1: str


class TestRequest(BaseModel):
    q: str


class HealthResponse(BaseModel):
    status: bool


@router.post(
    "/test1",
    response_model=TestResponse,
    name="predict:get-data",
)
async def predict(data_input: TestRequest):
    return TestResponse(var1=data_input.q)


@router.get(
    "/health",
    response_model=HealthResponse,
    name="health:get-data",
)
async def health():
    return HealthResponse(status=True)


@router.get(
    "/notes/",
    response_model=list[NoteT],
    name="db-test:get-data",
)
async def read_notes(request: Request, db: AsyncSession = Depends(get_db_session)):
    q = await db.execute(Note.select())
    results = q.tuples()
    return [NoteT(id=r.id, text=r.text, completed=r.completed) for r in results]


@router.get(
    "/tenant/",
    response_model=list[TenantT],
    name="db-test:get-data-foreign-key",
)
async def getTanants(request: Request, db: AsyncSession = Depends(get_db_session)):
    q = await db.scalars(select(Tenant).options(selectinload(Tenant.users)))

    return [
        TenantT(
            id=r.id,
            name=r.name,
            is_active=r.is_active,
            expiry_date=r.expiry_date,
            users=[
                AdministratorT(
                    id=admin.id,
                    name=admin.name,
                    email=admin.email,
                    is_active=admin.is_active,
                    is_admin=admin.is_admin,
                    is_staff=admin.is_staff,
                    password_change_required=admin.password_change_required,
                    next_password_change_due=admin.next_password_change_due,
                )
                for admin in r.users
            ],
        )
        for r in q
    ]


@router.get(
    "/tenant-with-join/",
    response_model=list[TenantT],
    name="db-test:get-data-with-join",
)
async def getTenantsWithJoin(
    request: Request, db: AsyncSession = Depends(get_db_session)
):
    COUNT_METRIC.labels("with-join").inc()
    q = await db.scalars(select(Tenant).options(joinedload(Tenant.users)))
    # pass innerjoin=True to get the Tenants where there is at least one user

    return [
        TenantT(
            id=r.id,
            name=r.name,
            is_active=r.is_active,
            expiry_date=r.expiry_date,
            users=[
                AdministratorT(
                    id=admin.id,
                    name=admin.name,
                    email=admin.email,
                    is_active=admin.is_active,
                    is_admin=admin.is_admin,
                    is_staff=admin.is_staff,
                    password_change_required=admin.password_change_required,
                    next_password_change_due=admin.next_password_change_due,
                )
                for admin in r.users
            ],
        )
        for r in q.unique()
    ]


@router.get(
    "/tenant-with-auto-serializer/",
    response_model=TenantSimpleT,
    name="db-test:get-data-with-auto-serializer",
)
async def getTenantsWithJoin(
    request: Request, db: AsyncSession = Depends(get_db_session)
):
    q = await db.scalars(select(Tenant).limit(1))
    print(q)
    return TenantSimpleT.from_orm(q.first())


@router.get(
    "/admin-with-auto-serializer/",
    response_model=list[AdministratorSimpleT],
    name="db-test:get-admin-data-with-auto-serializer",
)
async def getAdminsWithJoin(
    request: Request, db: AsyncSession = Depends(get_db_session)
):
    q = await db.execute(
        select(Administrator).options(joinedload(Administrator.tenant))
    )
    return [AdministratorSimpleT.from_orm(admin) for admin in q.scalars()]


@router.get(
    "/admins/",
    response_model=list[AdministratorSimplestT],
    name="db-test:get-admins-data-with-auto-serializer",
)
async def getAdminsWithJoin(
    request: Request, db: AsyncSession = Depends(get_db_session)
):
    q = await db.execute(select(Administrator))
    return [
        AdministratorSimplestT(
            id=admin.id,
            name=admin.name,
            email=admin.email,
            is_active=admin.is_active,
            is_admin=admin.is_admin,
            is_staff=admin.is_staff,
            password_change_required=admin.password_change_required,
            next_password_change_due=admin.next_password_change_due,
        )
        for admin in q.scalars()
    ]


@router.get(
    "/cache-test/",
    response_model=str,
    name="db-test:get-data-from-cache",
)
async def read_cache(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
):
    async with Redis(connection_pool=redis_pool) as cache:
        await cache.set("mykey", "cached-val")
        data = await cache.get("mykey")
    return data


@router.get(
    "/m2m-test/",
    response_model=list[Many2ManyTestT],
    name="db-test:m2m-test",
)
async def m2mTest(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
):
    q = await db.scalars(
        select(Many2ManyTest).options(
            joinedload(Many2ManyTest.testModels),
            joinedload(Many2ManyTest.crossAppModel),
        )
    )
    return [Many2ManyTestT.from_orm(obj) for obj in q.unique()]
