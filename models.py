from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from connect_db import engine

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id_pk = Column(Integer, primary_key=True, autoincrement=True)
    name_uq = Column(VARCHAR(56), nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey('groups.id_pk', ondelete='SET NULL', onupdate='CASCADE'))
    marks = relationship('Mark')


class Group(Base):
    __tablename__ = 'groups'
    id_pk = Column(Integer, primary_key=True, autoincrement=True)
    name_uq = Column(VARCHAR(56), nullable=False, unique=True)
    students = relationship('Student')


class Tutor(Base):
    __tablename__ = 'tutors'
    id_pk = Column(Integer, primary_key=True, autoincrement=True)
    name_uq = Column(VARCHAR(56), nullable=False, unique=True)
    students = relationship('Subject')


class Subject(Base):
    __tablename__ = 'subjects'
    id_pk = Column(Integer, primary_key=True, autoincrement=True)
    name_uq = Column(VARCHAR(26), nullable=False, unique=True)
    tutor_id_fk = Column(Integer, ForeignKey('tutors.id_pk', ondelete='SET NULL', onupdate='CASCADE'))
    marks = relationship('Mark')


class Mark(Base):
    __tablename__ = 'marks'
    id_pk = Column(Integer, primary_key=True, autoincrement=True)
    mark_value = Column(Integer, nullable=False)
    student_id_fk = Column(Integer, ForeignKey('students.id_pk', ondelete='CASCADE', onupdate='CASCADE'))
    subject_id_fk = Column(Integer, ForeignKey('subjects.id_pk', ondelete='CASCADE', onupdate='CASCADE'))
    today_date = Column(DateTime)


Base.metadata.create_all(engine)
Base.metadata.bind = engine