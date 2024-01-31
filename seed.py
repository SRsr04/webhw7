from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables_for_student import Student, Group, Teacher, Subject, Grade, Base
from datetime import datetime, timedelta
import random

DATABASE_URL = "sqlite:///example.db"

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

fake = Faker()

def create_groups():
    group_names = ["Group A", "Group B", "Group C"]
    groups = []
    for name in group_names:
        group = Group(name=name)
        groups.append(group)
        session.add(group)
    session.commit()
    return groups

def create_teachers():
    teacher_names = [fake.name() for _ in range(5)]
    teachers = []
    for name in teacher_names:
        teacher = Teacher(name=name)
        teachers.append(teacher)
        session.add(teacher)
    session.commit()
    return teachers

def create_subjects(teachers):
    subject_names = ["Math", "Physics", "Chemistry", "Biology", "History"]
    subjects = []
    for name, teacher in zip(subject_names, teachers):
        subject = Subject(name=name, teacher=teacher)
        subjects.append(subject)
        session.add(subject)
    session.commit()
    return subjects

def create_students(groups):
    students = []
    for _ in range(50):
        student = Student(name=fake.name(), group=random.choice(groups))
        students.append(student)
        session.add(student)
    session.commit()
    return students

def create_grades(students, subjects):
    for student in students:
        for subject in subjects:
            grade = Grade(value=random.randint(60, 100), date=fake.date_between(start_date='-1y', end_date='today'), student=student, subject=subject)
            session.add(grade)
    session.commit()

def seed_database():
    groups = create_groups()
    teachers = create_teachers()
    subjects = create_subjects(teachers)
    students = create_students(groups)
    create_grades(students, subjects)

if __name__ == "__main__":
    seed_database()
