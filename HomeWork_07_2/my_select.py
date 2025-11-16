from sqlalchemy import func, desc, and_
from models import Student, Grade, Subject, Teacher, Group, session


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    result = session.query(
        Student.fullname,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Grade).join(Student).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    print("\n1. 5 студентів із найбільшим середнім балом:")
    for row in result:
        print(row)
    return result


# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name: str = 'Математика'):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    result = session.query(
        Student.fullname,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Grade).join(Student).join(Subject).filter(Subject.name == subject_name).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    print(f"\n2. Студент з найвищим середнім балом з '{subject_name}':")
    for row in result:
        print(row)
    return result


# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_name: str = 'Фізика'):
    """Знайти середній бал у групах з певного предмета."""
    result = session.query(
        Group.name,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Grade).join(Student).join(Group).join(Subject).filter(Subject.name == subject_name).group_by(
        Group.name).order_by(Group.name).all()
    print(f"\n3. Середній бал у групах з '{subject_name}':")
    for row in result:
        print(row)
    return result


# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    result = session.query(
        func.round(func.avg(Grade.grade), 2).label('overall_average_grade')
    ).select_from(Grade).all()
    print("\n4. Середній бал на потоці:")
    for row in result:
        print(row)
    return result


# 5. Знайти які курси читає певний викладач.
def select_5(teacher_fullname: str = 'Ім`я Викладача'):
    """Знайти які курси читає певний викладач."""
    result = session.query(
        Subject.name
    ).join(Teacher).filter(Teacher.fullname == teacher_fullname).all()
    print(f"\n5. Курси, які читає '{teacher_fullname}':")
    for row in result:
        print(row[0])
    return result


# 6. Знайти список студентів у певній групі.
def select_6(group_name: str = 'Group A'):
    """Знайти список студентів у певній групі."""
    result = session.query(
        Student.fullname
    ).join(Group).filter(Group.name == group_name).order_by(Student.fullname).all()
    print(f"\n6. Студенти у групі '{group_name}':")
    for row in result:
        print(row[0])
    return result


# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_name: str = 'Group B', subject_name: str = 'Хімія'):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    result = session.query(
        Student.fullname,
        Grade.grade,
        Grade.grade_date
    ).select_from(Grade).join(Student).join(Group).join(Subject).filter(
        and_(Group.name == group_name, Subject.name == subject_name)
    ).order_by(Student.fullname, Grade.grade_date).all()
    print(f"\n7. Оцінки студентів у групі '{group_name}' з предмета '{subject_name}':")
    for row in result:
        print(row)
    return result


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_fullname: str = 'Ім`я Викладача'):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    result = session.query(
        Teacher.fullname,
        func.round(func.avg(Grade.grade), 2).label('average_grade_by_teacher')
    ).select_from(Grade).join(Subject).join(Teacher).filter(Teacher.fullname == teacher_fullname).group_by(
        Teacher.fullname).all()
    print(f"\n8. Середній бал, який ставить викладач '{teacher_fullname}':")
    for row in result:
        print(row)
    return result


# 9. Знайти список курсів, які відвідує певний студент.
def select_9(student_fullname: str = 'Ім`я Студента'):
    """Знайти список курсів, які відвідує певний студент."""
    result = session.query(
        Subject.name
    ).select_from(Grade).join(Student).join(Subject).filter(Student.fullname == student_fullname).group_by(
        Subject.name).order_by(Subject.name).all()
    print(f"\n9. Курси, які відвідує студент '{student_fullname}':")
    for row in result:
        print(row[0])
    return result


# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_fullname: str = 'Ім`я Студента', teacher_fullname: str = 'Ім`я Викладача'):
    """Список курсів, які певному студенту читає певний викладач."""
    result = session.query(
        Subject.name
    ).select_from(Grade).join(Student).join(Subject).join(Teacher).filter(
        and_(Student.fullname == student_fullname, Teacher.fullname == teacher_fullname)
    ).group_by(Subject.name).order_by(Subject.name).all()
    print(f"\n10. Курси, які '{teacher_fullname}' читає студенту '{student_fullname}':")
    for row in result:
        print(row[0])
    return result


# --- Запити підвищеної складності ---

# 11. Середній бал, який певний викладач ставить певному студентові.
def select_11(student_fullname: str = 'Ім`я Студента', teacher_fullname: str = 'Ім`я Викладача'):
    """Середній бал, який певний викладач ставить певному студентові."""
    result = session.query(
        Student.fullname,
        Teacher.fullname,
        func.round(func.avg(Grade.grade), 2).label('average_grade')
    ).select_from(Grade).join(Student).join(Subject).join(Teacher).filter(
        and_(Student.fullname == student_fullname, Teacher.fullname == teacher_fullname)
    ).group_by(Student.fullname, Teacher.fullname).all()
    print(f"\n11. Середній бал, який '{teacher_fullname}' ставить студенту '{student_fullname}':")
    for row in result:
        print(row)
    return result


# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(group_name: str = 'Group A', subject_name: str = 'Математика'):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    # Підзапит для знаходження максимальної дати оцінки для кожного студента з даного предмета
    subquery = session.query(
        Grade.student_id,
        func.max(Grade.grade_date).label('max_grade_date')
    ).join(Subject).filter(Subject.name == subject_name).group_by(Grade.student_id).subquery()

    result = session.query(
        Student.fullname,
        Group.name,
        Subject.name,
        Grade.grade,
        Grade.grade_date
    ).select_from(Grade).join(Student).join(Group).join(Subject).join(
        subquery,
        and_(
            Grade.student_id == subquery.c.student_id,
            Grade.grade_date == subquery.c.max_grade_date,
            Subject.name == subject_name  # Додаткова фільтрація для точності
        )
    ).filter(
        and_(Group.name == group_name, Subject.name == subject_name)
    ).order_by(Student.fullname).all()

    print(f"\n12. Оцінки студентів у групі '{group_name}' з предмета '{subject_name}' на останньому занятті:")
    for row in result:
        print(row)
    return result


if __name__ == "__main__":
    # Приклад виклику функцій
    # Перед запуском переконайтеся, що база даних створена та заповнена (виконайте seed.py)

    # Отримайте реальні імена студентів, викладачів та груп з вашої бази даних
    # для тестування запитів, що вимагають конкретних імен.
    # Наприклад, можна додати тимчасовий код для вибору випадкових імен:
    try:
        sample_student = session.query(Student).order_by(func.random()).first()
        sample_teacher = session.query(Teacher).order_by(func.random()).first()
        sample_group = session.query(Group).order_by(func.random()).first()
        sample_subject = session.query(Subject).order_by(func.random()).first()

        student_name = sample_student.fullname if sample_student else 'Невідомий Студент'
        teacher_name = sample_teacher.fullname if sample_teacher else 'Невідомий Викладач'
        group_name = sample_group.name if sample_group else 'Невідома Група'
        subject_name = sample_subject.name if sample_subject else 'Невідомий Предмет'

        print(f"\nВикористовуються приклади даних для запитів:")
        print(f"Студент: {student_name}")
        print(f"Викладач: {teacher_name}")
        print(f"Група: {group_name}")
        print(f"Предмет: {subject_name}")

        select_1()
        select_2(subject_name)
        select_3(subject_name)
        select_4()
        select_5(teacher_name)
        select_6(group_name)
        select_7(group_name, subject_name)
        select_8(teacher_name)
        select_9(student_name)
        select_10(student_name, teacher_name)
        select_11(student_name, teacher_name)
        select_12(group_name, subject_name)

    except Exception as e:
        print(f"Помилка під час виконання запитів: {e}")
    finally:
        session.close()  # Важливо закривати сесію після завершення роботи
