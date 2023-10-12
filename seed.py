from connect_db import session
from models import Student, Tutor, Group, Subject, Mark
import faker
from datetime import datetime, timedelta
from random import randint

faker = faker.Faker()

NUM_STUDENTS = 50
NUM_GROUPS = 3
NUM_SUBJECTS = randint(5, 8)
NUM_TUTORS = randint(3, 5)
NUM_MARKS = randint(10, 19)
FAKE_DATA_RANGES = NUM_STUDENTS, NUM_GROUPS, NUM_SUBJECTS, NUM_TUTORS, NUM_MARKS

groups = ["Группа А", "Группа Б", "Группа В", "Группа Г", "Группа Д"]
subjects = [
    "Математика",
    "Физика",
    "Химия Гачи-Мучи",
    "Истории у костра",
    "Иностранный язык",
    "Искусство",
    "Музыка",
    "Оленеводство",
    "Грибоварение",
]

def gen_fake_data(data_ranges: tuple) -> tuple:
    def generate_subject_name() -> str:
        while subjects:
            subject = faker.random_element(elements=subjects)
            subjects.remove(subject)
            yield subject

    def generate_group_name() -> str:
        group = faker.random_element(elements=groups)
        groups.remove(group)
        return group

    fake_students = []
    fake_groups = []
    fake_subjects = []
    fake_tutors = []
    fake_marks = []

    for _ in range(data_ranges[0]):
        fake_students.append(faker.name())

    for _ in range(data_ranges[1]):
        fake_groups.append(generate_group_name())

    subects_gen = generate_subject_name()
    for _ in range(data_ranges[2]):
        fake_subjects.append(next(subects_gen, None))

    for _ in range(data_ranges[3]):
        fake_tutors.append(faker.name())

    for _ in range(data_ranges[4]):
        fake_marks.append(randint(0, 100))

    return fake_students, fake_groups, fake_subjects, fake_tutors, fake_marks


def prepare_data(data: tuple) -> tuple:
    def generate_random_date() -> datetime:
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2023, 12, 31)
        delta = end_date - start_date
        random_days = randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        # random_date = random_date.strftime("%Y-%m-%d")
        return random_date

    students_list = []
    for item in data[0]:
        students_list.append((item, randint(1, NUM_GROUPS)))

    groups_list = []
    for item in data[1]:
        groups_list.append((item,))

    subjects_list = []
    for item in data[2]:
        subjects_list.append((item, randint(1, NUM_TUTORS)))

    tutors_list = []
    for item in data[3]:
        tutors_list.append((item,))

    marks_list = []
    for item in data[4]:
        marks_list.append(
            (
                item,
                randint(1, NUM_STUDENTS),
                randint(1, NUM_SUBJECTS),
                generate_random_date(),
            )
        )

    return students_list, groups_list, subjects_list, tutors_list, marks_list


def insert_data(data: tuple) -> None:
    with session:       
        try:
            for item in data[1]:
                    group = Group(name_uq=item[0])
                    session.add(group)
            session.commit()

            for item in data[0]:
                    student = Student(name_uq=item[0], group_id=item[1])
                    session.add(student)
            session.commit()

            for item in data[3]:
                    tutor = Tutor(name_uq=item[0])
                    session.add(tutor)
            session.commit()

            for item in data[2]:
                    subject = Subject(name_uq=item[0], tutor_id_fk=item[1])
                    session.add(subject)
            session.commit()

            for item in data[4]:
                    mark = Mark(mark_value=item[0], student_id_fk=item[1], subject_id_fk=item[2], today_date=item[3])
                    session.add(mark)
            session.commit()
            
        except Exception as error:
            print(error)
        

if __name__ == "__main__":
        generated_fake_data = gen_fake_data(FAKE_DATA_RANGES)
        prepared_fake_data = prepare_data(generated_fake_data)
        insert_data(prepared_fake_data)
