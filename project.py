from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem


# Set up the database session object
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurantList.html', restaurants = restaurants)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	return render_template('menu.html', 
							restaurant = restaurant, 
							menu_items = menu_items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['POST', 'GET'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

	if request.method == 'POST':
		menu_item = MenuItem(name = request.form['name'], 
							 restaurant_id = restaurant_id)
		session.add(menu_item)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

	if request.method == 'GET':
		return render_template('newMenuItem.html', restaurant = restaurant)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	menu_item = session.query(MenuItem).filter_by(id = menu_id).one()

	if request.method == 'GET':
		return render_template('editMenuItem.html', 
							   menu_item = menu_item,
							   restaurant_id = restaurant_id)

	if request.method == 'POST':
		menu_item.name = request.form['name']
		menu_item.description = request.form['description']
		menu_item.price = request.form['price']
		session.add(menu_item)
		session.commit()
		flash('Menu Item: {} Edited'.format(menu_item.name))
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	menu_item = session.query(MenuItem).filter_by(id = menu_id).one()

	if request.method == 'GET':
		return render_template('deleteMenuItem.html', 
								menu_item = menu_item, 
								restaurant = menu_item.restaurant)

	if request.method == 'POST':
		session.delete(menu_item)
		session.commit()
		flash('Menu Item: {} Deleted'.format(menu_item.name))
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

# Make an endpoint GET request
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems = [i.serialize for i in menu_items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/JSON')
def menuItem(restaurant_id, menu_item_id):
	menu_item = session.query(MenuItem).filter_by(id = menu_item_id).one()
	return jsonify(MenuItem = menu_item.serialize)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)

