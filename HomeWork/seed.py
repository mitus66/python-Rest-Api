from faker import Faker
import random
from datetime import datetime, timedelta
from models import Group, Teacher, Subject, Student, Grade, session  # Імпортуємо сесію та моделі

fake = Faker('uk_UA')


def seed_data(num_students=40, num_groups=3, num_teachers=4, num_subjects=7):
    """Заповнює базу даних випадковими даними."""
    try:
        # Очищаємо дані перед заповненням (опціонально, для розробки)
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()
        print("Existing data cleared.")

        # Заповнення груп
        groups = []
        for i in range(num_groups):
            group_name = f"Group {chr(65 + i)}"
            group = Group(name=group_name)
            groups.append(group)
            session.add(group)
        session.commit()
        print(f"Populated {num_groups} groups.")

        # Заповнення викладачів
        teachers = []
        for _ in range(num_teachers):
            teacher = Teacher(fullname=fake.name())
            teachers.append(teacher)
            session.add(teacher)
        session.commit()
        print(f"Populated {num_teachers} teachers.")

        # Заповнення предметів
        subjects = []
        subject_names = [
            "Математика", "Фізика", "Хімія", "Історія", "Література",
            "Програмування", "Економіка", "Біологія"
        ]
        random.shuffle(subject_names)

        for i in range(min(num_subjects, len(subject_names))):
            subject = Subject(name=subject_names[i], teacher=random.choice(teachers))
            subjects.append(subject)
            session.add(subject)
        session.commit()
        print(f"Populated {len(subjects)} subjects.")

        # Заповнення студентів
        students = []
        for _ in range(num_students):
            student = Student(fullname=fake.name(), group=random.choice(groups))
            students.append(student)
            session.add(student)
        session.commit()
        print(f"Populated {num_students} students.")

        # Заповнення оцінок
        for student in students:
            # Кожен студент отримує оцінки з випадкової кількості предметів
            num_subjects_for_student = random.randint(1, len(subjects))
            subjects_for_student = random.sample(subjects, num_subjects_for_student)

            for subject in subjects_for_student:
                # До 20 оцінок для кожного студента з кожного предмета
                num_grades = random.randint(1, 20)
                for _ in range(num_grades):
                    grade_value = random.randint(60, 100)  # Оцінки від 60 до 100

                    # Випадкова дата оцінки за останній рік
                    grade_date = fake.date_between(start_date='-1y', end_date='today')

                    grade = Grade(
                        student=student,
                        subject=subject,
                        grade=grade_value,
                        grade_date=grade_date
                    )
                    session.add(grade)
        session.commit()
        print("Populated grades for students.")

        print("Database populated successfully.")

    except Exception as e:
        session.rollback()  # Відкочуємо зміни у разі помилки
        print(f"An error occurred during seeding: {e}")
    finally:
        session.close()  # Закриваємо сесію


if __name__ == "__main__":
    seed_data()
