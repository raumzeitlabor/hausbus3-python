#!/usr/bin/python

# Import the Hausbus2 module
import hausbus2
import os, time

base_path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))

# start the Hausbus2 server on port 8080
hausbus2.start("example", http_port=8080, https_port=4443, keyfile=base_path + '/example.key', certfile=base_path + '/example.crt', mqtt_broker = "127.0.0.1")

# Set variables to be served via the Hausbs2 Server
hausbus2.update("temperature","olymp", 23.70, False)
hausbus2.update("temperature", "kueche", 25.20, False)
hausbus2.update("temperature", "eecke", 23.40)

hausbus2.update("io_ports", "A", "11001101", False)
hausbus2.update("io_ports", "B", "10001110", False)
hausbus2.update("io_ports", "C", "01010100")

hausbus2.update("pinpad", "door", "locked", False)
hausbus2.update("pinpad", "lastsync", 1321819942, False)
hausbus2.update("pinpad", "wrongpins", 3, False)
hausbus2.update("pinpad", "msg", "Willkommen im RZL")

hausbus2.update("windows","state", [["x", "1", "x", "x", "0", "x", "x", "?", "x", "x", "?", "x"], ["x", "0", "0", "?", "0", "x", "x", "0", "?", "0", "0", "x"]])
try:
	while 1:
		time.sleep(10)
# Ctrl-C interupts our server magic
except KeyboardInterrupt:
	print '^C received, shutting down server'

hausbus2.stop()
