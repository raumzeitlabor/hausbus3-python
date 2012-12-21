#!/usr/bin/python

# Import the Hausbus2 module
import hausbus2

# Set variables to be served via the Hausbs2 Server
hausbus2.variables["temperature"] = {}
hausbus2.variables["temperature"]["olymp"] = 23.70
hausbus2.variables["temperature"]["kueche"] = 25.20
hausbus2.variables["temperature"]["eecke"] = 23.40

hausbus2.variables["io_ports"] = {}
hausbus2.variables["io_ports"]["A"] = "11001101"
hausbus2.variables["io_ports"]["B"] = "10001110"
hausbus2.variables["io_ports"]["C"] = "01010100"

hausbus2.variables["pinpad"] = {}
hausbus2.variables["pinpad"]["door"] = "locked"
hausbus2.variables["pinpad"]["lastsync"] = 1321819942
hausbus2.variables["pinpad"]["wrongpins"] = 3
hausbus2.variables["pinpad"]["msg"] = "Willkommen im RZL"

# start the Hausbus2 server on port 8080
hausbus2.start(8080, https_port=4443, keyfile='example.key', certfile='example.crt')
