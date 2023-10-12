import argparse
from connect_db import session
from sqlalchemy.sql import text
from models import Student, Group, Tutor, Subject, Mark

## poetry run main.py -o list -m Student
## poetry run main.py -o create -m Group -a REVO_DRINKERS
## poetry run main.py -o delete -m Group -a 4
## poetry run main.py -o create -m Subject -a 'Mortilogy',1
## poetry run main.py -o update -m Subject -a 8,'Morti logy',2
## poetry run main.py -o delete -m Subject -a 8


### ARGPARSE CONFIGS
### REQUEST REFERENCE: py FileSort-multi-v1-dirwalker.py -s C:\Users\Professional\Desktop\sort_test -r no
### TRUE CLI SETTINGS START
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--operation", required=True, help="What to do? (create, list, update, remove)")
parser.add_argument("-m", "--model", required=False, help="Select model.")
parser.add_argument("-a", "--arguments", help="Pass the set of arguments via ','")
ARGUMENTS = vars(parser.parse_args())
### END OF TRUE SETTINGS
### # TEMPORARY DEBUG SETTINGS START
### # END OF TEMP DEBUG SETTINGS


def parse_arguments(arg: str=ARGUMENTS['arguments']) -> list:
        if arg:
                argument_list = arg.split(',')
                return argument_list

def help() -> None:
        action_list = { 'create': { 
                                'Student': 'name_uq,group_id',
                                'Group': 'name_uq',
                                'Tutor': 'name_uq',
                                'Subject': 'name_uq,tutor_id_fk',
                                'Mark': 'mark_value,student_id_fk,subject_id_fk,date'
                        },
                        'list': {
                                'Student': '',
                                'Group': '',
                                'Tutor': '',
                                'Subject': '',
                                'Mark': ''                                
                        },
                        'update': {
                                'Student': 'id,name_uq,group_id',
                                'Group': 'id,name_uq',
                                'Tutor': 'id,name_uq',
                                'Subject': 'id,name_uq,tutor_id_fk',
                                'Mark': 'id,mark_value,student_id_fk,subject_id_fk,date'                                
                        },
                        'delete': {
                                'Student': 'id',
                                'Group': 'id',
                                'Tutor': 'id',
                                'Subject': 'id',
                                'Mark': 'id'                                
                        }                                                
        }
        # print(f'For action {action, model} use the following arguments and structure: {action_list[action][model]}')
        print(action_list)



relation_list = {
                'Student': Student,
                'Group': Group,
                'Tutor': Tutor,
                'Subject': Subject,
                'Mark': Mark
}


def create_grtut(argument_list: list) -> None:
        row = relation_list[ARGUMENTS["model"]](name_uq=argument_list[0])
        session.add(row)
        session.commit()
        print(f'CREATED: {row}')

def create_stud(argument_list: list) -> None:
        row = relation_list[ARGUMENTS["model"]](name_uq=argument_list[0], group_id=argument_list[1])
        session.add(row)
        session.commit()
        print(f'CREATED: {row}')

def create_sub(argument_list: list) -> None:
        row = relation_list[ARGUMENTS["model"]](name_uq=argument_list[0], tutor_id_fk=argument_list[1])
        session.add(row)
        session.commit()
        print(f'CREATED: {row}')

def create_mark(argument_list: list) -> None:
        row = relation_list[ARGUMENTS["model"]](mark_value=argument_list[0], student_id_fk=argument_list[1], subject_id_fk=argument_list[1], today_date=argument_list[1])
        session.add(row)
        session.commit()
        print(f'CREATED: {row}')


def list_anything(*_) -> None:
        table_names = {
                'Student': 'students',
                'Group': 'groups',
                'Tutor': 'tutors',
                'Subject': 'subjects',
                'Mark': 'marks'
        }
        sql = text(f'SELECT * FROM {table_names[ARGUMENTS["model"]]}')
        result = session.execute(sql)
        data = result.fetchall()
        print(data)


def update_grtut(argument_list: list) -> None:
        row = session.query(relation_list[ARGUMENTS["model"]]).get(argument_list[0])
        try:
                row.name_uq = argument_list[1]
        except:
                ...
        else:
                session.add(row)
                session.commit()
                print(f'UPDATED WITH: {row}')

def update_stud(argument_list: list) -> None:
        row = session.query(relation_list[ARGUMENTS["model"]]).get(argument_list[0])
        try: 
                row.name_uq = argument_list[1]
        except:
                ...    
        try:
                row.group_id = argument_list[2]
        except:
                ...
        session.add(row)
        session.commit()
        print(f'UPDATED WITH: {row}')

def update_subj(argument_list: list) -> None:
        row = session.query(relation_list[ARGUMENTS["model"]]).get(argument_list[0])
        try:
                row.name_uq = argument_list[1]
        except:
                ...
        try:
                row.tutor_id_fk = argument_list[2]
        except:
                ...
        session.add(row)
        session.commit()
        print(f'UPDATED WITH: {row}')

def update_mark(argument_list: list) -> None:
        row = session.query(relation_list[ARGUMENTS["model"]]).get(argument_list[0])
        try:
                row.mark_value = argument_list[1]
        except:
                ...
        try:
                row.student_id_fk = argument_list[2]
        except:
                ...
        try:
                row.subject_id_fk = argument_list[3]
        except:
                ... 
        try:
                row.date = argument_list[4]
        except:
                ... 
   
        session.add(row)
        session.commit()
        print(f'UPDATED WITH: {row}')


def delete_anything(argument_list: list) -> None:
        table = relation_list[ARGUMENTS["model"]]
        row = session.query(table).filter(table.id_pk == argument_list[0]).one_or_none()
        if row:
                session.delete(row)
                session.commit()
                print('C:// has been formatted!')
        else:
                print('NOT FOUND!')


create_methods = {
                'Student': create_stud,
                'Group': create_grtut,
                'Tutor': create_grtut,
                'Subject': create_sub,
                'Mark': create_mark
        }

update_methods = {
                'Student': update_stud,
                'Group': update_grtut,
                'Tutor': update_grtut,
                'Subject': update_subj,
                'Mark': update_mark
        }


if __name__ == '__main__':
        argument_list = parse_arguments()

        if ARGUMENTS['operation'].casefold() == 'create':
                create_methods[ARGUMENTS['model']](argument_list)
        elif ARGUMENTS['operation'].casefold() == 'list':
                list_anything(argument_list)
        elif ARGUMENTS['operation'].casefold() == 'update':
                update_methods[ARGUMENTS['model']](argument_list)
        elif ARGUMENTS['operation'].casefold() == 'delete':
                delete_anything(argument_list)
        else:
                help()
                print('WRONG operation! EXITING!')