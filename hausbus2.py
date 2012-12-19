from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import json
from sys import exit
import os
import mimetypes

variables = {}

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
		elif os.path.isfile("htdocs" + self.path):
			self.serveHtdocs()
		elif os.path.isfile("htdocs" + self.path +"index.html"):
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
		self.send_response(200)
		(mtype, encoding) = mimetypes.guess_type('htdocs' + self.path)
		self.send_header('Content-type', mtype)
		f = open('htdocs' + self.path, 'rb')
		
		fs = os.fstat(f.fileno())
		self.send_header("Content-Length", str(fs[6]))
		self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
		self.send_header("Cache-Control", "public, max-age=86400")
		self.end_headers()
		self.wfile.write(f.read())
		return

class HTTPServerV6(HTTPServer):
	address_family = socket.AF_INET6

def start(port):
	try:
		server = HTTPServerV6(('::', port,0,0), HausbusHandler)
		print 'started Hausbus2 server...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()
		exit(1)

def compactVariables():
	out = {}
	for major_key,minor_variables in variables.items():
		for minor_key,value in minor_variables.items():
			out[major_key + "." + minor_key] = value
	return out
