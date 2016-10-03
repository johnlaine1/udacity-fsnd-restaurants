from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def get_restaurants():
	""" Get all restaurants """
	restaurants = session.query(Restaurant).all()
	return restaurants

def create_restaurant(name):
	restaurant = Restaurant(name = name)
	session.add(restaurant)
	session.commit()
	return restaurant

def get_restaurant(id):
	restaurant = session.query(Restaurant).filter(Restaurant.id == id).one()
	return restaurant

def update_restaurant(id, name):
	restaurant = get_restaurant(id)
	restaurant.name = name
	session.add(restaurant)
	session.commit()

def delete_restaurant(id):
	restaurant = get_restaurant(id)
	session.delete(restaurant)
	session.commit()

def get_menu_items_by_restaurant(restaurant_id):
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return items

def get_menu_item(menu_item_id):
	item = session.query(MenuItem).filter_by(id = menu_item_id).one()
	return item

def create_menu_item(name, description, price, course, restaurant_id):
	item = MenuItem(name = name, description = description, price = price, course = course, restaurant_id = restaurant_id)
	session.add(item)
	session.commit()
	return item

def update_menu_item(menu_item_id, name, description, price, course):
	item = session.query(MenuItem).filter_by(id = menu_item_id).one()
	item.name = name
	item.description = description
	item.price = price
	item.course = course
	session.add(item)
	session.commit()

def delete_menu_item(menu_item_id):
	item = session.query(MenuItem).filter_by(id = menu_item_id).one()
	session.delete(item)
	session.commit()