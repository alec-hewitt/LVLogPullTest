import json


new_device = '{"id": 10}'

f = open('devices.json', "r")

data = json.loads(f.read())
print(data)

devices = data["devices"]

#devices.append(new_device)
