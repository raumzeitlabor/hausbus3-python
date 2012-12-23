from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import json
import sys
import os
import mimetypes
import ssl
import threading
import time
import mosquitto

bus_id = ""
features = { "http": {}, "https": {}, "mqtt": {}}
variables = {}
base_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
running = False
mqtt = None
http_server = None
https_server = None

class HausbusHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == "/_/state":
			self.sendJSON(variables)
		elif self.path.startswith("/_/state/"):
			variable_name = self.path.replace("/_/state/","",1)
			if variable_name in compactVariables():
				self.sendJSON({variable_name: _compactVariables()[variable_name]})
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
	thread = None
	
	def startThread(self):
		thread = threading.Thread(target=self.serve_forever)
		thread.start()

# Basic self monitoring infos on the api
def self_monitoring():
	variables["system"] = {}
	variables["system"]["id"] = bus_id
	while running:
		variables["system"]["features"] = features
		f = open('/proc/uptime', 'r')
		variables["system"]["uptime"] = f.readline().split()[0]
		f.close
		f = open('/proc/loadavg', 'r')
		loadavg = f.readline().split()
		variables["system"]["loadavg"] = loadavg[0] + " " + loadavg[1] + " " + loadavg[2]
		f.close()
		publish("system")
		time.sleep(10)
		

# Default entry point for hausbus2 server applications. Starts up a
# HTTP server, and HTTPS server if it gets the configuration settings.
# See example.py for an example
def start(devicename, http_port=None, https_port=None, keyfile=None, certfile=None, mqtt_broker=None):
	global bus_id, running, features, http_server, https_server
	
	bus_id = devicename
	
	running = True
	
	# Start HTTP server
	if http_port != None:
		features["http"]["enabled"] = True
		features["http"]["port"] = http_port
		http_server = HTTPServerV6(('::', http_port,0,0), HausbusHandler)
		http_server.startThread()
	
	# Start HTTPS server, if required
	if https_port != None:
		features["https"]["enabled"] = True
		features["https"]["port"] = https_port
		https_server = HTTPServerV6(('::', https_port,0,0), HausbusHandler)
		https_server.socket = ssl.wrap_socket(https_server.socket, keyfile=keyfile, certfile=certfile, server_side=True)
		https_server.startThread()
	
	# Start MQTT client
	if mqtt_broker != None:
		features["mqtt"]["enabled"] = True
		features["mqtt"]["port"] = mqtt_broker
		mqtt_init(mqtt_broker)
		
	# Start selfmonitoring thread
	monitor_thread = threading.Thread(target=self_monitoring)
	monitor_thread.start()
	
	print >> sys.stderr, 'started Hausbus2 server.'


def stop():
	global running
	running = False
	if features["http"]["enabled"]:	# shutdown HTTP server
		http_server.shutdown()
	if features["https"]["enabled"]:	# shutdown	 HTTPS server if running
		https_server.shutdown()
		https_server.socket.close()
	if features["mqtt"]["enabled"]:
		mqtt.publish("/monitor", json.dumps({"event": "service_shutdown","device": bus_id}), 1)
		mqtt.disconnect()
	
	
def mqtt_init(broker):
	global mqtt
	
	if not hasattr(mosquitto.Mosquitto, "loop_forever"):
		print >> sys.stderr, "Your python mosquitto library is too old. Use v16 or higher. Disabling MQTT integtration."
		features["mqtt"]["enabled"] = False
	else:
		mqtt = mosquitto.Mosquitto(bus_id, clean_session=False)
		mqtt.will_set(topic="/monitor", payload=json.dumps({"event": "unexpected_disconnect","device": bus_id}))
		mqtt.connect(broker)
		mqtt.subscribe("/device/"+bus_id+"/control", 2)
		#mqtt.on_message = on_message
		threading.Thread(target=mqtt.loop_forever).start()

def mqtt_publish(major_key):
	if features["mqtt"]["enabled"]:
		output = variables[major_key].copy()
		output["_timestamp"] = time.time()
		mqtt.publish("/device/"+bus_id+"/"+major_key, json.dumps(output), 1)

def publish(major_key):
	mqtt_publish(major_key)
	
# Update a hausbus variable, and publish it automatically (or not)
def update(major_key, minor_key, value, auto_publish = True):
	if not major_key in variables:
		variables[major_key] = {}
	
	variables[major_key][minor_key] = value

	if auto_publish:
		publish(major_key)

def _compactVariables():
	out = {}
	for major_key,minor_variables in variables.items():
		for minor_key,value in minor_variables.items():
			out[major_key + "." + minor_key] = value
	return out
