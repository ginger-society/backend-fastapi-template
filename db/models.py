from __future__ import annotations

from db.meta import Model
from sqlalchemy import String, Boolean, ForeignKey, Column, Table, Enum, Integer, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import enum
from pydantic import BaseModel
import datetime





class Course_TypeEnum(enum.Enum):

    compulsary = "Compulsary"
    elective = "Elective"
    



class SubjectEnum(enum.Enum):

    english = "English"
    hindi = "Hindi"
    maths = "Maths"
    science = "Science"
    social_studies = "Social Studies"
    




class Student(Model):
    __tablename__ = "student"
    name: Mapped[str] = mapped_column(String(150))
    roll_number: Mapped[str] = mapped_column(String(40))
    on_scholarship: Mapped[bool] = mapped_column(Boolean)
    father_name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(500))
    data_of_birth: Mapped[Date] = mapped_column(Date)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[Date] = mapped_column(Date)
    has_cab_service: Mapped[bool] = mapped_column(Boolean)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    courses: Mapped[list["Enrollment"]] = relationship(back_populates="student")


class Enrollment(Model):
    __tablename__ = "enrollment"
    student: Mapped["Student"] = relationship(back_populates="courses")
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    course: Mapped["Course"] = relationship(back_populates="enrollment_set")
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    id: Mapped[int] = mapped_column(Integer,primary_key=True)


class Course(Model):
    __tablename__ = "course"
    name: Mapped[str] = mapped_column(String(100))
    course_type: Mapped[str] = mapped_column(Enum(Course_TypeEnum))
    duration: Mapped[int] = mapped_column(Integer)
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    enrollment_set: Mapped[list["Enrollment"]] = relationship(back_populates="course")


class Exam(Model):
    __tablename__ = "exam"
    date: Mapped[Date] = mapped_column(Date)
    subject: Mapped[str] = mapped_column(Enum(SubjectEnum))
    id: Mapped[int] = mapped_column(Integer,primary_key=True)





class StudentT(BaseModel):
    
    name: str
    roll_number: str
    on_scholarship: bool
    father_name: Optional[str]
    address: str
    data_of_birth: Optional[datetime.date]
    created_at: datetime.datetime
    updated_at: datetime.date
    has_cab_service: Optional[bool]
    id: int
    courses: list["EnrollmentT"]
    class Config:
        orm_mode = True

class EnrollmentT(BaseModel):
    
    student: "StudentT"
    student_id: int
    course: Optional["CourseT"]
    course_id: Optional[int]
    id: int
    class Config:
        orm_mode = True

class CourseT(BaseModel):
    
    name: str
    course_type: str
    duration: Optional[int]
    id: int
    enrollment_set: Optional[list["EnrollmentT"]]
    class Config:
        orm_mode = True

class ExamT(BaseModel):
    
    date: datetime.date
    subject: str
    id: int
    class Config:
        orm_mode = True





class StudentInsertableT(BaseModel):
    
    name: str
    roll_number: str
    on_scholarship: bool
    father_name: Optional[str]
    address: str
    data_of_birth: Optional[datetime.date]
    created_at: datetime.datetime
    updated_at: datetime.date
    has_cab_service: Optional[bool]
    
    courses: list["EnrollmentT"]
    class Config:
        orm_mode = True

class StudentUpdatableT(BaseModel):
    
    name: Optional[str]
    roll_number: Optional[str]
    on_scholarship: Optional[bool]
    father_name: Optional[str]
    address: Optional[str]
    data_of_birth: Optional[datetime.date]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.date]
    has_cab_service: Optional[bool]
    
    courses: Optional[list["EnrollmentT"]]
    class Config:
        orm_mode = True

class EnrollmentInsertableT(BaseModel):
    
    student: "StudentT"
    student_id: int
    course: Optional["CourseT"]
    course_id: Optional[int]
    
    class Config:
        orm_mode = True

class EnrollmentUpdatableT(BaseModel):
    
    student: Optional["StudentT"]
    student_id: Optional[int]
    course: Optional["CourseT"]
    course_id: Optional[int]
    
    class Config:
        orm_mode = True

class CourseInsertableT(BaseModel):
    
    name: str
    course_type: str
    duration: Optional[int]
    
    enrollment_set: Optional[list["EnrollmentT"]]
    class Config:
        orm_mode = True

class CourseUpdatableT(BaseModel):
    
    name: Optional[str]
    course_type: Optional[str]
    duration: Optional[int]
    
    enrollment_set: Optional[list["EnrollmentT"]]
    class Config:
        orm_mode = True

class ExamInsertableT(BaseModel):
    
    date: datetime.date
    subject: str
    
    class Config:
        orm_mode = True

class ExamUpdatableT(BaseModel):
    
    date: Optional[datetime.date]
    subject: Optional[str]
    
    class Config:
        orm_mode = True



StudentT.update_forward_refs()
StudentUpdatableT.update_forward_refs()
StudentInsertableT.update_forward_refs()

EnrollmentT.update_forward_refs()
EnrollmentUpdatableT.update_forward_refs()
EnrollmentInsertableT.update_forward_refs()

CourseT.update_forward_refs()
CourseUpdatableT.update_forward_refs()
CourseInsertableT.update_forward_refs()

ExamT.update_forward_refs()
ExamUpdatableT.update_forward_refs()
ExamInsertableT.update_forward_refs()


