from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
DBsession = sessionmaker(bind=engine)
session = DBsession()