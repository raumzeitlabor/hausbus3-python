#!/usr/bin/python

# Import the Hausbus3 module
import hausbus3
import os, time

base_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))

# start the Hausbus2 server on port 8080
hausbus3.start("example", http_port=8080, https_port=4443, keyfile=base_path + '/example.key', certfile=base_path + '/example.crt', mqtt_broker = "127.0.0.1")

# Set variables to be served via the Hausbs3 Server
hausbus3.update("temperature","olymp", 23.70, False)
hausbus3.update("temperature", "kueche", 25.20, False)
hausbus3.update("temperature", "eecke", 23.40)

hausbus3.update("io_ports", "A", "11001101", False)
hausbus3.update("io_ports", "B", "10001110", False)
hausbus3.update("io_ports", "C", "01010100")

hausbus3.update("pinpad", "door", "locked", False)
hausbus3.update("pinpad", "lastsync", 1321819942, False)
hausbus3.update("pinpad", "wrongpins", 3, False)
hausbus3.update("pinpad", "msg", "Willkommen im RZL")

hausbus3.update("windows","state", [["x", "1", "x", "x", "0", "x", "x", "?", "x", "x", "?", "x"], ["x", "0", "0", "?", "0", "x", "x", "0", "?", "0", "0", "x"]])
try:
	while 1:
		time.sleep(10)
# Ctrl-C interupts our server magic
except KeyboardInterrupt:
	print '^C received, shutting down server'

hausbus3.stop()
