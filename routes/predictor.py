from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request, status

from db.dependencies import get_db_session
from db.models import *
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
    "/students-list/",
    response_model=list[StudentT],
    name="db-test:get-data-foreign-key",
)
async def getTanants(request: Request, db: AsyncSession = Depends(get_db_session)):
    q = await db.execute(select(Student))
    return [
        StudentT(
            id=admin.id,
            name=admin.name,
            roll_number=admin.roll_number,
            on_scholarship=admin.on_scholarship,
            father_name=admin.father_name,
            address=admin.address,
            created_at=admin.created_at,
            updated_at=admin.updated_at,
            has_cab_service=admin.has_cab_service,
            courses=[],
        )
        for admin in q.scalars()
    ]


@router.get(
    "/student-with-auto-serializer/",
    response_model=list[StudentT],
    name="db-test:get-admin-data-with-auto-serializer",
)
async def getAdminsWithJoin(
    request: Request, db: AsyncSession = Depends(get_db_session)
):
    q = await db.execute(
        select(Student).options(
            selectinload(Student.courses).selectinload(Enrollment.course)
        )
    )
    students = q.scalars().unique().all()
    return [StudentT.from_orm(admin) for admin in students]


@router.post(
    "/create-student/",
    response_model=StudentT,
    name="db-test:create-student",
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    request: Request,
    student_data: StudentInserableT,
    db: AsyncSession = Depends(get_db_session),
):
    new_student = Student(
        name=student_data.name,
        roll_number=student_data.roll_number,
        on_scholarship=student_data.on_scholarship,
        father_name=student_data.father_name,
        address=student_data.address,
        data_of_birth=student_data.data_of_birth,
        created_at=student_data.created_at,
        updated_at=student_data.updated_at,
        has_cab_service=student_data.has_cab_service,
    )

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return StudentT(
        id=new_student.id,
        name=new_student.name,
        roll_number=new_student.roll_number,
        on_scholarship=new_student.on_scholarship,
        father_name=new_student.father_name,
        address=new_student.address,
        created_at=new_student.created_at,
        updated_at=new_student.updated_at,
        has_cab_service=new_student.has_cab_service,
        courses=[],
    )


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
