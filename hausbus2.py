from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import json
from sys import exit
import os
import mimetypes
import ssl
import threading

variables = {}
base_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))

class HausbusHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == "/_/state":
			self.sendJSON(variables)
		elif self.path.startswith("/_/state/"):
			variable_name = self.path.replace("/_/state/","",1)
			if variable_name in compactVariables():
				self.sendJSON({variable_name:compactVariables()[variable_name]})
			else:
				self.send404()
		elif os.path.isfile(base_path + "/htdocs" + self.path):
			self.serveHtdocs()
		elif os.path.isfile(base_path + "/htdocs" + self.path +"index.html"):
			self.path = self.path + "index.html"
			self.serveHtdocs()
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
	
	def sendJSON(self, content):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps(content) + "\n")
		return
		
	def serveHtdocs(self):
		file_path = base_path + "/htdocs" + self.path
		self.send_response(200)
		(mtype, encoding) = mimetypes.guess_type(file_path)
		self.send_header('Content-type', mtype)
		f = open(file_path, 'rb')
		
		fs = os.fstat(f.fileno())
		self.send_header("Content-Length", str(fs[6]))
		self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
		self.send_header("Cache-Control", "public, max-age=86400")
		self.end_headers()
		self.wfile.write(f.read())
		return

# HTTP server with IPv4 and IPv6 capability
class HTTPServerV6(HTTPServer):
	address_family = socket.AF_INET6

# Default entry point for hausbus2 server applications. Starts up a
# HTTP server, and HTTPS server if it gets the configuration settings.
# See example.py for an example
def start(http_port, https_port=None, keyfile=None, certfile=None):
	try:
		# Start HTTP server
		http_server = HTTPServerV6(('::', http_port,0,0), HausbusHandler)
		threading.Thread(target=http_server.serve_forever).start()
		
		# Start HTTPS server, if required
		if https_port != None:
			https_server = HTTPServerV6(('::', https_port,0,0), HausbusHandler)
			https_server.socket = ssl.wrap_socket(https_server.socket, keyfile=keyfile, certfile=certfile, server_side=True)
			threading.Thread(target=https_server.serve_forever).start()
			
		print 'started Hausbus2 server.'
		
		while 1:
			pass

	# Ctrl-C interupts our server magic
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		http_server.shutdown()	# shutdown HTTP server
		if https_port != None:	# shutdown HTTPS server if running
			https_server.shutdown()
			
		exit(1)

def compactVariables():
	out = {}
	for major_key,minor_variables in variables.items():
		for minor_key,value in minor_variables.items():
			out[major_key + "." + minor_key] = value
	return out
