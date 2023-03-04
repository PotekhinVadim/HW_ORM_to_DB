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

condition = Publisher.id == input("Введите id издателя ")
q = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).\
    join(Publisher).join(Stock).join(Sale).join(Shop).\
        filter(condition).order_by(Sale.date_sale)
for book, shop, price, count, date in q:
        print(f'{book:<40} | {shop:<10} | {price*count:<8} | {date}')