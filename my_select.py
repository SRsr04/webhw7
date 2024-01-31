from sqlalchemy import func, desc
from tables_for_student import Student, Group, Teacher, Subject, Grade, Base, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///example.db"

engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def select_1():
    
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    
    result = session.query(Student.fullname, func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result

def select_2(subject_name):
    
    # Знайти студента із найвищим середнім балом з певного предмета.
    
    result = session.query(Student.fullname, func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .join(Grade).join(Subject).filter(Subject.name == subject_name).group_by(Student.id) \
        .order_by(desc('avg_grade')).first()
    return result

def select_3(subject_name):
    
    # Знайти середній бал у групах з певного предмета.
    
    result = session.query(Group.name, func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .join(Student).join(Grade).join(Subject).filter(Subject.name == subject_name).group_by(Group.id).all()
    return result

def select_4():
    
    # Знайти середній бал на потоці (по всій таблиці оцінок).
    
    result = session.query(func.round(func.avg(Grade.value), 2).label('avg_grade')).scalar()
    return result

def select_5(teacher_name):
    
    # Знайти які курси читає певний викладач.
    
    result = session.query(Subject.name) \
        .join(Teacher).filter(Teacher.name == teacher_name).all()
    return result

def select_6(group_name):
    
    # Знайти список студентів у певній групі.
    
    result = session.query(Student.fullname) \
        .join(Group).filter(Group.name == group_name).all()
    return result

def select_7(group_name, subject_name):
    
    # Знайти оцінки студентів у окремій групі з певного предмета.
    
    result = session.query(Student.fullname, Grade.value) \
        .join(Group).join(Grade).join(Subject).filter(Group.name == group_name, Subject.name == subject_name).all()
    return result

def select_8(teacher_name):
    
    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    
    result = session.query(func.round(func.avg(Grade.value), 2).label('avg_grade')) \
        .join(Teacher).filter(Teacher.name == teacher_name).scalar()
    return result

def select_9(student_fullname):
    
    # Знайти список курсів, які відвідує певний студент.
    
    result = session.query(Subject.name) \
        .join(Student).filter(Student.fullname == student_fullname).all()
    return result

def select_10(student_fullname, teacher_name):
    
    # Список курсів, які певному студенту читає певний викладач.
    
    result = session.query(Subject.name) \
        .join(Student).join(Teacher).filter(Student.fullname == student_fullname, Teacher.name == teacher_name).all()
    return result

if __name__ == "__main__":
    print("Select 1:")
    print(select_1())

    print("\nSelect 2:")
    print(select_2("Math"))

    print("\nSelect 3:")
    print(select_3("Physics"))

    print("\nSelect 4:")
    print(select_4())

    print("\nSelect 5:")
    print(select_5("John Doe"))

    print("\nSelect 6:")
    print(select_6("Group A"))

    print("\nSelect 7:")
    print(select_7("Group B", "Chemistry"))

    print("\nSelect 8:")
    print(select_8("John Doe"))

    print("\nSelect 9:")
    print(select_9("Alice Johnson"))

    print("\nSelect 10:")
    print(select_10("Alice Johnson", "Professor Smith"))
