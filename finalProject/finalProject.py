from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	return 'This page will show all the restaurants'

@app.route('/restaurant/add')
def addRestaurant():
	return 'This page will contain a form to create a new restaurant'

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
	return 'This page will contain a form to edit a restaurant. restaurant_id: {}'.format(restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	return 'This page will contain a form (probably just a button really) to delete a restaurant. restaurant_id: {}'.format(restaurant_id)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showRestaurantMenu(restaurant_id):
	return 'This page will show a restaurant menu. restaurant_id: {}'.format(restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/add')
def addMenuItem(restaurant_id):
	return 'This page will contain a form to add a menu item. restaurant_id: {}'.format(restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/edit')
def editMenuItem(restaurant_id, menu_item_id):
	return 'This page will contain a form to edit a menu item. restaurant_id: {}, menu_item_id: {}'.format(restaurant_id, menu_item_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/delete')
def deleteMenuItem(restaurant_id, menu_item_id):
	return 'This page will contain a form to delete a menu item. restaurant_id: {}, menu_item_id: {}'.format(restaurant_id, menu_item_id)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
