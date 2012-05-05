#!/usr/bin/python

# Import the Hausbus2 module
import hausbus2

# Set variables to be served via the Hausbs2 Server
hausbus2.variables["temperature"] = {}
hausbus2.variables["temperature"]["olymp"] = 23.70
hausbus2.variables["temperature"]["kueche"] = 25.20
hausbus2.variables["temperature"]["eecke"] = 23.40

# start the Hausbus2 server on port 8080
hausbus2.start(8080)
