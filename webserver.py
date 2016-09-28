from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
import db_controller
import re


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):

		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ''
				output += '<html><body>'
				output += 'Hello World! - <a href="/hola">Go to Hola</a>'
				output += '<form method="POST" enctype="multipart/form-data" action="/hello">'
				output += '<h2>What would you like me to say?</h2><input name="message"'
				output += 'type="text"><input type="submit" value="Submit"></form>'
				output += '</body></html>'
				self.wfile.write(output)
				print 'do_GET /hello'
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ''
				output += '<html><body>'
				output += 'Hola World! - <a href="/hello">Go to Hello</a>'
				output += '<form method="POST" enctype="multipart/form-data" action="/hello">'
				output += '<h2>What would you like me to say?</h2><input name="message"'
				output += 'type="text"><input type="submit" value="Submit"></form>'
				output += '</body></html>'
				self.wfile.write(output)
				print 'do_GET /hola'
				return

			if self.path.endswith("/restaurants"):
				restaurants = ''
				for rest in db_controller.get_restaurants():
					restaurants += '<li>{}</li>'.format(rest.name)
					restaurants += '<a href="restaurants/{}/edit">Edit</a><br>'.format(rest.id)
					restaurants += '<a href="restaurants/{}/delete">Delete</a>'.format(rest.id)
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ''
				output += '<html><body>'
				output += '<h1>All Restaurants</h1>'
				output += '<ol>'
				output += restaurants
				output += '</ol>'
				output += '</body></html>'
				self.wfile.write(output)
				return

			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ''
				output += '<html><body>'
				output += '<form method="post" enctype="multipart/form-data" action="/restaurants/new">'
				output += '<label for="rest_name">Restaurant Name </label>'
				output += '<input type="text" name="rest_name">'
				output += '<input type="submit" value="Add Restaurant">'
				output += '</form>'
				output += '</body></html>'
				self.wfile.write(output)
				return

			if re.match(r'.*/restaurants/.*/edit', self.path):
				rest_id = self.path.split('/')[2]
				restaurant = db_controller.get_restaurant(rest_id)
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ''
				output += '<html><body>'
				output += '<h1>Edit the Restaurant name for {}</h1>'.format(restaurant.name)
				output += '<form method="post" enctype="multipart/form-data" action="/restaurants/{}/edit">'.format(rest_id)
				output += '<input type="text" name="rest_name" value="{}">'.format(restaurant.name)
				output += '<input type="submit" value="Update Restaurant Name">'
				output += '</form>'
				output += '</body></html>'
				self.wfile.write(output)				
				return

			if re.match(r'.*/restaurants/.*/delete', self.path):
				restaurant = db_controller.get_restaurant(self.path.split('/')[2])

				output = ''
				output += '<h2>Are you sure that you want to delete the restaurant named <strong>{}?</strong></h2>'.format(restaurant.name)
				output += '<form method="post" enctype="mutipart/form-data" action="/restaurants/{}/delete">'.format(restaurant.id)
				output += '<input type="submit" value="Delete {}">'.format(restaurant.name)
				output += '<form>'

				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404, "File Not Found {}".format(self.path))

	def do_POST(self):

		try:
			if re.match(r'.*/restaurants/.*/delete', self.path):
				restaurant = db_controller.get_restaurant(self.path.split('/')[2])

				db_controller.delete_restaurant(restaurant.id)
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return

			if re.match(r'.*/restaurants/.*/edit', self.path):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					rest_name = fields.get('rest_name')				
					rest_id = self.path.split('/')[2]
					restaurant = db_controller.get_restaurant(rest_id)								

					db_controller.update_restaurant(restaurant.id, rest_name[0])
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
				return

			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))				
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					rest_name = fields.get('rest_name')

					db_controller.create_restaurant(rest_name[0])
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

				return

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print "Web server is running on port {}".format(port)
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()


if __name__ == '__main__':
	main()