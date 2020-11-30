import pysftp
from datetime import datetime
import os
import scp as SCPClient
import time
import requests
import json
from paramiko.client import SSHClient
from paramiko import AutoAddPolicy

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

flag = 0
previous_stamp = ''

#*********PARAMETERS***********#
authKeyId = 'keyId-hYuSNmbpQxVNNJAYKpdhdnrCCENwcYwo'
authKey = 'q5kLkxJJTkRNwZ70mglXRVks4tznBNJgiLszIUMlVBJw69jaZ5N1mHrpp3ndKyTT'
api_endpoint = 'https://g.api.soracom.io/v1/'
imsiTarget = 295050911071568
portTarget = 22
duration_min = 30
tlsBool = True
#source_ip_cidr = null
#******************************#
edge_devices = [1046]


def authenticate_to_soracom(authKeyId, authKey, api_endpoint):
		headerString = {'Content-Type': 'application/json', 'Accept': 'application/json'}
		bodyDict = {'authKeyId': authKeyId, 'authKey': authKey}

		http_response = requests.post(api_endpoint+'auth', headers = headerString, data = json.dumps(bodyDict))

		return http_response

def unpack_authentication_response(http_response):
	json_response = json.loads(http_response.text)
	auth_dict = {
		'apiKey': json_response['apiKey'],
		'apiToken':json_response['token'],
		'apiOperatorId': json_response['operatorId'],
		'apiUsername': json_response['userName']
	}
	return auth_dict

def append_tunnel(dict):
	tunnel_object = json.dumps(dict)
	print(tunnel_object)
	with open('tunnels.json', 'w') as outfile:
		json.dump(tunnel_object, outfile)

def create_napter_tunnel(auth_dict, imsi_target, port_target, duration_min, tls_bool, *args):
	headerString = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'X-Soracom-API-Key': auth_dict['apiKey'],
		'X-Soracom-Token': auth_dict['apiToken']
		}
	bodyDict = {
		'destination': {
			'imsi': imsi_target,
			'port': port_target
		},
		'duration': duration_min,
		'tlsRequired': tls_bool
	  }
	http_response = requests.post(api_endpoint+'port_mappings', headers = headerString, data = json.dumps(bodyDict))
	napter_dict = json.loads(http_response.text)

	append_tunnel(napter_dict)
	return napter_dict

	#Establishes connection with CloudGate and retrieves lvm service log 01
	#TODO: have pysft 'roam' for connection with CG to prevent timeouts
	#TODO: Catch Paramiko exceptions
def pull(unit):

	with open('tunnels.json', 'r') as f:
		lines = f.readlines()

	#host = lines[0][19:33]
	#portnumber =int(lines[0][47:52])
	host = '44.240.187.181'
	portnumber = '23674'
	#print(host)
	#print(portnumber)
	#print("connecting to " + host + " on port " + portnumber)

	print("connecting")
	#Establish connection

	client = SSHClient()
	#client.set_missing_host_key_policy(AutoAddPolicy())
	client.connect(hostname=host, port=portnumber, username='admin', password='Metro123!', banner_timeout=10000, auth_timeout=10000, timeout=10000)
	sftp = client.open_sftp()

	now = datetime.now()
	timestamp = now.strftime('%Y-%m-%d-%H')

	destination = 'logs/' + str(unit) + '/' + timestamp + ".txt"
	sftp.get('mnt/data/lvm/logs/lvm-service-log-01.txt', destination)

	print("Complete")
	sftp.close()
	#return destination

def getDest():
	return destination

class PullerRemote:

	def __init__(self):
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None

		flag = 0
		previous_stamp = ''

	def device_cycle(self, device_list):
		#cycle through edge devices
		#for unit in device_list:
			#tunnel(unit)
		http_response = authenticate_to_soracom(authKeyId, authKey, api_endpoint)
		auth_dict = unpack_authentication_response(http_response)
		napter_dict = create_napter_tunnel(auth_dict, imsiTarget, portTarget, duration_min, tlsBool)
		print(napter_dict)

		print("Created new tunnel")
		#pull(1046)

	#for one unit, checks if a Soracom tunnel is already open. opens one otherwise
	def tunnel(self, unit):
		print("hello")
		#check if a tunnel to device is already open
		#read napter dict file
		#is expired?
			#no -> call search 

		#Authenticate to Soracom API, retrieve temporary API token
		#http_response = authenticate_to_soracom(authKeyId, authKey, api_endpoint)
		#auth_dict = unpack_authentication_response(http_response)

		#napter_dict = create_napter_tunnel(auth_dict, imsiTarget, portTarget, duration_min, tlsBool)
		#save napter_dict and timestamp to file
		#print(napter_dict)

	def pull_test(self, unit):
		#self.device_cycle(unit)
		pull(unit)
