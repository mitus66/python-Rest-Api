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
        print(row[0])  # Доступ до елемента кортежу
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


if __name__ == "__main__":
    # Приклад виклику функцій
    # Перед запуском переконайтеся, що база даних створена та заповнена (виконайте seed.py)

    # Отримайте реальні імена студентів та викладачів з вашої бази даних
    # для тестування запитів, що вимагають конкретних імен.
    # Наприклад:
    # try:
    #     first_student = session.query(Student).first()
    #     first_teacher = session.query(Teacher).first()
    #     if first_student:
    #         print(f"Приклад імені студента: {first_student.fullname}")
    #     if first_teacher:
    #         print(f"Приклад імені викладача: {first_teacher.fullname}")
    # except Exception as e:
    #     print(f"Не вдалося отримати приклади імен: {e}")

    select_1()
    select_2('Математика')  # Замініть на реальний предмет
    select_3('Фізика')  # Замініть на реальний предмет
    select_4()
    # Щоб протестувати select_5, select_8, select_9, select_10, вам потрібно буде
    # знати реальні імена викладачів та студентів з вашої заповненої бази даних.
    # Ви можете запустити seed.py, а потім вручну перевірити таблиці,
    # або додати логіку для вибору випадкових імен з бази.

    # Приклад виклику з реальними даними (замініть на імена з вашої БД)
    # select_5('Олена Коваленко')
    # select_6('Group A')
    # select_7('Group B', 'Хімія')
    # select_8('Іван Петренко')
    # select_9('Марія Савченко')
    # select_10('Андрій Мельник', 'Олена Коваленко')

    session.close()  # Важливо закривати сесію після завершення роботи
