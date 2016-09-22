import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import Base, Restaurant, MenuItem

pp = pprint.PrettyPrinter(indent=4)

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

r = session.query(Restaurant)
m = session.query(MenuItem)

# items = m.all()
# for item in items:
# 	print "Name: {} \n Price: {}".format(item.name, item.price)

# print firstResult.name, firstResult.id

for instance in r.order_by(Restaurant.name):
	print instance.name
