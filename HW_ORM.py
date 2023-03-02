import sqlalchemy
from sqlalchemy.orm import sessionmaker

from settings import PASSWORD
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = f'postgresql://postgres:{PASSWORD}@localhost:5432/HWORM'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()




session.close()