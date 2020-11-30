import json

devices = '{"devices":[{"id":1046}]}'

object = json.dumps(devices)
print(object)

with open('devices.json', 'w') as outfile:
	json.dump(object, outfile)

