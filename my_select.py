from sqlalchemy import func, and_
from sqlalchemy.sql import select, desc, asc
from random import choice

from connect_db import session
from models import Student, Tutor, Group, Subject, Mark

def take_randoms() -> tuple:
        subquery_1 = (select(Subject.name_uq))
        subjects = session.execute(subquery_1).fetchall()
        rand_subject = choice(subjects)

        subquery_2 = (select(Group.name_uq))
        groups = session.execute(subquery_2).fetchall()
        rand_group = choice(groups)

        subquery_3 = (select(Student.name_uq))
        students = session.execute(subquery_3).fetchall()
        rand_student = choice(students)

        subquery_4 = (select(Tutor.name_uq))
        tutors = session.execute(subquery_4).fetchall()
        rand_tutor = choice(tutors)

        return rand_subject, rand_group, rand_student, rand_tutor

# RANDOM PASSED VALUES 
SQL_PASSED_VALUES = [(), ## 1 Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
              (take_randoms()[0][0],), ## 2 Знайти студента із найвищим середнім балом з певного предмета
              (take_randoms()[0][0],), ## 3 Знайти середній бал у групах з певного предмета.
              (), ## 4 Знайти середній бал на потоці (по всій таблиці оцінок).
              (take_randoms()[3][0],), ## 5 Знайти які курси читає певний викладач
              (take_randoms()[1][0],), ## 6 Знайти список студентів у певній групі.
              (take_randoms()[1][0], take_randoms()[0][0]), ## 7 Знайти оцінки студентів у окремій групі з певного предмета.
              (take_randoms()[3][0],), ## 8 Знайти середній бал, який ставить певний викладач зі своїх предметів.
              (take_randoms()[2][0],),  ## 9 Знайти список курсів, які відвідує студент.
              (take_randoms()[2][0], take_randoms()[3][0]), ## 10 Список курсів, які певному студенту читає певний викладач.
              (take_randoms()[2][0], take_randoms()[3][0]), ## 11 Середній бал, який певний викладач ставить певному студентові.
              (take_randoms()[1][0], take_randoms()[0][0]), ## 12 Оцінки студентів у певній групі з певного предмета на останньому занятті. (по каждому последнему занятию для каждого студента)
              (take_randoms()[1][0], take_randoms()[0][0]) ## 13 Оцінки студентів у певній групі з певного предмета на останньому занятті. (только 1 самое последнее занятие для указанного предмета)
              ]

# MANUAL PASSED VALUES 
# SQL_PASSED_VALUES = [(), ## 1 Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
#               (('Математика'),), ## 2 Знайти студента із найвищим середнім балом з певного предмета
#               ('Математика',), ## 3 Знайти середній бал у групах з певного предмета.
#               (), ## 4 Знайти середній бал на потоці (по всій таблиці оцінок).
#               ('Arthur Morris',), ## 5 Знайти які курси читає певний викладач
#               ('Группа Г',), ## 6 Знайти список студентів у певній групі.
#               ('Группа Г', 'Математика'), ## 7 Знайти оцінки студентів у окремій групі з певного предмета.
#               ('Arthur Morris',), ## 8 Знайти середній бал, який ставить певний викладач зі своїх предметів.
#               ('John Friedman',),  ## 9 Знайти список курсів, які відвідує студент.
#               ('John Friedman', 'Arthur Morris'), ## 10 Список курсів, які певному студенту читає певний викладач.
#               ('John Friedman', 'Arthur Morris'), ## 11 Середній бал, який певний викладач ставить певному студентові.
#               ('Группа Г', 'Математика'), ## 12 Оцінки студентів у певній групі з певного предмета на останньому занятті. (по каждому последнему занятию для каждого студента)
#               ('Группа Г', 'Математика') ## 13 Оцінки студентів у певній групі з певного предмета на останньому занятті. (только 1 самое последнее занятие для указанного предмета)
#               ]

def select_1() -> list: ## -- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
        subquery = (
            select(Student.name_uq, func.ROUND(func.AVG(Mark.mark_value), 0).label('average_mark')). \
            select_from(Student). \
            join(Mark, Student.id_pk == Mark.student_id_fk). \
            group_by(Student.name_uq). \
            order_by(desc('average_mark')). \
            limit(5)
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_2(value: tuple) -> list: ## --  Знайти студента із найвищим середнім балом з певного предмета
        value = value[0]
        subquery = (
            select(Student.name_uq, func.max(Mark.mark_value).label('maximal_mark'), Subject.name_uq). \
            select_from(Mark). \
            join(Student, Student.id_pk == Mark.student_id_fk). \
            join(Subject, Subject.id_pk == Mark.subject_id_fk). \
            where(Subject.name_uq == value). \
            group_by(Student.name_uq, Subject.name_uq)
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_3(value: tuple) -> list: ## --  Знайти середній бал у групах з певного предмета.
        value = value[0]
        subquery = (
            select(Subject.name_uq, Group.name_uq, func.ROUND(func.AVG(Mark.mark_value), 2).label('average_mark'),). \
            select_from(Mark). \
            join(Student, Student.id_pk == Mark.student_id_fk). \
            join(Subject, Subject.id_pk == Mark.subject_id_fk). \
            join(Group, Group.id_pk == Student.group_id). \
            where(Subject.name_uq == value). \
            group_by(Subject.name_uq, Group.name_uq). \
            order_by(desc('average_mark'))
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_4() -> list: ## --  Знайти середній бал на потоці (по всій таблиці оцінок).
        subquery = (
            select(func.ROUND(func.AVG(Mark.mark_value), 2).label('total_average'),). \
            select_from(Mark)
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_5(value: tuple) -> list: ## --  Знайти які курси читає певний викладач
        value = value[0]
        subquery = (
            select(Tutor.name_uq, Subject.name_uq). \
            select_from(Subject). \
            join(Tutor, Subject.tutor_id_fk == Tutor.id_pk). \
            where(Tutor.name_uq == value). \
            group_by(Tutor.name_uq, Subject.name_uq)
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_6(value: tuple) -> list: ## --  Знайти список студентів у певній групі.
        value = value[0]
        subquery = (
            select(Group.name_uq, Student.name_uq). \
            select_from(Group). \
            join(Student, Student.group_id == Group.id_pk). \
            where(Group.name_uq == value). \
            group_by(Group.name_uq, Student.name_uq). \
            order_by(asc(Group.name_uq))
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_7(values: tuple) -> list: ## --  Знайти оцінки студентів у окремій групі з певного предмета.
        subquery = (
            select(Group.name_uq, Subject.name_uq, Mark.mark_value, Student.name_uq). \
            select_from(Mark). \
            join(Student, Student.id_pk == Mark.student_id_fk). \
            join(Group, Student.group_id == Group.id_pk). \
            join(Subject, Subject.id_pk == Mark.subject_id_fk). \
            where(Group.name_uq == values[0] and Subject.name_uq == values[1]). \
            group_by(Group.name_uq, Subject.name_uq, Student.name_uq, Mark.mark_value). \
            order_by(asc(Student.name_uq))
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_8(value: tuple) -> list: ## --  Знайти середній бал, який ставить певний викладач зі своїх предметів.
        value = value[0]        
        subquery = (
            select(Tutor.name_uq, Subject.name_uq, func.ROUND(func.AVG(Mark.mark_value), 2)). \
            select_from(Subject). \
            join(Tutor, Tutor.id_pk == Subject.tutor_id_fk). \
            join(Mark, Mark.subject_id_fk == Subject.id_pk). \
            where(Tutor.name_uq == value). \
            group_by(Tutor.name_uq, Subject.name_uq). \
            order_by(Tutor.name_uq)
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result

def select_9(value: tuple) -> list: ## --  Знайти список курсів, які відвідує студент.
        value = value[0]        
        subquery = (
            select(Student.name_uq, Subject.name_uq). \
            select_from(Mark). \
            join(Student, Student.id_pk == Mark.student_id_fk). \
            join(Subject, Mark.subject_id_fk == Subject.id_pk). \
            where(Student.name_uq == value). \
            group_by(Student.name_uq, Subject.name_uq)
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result


def select_10(values: tuple) -> list: ## --  Список курсів, які певному студенту читає певний викладач.
        subquery = (
            select(Student.name_uq, Tutor.name_uq, Subject.name_uq). \
            select_from(Mark). \
            join(Student, Student.id_pk == Mark.student_id_fk). \
            join(Subject, Mark.subject_id_fk == Subject.id_pk). \
            join(Tutor, Tutor.id_pk == Subject.tutor_id_fk). \
            where(Student.name_uq == values[0] and Tutor.name_uq == values[1]). \
            order_by(Student.name_uq)
        )

        query = session.execute(subquery)
        result = query.mappings().all()
        return result


def select_11(values: tuple) -> list: ## --  Середній бал, який певний викладач ставить певному студентові.
        
        subquery = (
                    select(Student.name_uq.label('student_name'),
                        Tutor.name_uq.label('tutor_name'),
                        func.ROUND(func.AVG(Mark.mark_value), 2).label('average_mark')). \
                        select_from(Mark). \
                        join(Student, Student.id_pk == Mark.student_id_fk). \
                        join(Subject, Mark.subject_id_fk == Subject.id_pk). \
                        join(Tutor, Tutor.id_pk == Subject.tutor_id_fk). \
                        group_by('student_name', 'tutor_name', Subject.name_uq).subquery()
        )
        
        query = (
            select(subquery.c.student_name, subquery.c.tutor_name, subquery.c.average_mark). \
            select_from(subquery). \
            where(subquery.c.student_name == values[0] and subquery.c.tutor_name == values[1]). \
            group_by(subquery.c.student_name, subquery.c.tutor_name, subquery.c.average_mark). \
            order_by(subquery.c.student_name, subquery.c.tutor_name)
        )

        raw_result = session.execute(query)
        result = raw_result.mappings().all()
        return result


def select_12(values: tuple) -> list: ## --  Оцінки студентів у певній групі з певного предмета на останньому занятті.  
    query = (
        select(Student.name_uq, Group.name_uq, Subject.name_uq, Mark.mark_value, func.max(Mark.today_date))
        .select_from(Student)
        .join(Group, Group.id_pk == Student.group_id)
        .join(Mark, Student.id_pk == Mark.student_id_fk)
        .join(Subject, Mark.subject_id_fk == Subject.id_pk)
        .where(Group.name_uq == values[0])
        .where(Subject.name_uq == values[1])
        .group_by(Student.name_uq, Group.name_uq, Subject.name_uq, Mark.mark_value)
    )

    raw_result = session.execute(query)
    result = raw_result.mappings().all()
    return result


q_dict = [select_1, select_2, select_3, select_4, select_5, 
          select_6, select_7, select_8, select_9, select_10,
          select_11, select_12]

if __name__ == '__main__':
    with session:
        try:
            i = 0
            for selection in q_dict:
                print('+' * 10)
                print(f'Executing {selection.__name__}')
                if SQL_PASSED_VALUES[i]:
                    print(f'With passed values: {SQL_PASSED_VALUES[i]}')
                    result = selection(SQL_PASSED_VALUES[i])
                else:
                    result = selection()
                print(result)
                i += 1
        except Exception as excpt:
            print(f'ERROR!!!&!&!&!&!&!: {excpt}')

    print('DONE!')