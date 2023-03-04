import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from settings import PASSWORD
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = f'postgresql://postgres:{PASSWORD}@localhost:5432/HWORM'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('book_data.json', 'r') as bd:
    data = json.load(bd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()
session.close()

subq = session.query(Publisher).filter(Publisher.id == input("Введите id издателя ")).subquery()
q = session.query(Book).join(subq, Book.id == subq.c.id_publisher)
for s in q.all():
    print(s.id, s.title)
    for p in s.publisher:
        print("\t", p.id, p.name)

# subq = session.query(Homework).filter(Homework.description.like("%сложн%")).subquery("simple_hw")
# q = session.query(Course).join(subq, Course.id == subq.c.course_id)
# print(q)
# for s in q.all():
#     print(s.id, s.name)
#     for hw in s.homeworks:
#         print("\t", hw.id, hw.number, hw.description)
