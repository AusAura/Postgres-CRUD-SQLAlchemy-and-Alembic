# Postgres-CRUD-SQLAlchemy-and-Alembic
CLI CRUD is done in the main.py file. Uses currying.

- Uses a PostgreSQL.
- Uses Alembic for easy migrations.
- With sqlalchemy ORM, models for the DB were made.
- seed.py fills the database with the fake data (using Faker). Now by using models.
- my_select.py performs a series of queries using models. Queries are the same as were here: https://github.com/AusAura/PureSQL-sqlite3

### Usage:
Run the script in the CLI with selected operation and additional parameters

### Examples:
- py main.py -o list -m Student
- py main.py -o create -m Group -a REVO_DRINKERS
- py main.py -o delete -m Group -a 4
- py main.py -o create -m Subject -a 'Mortilogy',1
- py main.py -o update -m Subject -a 8,'Morti logy',2
- py main.py -o delete -m Subject -a 8

## Arguments:
- "-o", "--operation": (required=True) What to do? (create, list, update, remove)
- "-m", "--model": Select the model.
- "-a", "--arguments": Pass the set of arguments via comma (,).

## Required arguments for passing during each of the operations for each model:
1) **'create'**
- 'Student': 'name_uq,group_id'
- 'Group': 'name_uq'
- 'Tutor': 'name_uq'
- 'Subject': 'name_uq,tutor_id_fk',
- 'Mark': 'mark_value,student_id_fk,subject_id_fk,date'

2) **'list'**
- 'Student': ''
- 'Group': ''
- 'Tutor': ''
- 'Subject': ''
- 'Mark': ''                                
          
3) **'update'**
- 'Student': 'id,name_uq,group_id'
- 'Group': 'id,name_uq',
- 'Tutor': 'id,name_uq',
- 'Subject': 'id,name_uq,tutor_id_fk',
- 'Mark': 'id,mark_value,student_id_fk,subject_id_fk,date'                                

4) **'delete'**
- 'Student': 'id'
- 'Group': 'id'
- 'Tutor': 'id'
- 'Subject': 'id'
- 'Mark': 'id'                                
