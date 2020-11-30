import pysftp
import json
import os
import time

with open('tunnels.json', 'r') as file:
	lines = file.readlines()
ip = lines[0][19:33]
print(ip)
port = lines[0][47:52]
print(port)
