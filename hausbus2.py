from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

variables = {}

class HausbusHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == "/_/state":
			self.sendJSON(str(compactVariables()))
		elif self.path.startswith("/_/state/"):
			variable_name = self.path.replace("/_/state/","",1)
			if variable_name in compactVariables():
				self.sendJSON(str({variable_name:compactVariables()[variable_name]}))
			else:
				self.send404()
		else:
			self.send404()
		return
		
#	def do_POST(self):
#		self.send_response(200)
#		self.send_header('Content-type',	'text/html')
#		self.end_headers()
#		self.wfile.write("Post-Hello World")
#		return
		
	def send404(self):
		self.send_response(404)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write("File not found! - RZL Hausbus2 Python Server\n")
		return
	
	def sendJSON(self, json):
		self.send_response(200)
		self.send_header('Content-type', 'text/json')
		self.end_headers()
		self.wfile.write(json + "\n")
		return

def start(port):
	try:
		server = HTTPServer(('', port), HausbusHandler)
		print 'started Hausbus2 server...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

def compactVariables():
	out = {}
	for major_key,minor_variables in variables.items():
		for minor_key,value in minor_variables.items():
			out[major_key + "." + minor_key] = value
	return out
