from flask import Flask, render_template, redirect, url_for, request, jsonify
import db_controller


app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = db_controller.get_restaurants()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/add/', methods = ['GET', 'POST'])
def addRestaurant():
	if request.method == 'GET':
		return render_template('addRestaurant.html')
	if request.method == 'POST':
		db_controller.create_restaurant(request.form['name'])
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = db_controller.get_restaurant(restaurant_id)
	if request.method == 'GET':
		return render_template('editRestaurant.html', restaurant = restaurant)
	if request.method == 'POST':
		db_controller.update_restaurant(restaurant.id, request.form['name'])
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = db_controller.get_restaurant(restaurant_id)
	if request.method == 'GET':
		return render_template('deleteRestaurant.html', restaurant = restaurant)
	if request.method == 'POST':
		db_controller.delete_restaurant(restaurant.id)
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showRestaurantMenu(restaurant_id):
	restaurant = db_controller.get_restaurant(restaurant_id)
	menu_items = db_controller.get_menu_items_by_restaurant(restaurant_id)
	return render_template('menu.html', menu_items = menu_items, restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/add/', methods = ['GET', 'POST'])
def addMenuItem(restaurant_id):
	if request.method == 'GET':
		return render_template('addMenuItem.html', restaurant = restaurant)
	if request.method == 'POST':
		db_controller.create_menu_item(
			name = request.form['name'],
			description = request.form['description'],
			price = request.form['price'],
			course = request.form['course'],
			restaurant_id = restaurant_id)
		return redirect(url_for('showRestaurantMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_item_id):
	menu_item = db_controller.get_menu_item(menu_item_id)

	if request.method == 'GET':
		return render_template('editMenuItem.html', restaurant = restaurant, menu_item = menu_item)
	if request.method == 'POST':
		db_controller.update_menu_item(
			menu_item_id = menu_item_id, 
			name = request.form['name'],
			description = request.form['description'],
			price = request.form['price'],
			course = request.form['course'])
		return redirect(url_for('showRestaurantMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_item_id):
	restaurant = db_controller.get_restaurant(restaurant_id)
	menu_item = db_controller.get_menu_item(menu_item_id)

	if request.method == 'GET':
		return render_template('deleteMenuItem.html', restaurant = restaurant, menu_item = menu_item)

	if request.method == 'POST':
		db_controller.delete_menu_item(menu_item_id)
		return redirect(url_for('showRestaurantMenu', restaurant_id = restaurant_id))

########## JSON API Endpoints ##########
@app.route('/restaurants/JSON')
def showRestaurantsJSON():
	restaurants = db_controller.get_restaurants()
	return jsonify(restaurants = [r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showRestaurantMenuJSON(restaurant_id):
	menu_items = db_controller.get_menu_items_by_restaurant(restaurant_id)
	return jsonify(menu_items = [i.serialize for i in menu_items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/JSON')
def showRestaurantMenuItemJSON(restaurant_id, menu_item_id):
	menu_item = db_controller.get_menu_item(menu_item_id)
	return jsonify(menu_item = menu_item.serialize)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
