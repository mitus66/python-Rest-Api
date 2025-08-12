import argparse
from datetime import datetime
from sqlalchemy import func
from models import Group, Teacher, Subject, Student, Grade, session  # Імпортуємо сесію та моделі


def create_record(model, **kwargs):
    """Створює новий запис у базі даних."""
    try:
        if model == Group:
            new_record = Group(name=kwargs['name'])
        elif model == Teacher:
            new_record = Teacher(fullname=kwargs['name'])
        elif model == Student:
            group = session.query(Group).filter_by(id=kwargs['group_id']).first()
            if not group:
                raise ValueError(f"Group with ID {kwargs['group_id']} not found.")
            new_record = Student(fullname=kwargs['name'], group=group)
        elif model == Subject:
            teacher = session.query(Teacher).filter_by(id=kwargs['teacher_id']).first()
            if not teacher:
                raise ValueError(f"Teacher with ID {kwargs['teacher_id']} not found.")
            new_record = Subject(name=kwargs['name'], teacher=teacher)
        elif model == Grade:
            student = session.query(Student).filter_by(id=kwargs['student_id']).first()
            subject = session.query(Subject).filter_by(id=kwargs['subject_id']).first()
            if not student:
                raise ValueError(f"Student with ID {kwargs['student_id']} not found.")
            if not subject:
                raise ValueError(f"Subject with ID {kwargs['subject_id']} not found.")
            grade_date = datetime.strptime(kwargs['grade_date'], '%Y-%m-%d').date()
            new_record = Grade(student=student, subject=subject, grade=kwargs['grade'], grade_date=grade_date)
        else:
            raise ValueError("Unsupported model for creation.")

        session.add(new_record)
        session.commit()
        print(f"Successfully created {model.__name__}: {new_record}")
    except Exception as e:
        session.rollback()
        print(f"Error creating {model.__name__}: {e}")
    finally:
        session.close()


def list_records(model):
    """Виводить список всіх записів для даної моделі."""
    try:
        records = session.query(model).all()
        if not records:
            print(f"No {model.__name__} records found.")
            return

        print(f"\n--- All {model.__name__}s ---")
        for record in records:
            if model == Student:
                print(f"ID: {record.id}, Name: {record.fullname}, Group: {record.group.name}")
            elif model == Subject:
                print(f"ID: {record.id}, Name: {record.name}, Teacher: {record.teacher.fullname}")
            elif model == Grade:
                print(
                    f"ID: {record.id}, Student: {record.student.fullname}, Subject: {record.subject.name}, Grade: {record.grade}, Date: {record.grade_date}")
            else:
                print(f"ID: {record.id}, Name: {record.name if hasattr(record, 'name') else record.fullname}")
        print("--------------------")
    except Exception as e:
        print(f"Error listing {model.__name__}s: {e}")
    finally:
        session.close()


def update_record(model, record_id, **kwargs):
    """Оновлює існуючий запис."""
    try:
        record = session.query(model).filter_by(id=record_id).first()
        if not record:
            print(f"{model.__name__} with ID {record_id} not found.")
            return

        if model == Group:
            record.name = kwargs.get('name', record.name)
        elif model == Teacher:
            record.fullname = kwargs.get('name', record.fullname)
        elif model == Student:
            record.fullname = kwargs.get('name', record.fullname)
            if 'group_id' in kwargs:
                group = session.query(Group).filter_by(id=kwargs['group_id']).first()
                if not group:
                    raise ValueError(f"Group with ID {kwargs['group_id']} not found.")
                record.group = group
        elif model == Subject:
            record.name = kwargs.get('name', record.name)
            if 'teacher_id' in kwargs:
                teacher = session.query(Teacher).filter_by(id=kwargs['teacher_id']).first()
                if not teacher:
                    raise ValueError(f"Teacher with ID {kwargs['teacher_id']} not found.")
                record.teacher = teacher
        elif model == Grade:
            record.grade = kwargs.get('grade', record.grade)
            if 'grade_date' in kwargs:
                record.grade_date = datetime.strptime(kwargs['grade_date'], '%Y-%m-%d').date()
            if 'student_id' in kwargs:
                student = session.query(Student).filter_by(id=kwargs['student_id']).first()
                if not student:
                    raise ValueError(f"Student with ID {kwargs['student_id']} not found.")
                record.student = student
            if 'subject_id' in kwargs:
                subject = session.query(Subject).filter_by(id=kwargs['subject_id']).first()
                if not subject:
                    raise ValueError(f"Subject with ID {kwargs['subject_id']} not found.")
                record.subject = subject
        else:
            raise ValueError("Unsupported model for update.")

        session.commit()
        print(f"Successfully updated {model.__name__} with ID {record_id}: {record}")
    except Exception as e:
        session.rollback()
        print(f"Error updating {model.__name__} with ID {record_id}: {e}")
    finally:
        session.close()


def remove_record(model, record_id):
    """Видаляє запис за ID."""
    try:
        record = session.query(model).filter_by(id=record_id).first()
        if not record:
            print(f"{model.__name__} with ID {record_id} not found.")
            return

        session.delete(record)
        session.commit()
        print(f"Successfully removed {model.__name__} with ID {record_id}.")
    except Exception as e:
        session.rollback()
        print(f"Error removing {model.__name__} with ID {record_id}: {e}")
    finally:
        session.close()


def get_model_class(model_name: str):
    """Повертає клас моделі за її назвою."""
    models_map = {
        'Group': Group,
        'Teacher': Teacher,
        'Subject': Subject,
        'Student': Student,
        'Grade': Grade
    }
    model_class = models_map.get(model_name.capitalize())
    if not model_class:
        raise ValueError(f"Unknown model: {model_name}. Available models: {', '.join(models_map.keys())}")
    return model_class


def main():
    parser = argparse.ArgumentParser(description="CLI for managing university database.")
    parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'remove'], required=True,
                        help="CRUD operation to perform.")
    parser.add_argument('-m', '--model', choices=['Group', 'Teacher', 'Subject', 'Student', 'Grade'], required=True,
                        help="Model to perform operation on.")
    parser.add_argument('-id', '--id', type=int, help="ID of the record to update or remove.")
    parser.add_argument('-n', '--name', help="Name for Group, Teacher, Student, Subject.")
    parser.add_argument('--fullname', help="Full name for Teacher or Student (alias for -n).")  # Alias for -n
    parser.add_argument('--group_id', type=int, help="Group ID for Student.")
    parser.add_argument('--teacher_id', type=int, help="Teacher ID for Subject.")
    parser.add_argument('--student_id', type=int, help="Student ID for Grade.")
    parser.add_argument('--subject_id', type=int, help="Subject ID for Grade.")
    parser.add_argument('--grade', type=int, help="Grade value for Grade.")
    parser.add_argument('--grade_date', help="Grade date for Grade (YYYY-MM-DD).")

    args = parser.parse_args()

    model_class = get_model_class(args.model)

    if args.action == 'create':
        if args.model == 'Group' and not args.name:
            parser.error("Group creation requires --name.")
        if args.model == 'Teacher' and not args.name and not args.fullname:
            parser.error("Teacher creation requires --name or --fullname.")
        if args.model == 'Student' and (not args.name and not args.fullname or not args.group_id):
            parser.error("Student creation requires --name/--fullname and --group_id.")
        if args.model == 'Subject' and (not args.name or not args.teacher_id):
            parser.error("Subject creation requires --name and --teacher_id.")
        if args.model == 'Grade' and (
                not args.student_id or not args.subject_id or args.grade is None or not args.grade_date):
            parser.error("Grade creation requires --student_id, --subject_id, --grade, and --grade_date (YYYY-MM-DD).")

        # Використовуємо 'name' або 'fullname' для Teacher/Student
        name_arg = args.name if args.name else args.fullname

        create_record(model_class,
                      name=name_arg,
                      group_id=args.group_id,
                      teacher_id=args.teacher_id,
                      student_id=args.student_id,
                      subject_id=args.subject_id,
                      grade=args.grade,
                      grade_date=args.grade_date)

    elif args.action == 'list':
        list_records(model_class)

    elif args.action == 'update':
        if not args.id:
            parser.error("Update action requires --id.")

        update_kwargs = {}
        if args.name:
            update_kwargs['name'] = args.name
        if args.fullname:  # Allow fullname to update name
            update_kwargs['name'] = args.fullname
        if args.group_id:
            update_kwargs['group_id'] = args.group_id
        if args.teacher_id:
            update_kwargs['teacher_id'] = args.teacher_id
        if args.student_id:
            update_kwargs['student_id'] = args.student_id
        if args.subject_id:
            update_kwargs['subject_id'] = args.subject_id
        if args.grade is not None:
            update_kwargs['grade'] = args.grade
        if args.grade_date:
            update_kwargs['grade_date'] = args.grade_date

        if not update_kwargs:
            parser.error("Update action requires at least one field to update (--name, --group_id, etc.).")

        update_record(model_class, args.id, **update_kwargs)

    elif args.action == 'remove':
        if not args.id:
            parser.error("Remove action requires --id.")
        remove_record(model_class, args.id)


if __name__ == "__main__":
    main()
