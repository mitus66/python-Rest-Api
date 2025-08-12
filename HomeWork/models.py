from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Базовий клас для декларативного відображення
Base = declarative_base()

# Визначення моделей
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    students = relationship('Student', back_populates='group')

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)

    subjects = relationship('Subject', back_populates='teacher')

    def __repr__(self):
        return f"<Teacher(id={self.id}, fullname='{self.fullname}')>"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})>"

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')

    def __repr__(self):
        return f"<Student(id={self.id}, fullname='{self.fullname}', group_id={self.group_id})>"

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer, nullable=False)
    grade_date = Column(Date, nullable=False)

    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')

    def __repr__(self):
        return f"<Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, grade={self.grade}, date={self.grade_date})>"

# Налаштування підключення до бази даних PostgreSQL
# Змініть 'mysecretpassword' на ваш пароль, якщо він інший
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()
