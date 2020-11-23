import pysftp
from datetime import datetime
import os
import scp as SCPClient
import time
import requests
import json

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

flag = 0
previous_stamp = ''

#*********PARAMETERS***********#
authKeyId = 'keyId-hYuSNmbpQxVNNJAYKpdhdnrCCENwcYwo'
authKey = 'secret-q5kLkxJJTkRNwZ70mglXRVks4tznBNJgiLszIUMlVBJw69jaZ5N1mHrpp3ndKyTT'
api_endpoint = 'https://g.api.soracom.io/v1/'
imsiTarget = 295050911071572
portTarget = 22
duration_min = 30
tlsBool = True
#source_ip_cidr = null

edge_devices = [1046]

class PullerRemote:

	def __init__(self):
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None

		destination = ""

		flag = 0
		previous_stamp = ''

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

	def device_cycle(self):
		#cycle through edge devices
		#for unit in edge_devices:
		http_response = authenticate_to_soracom(authKeyId, authKey, api_endpoint)
		auth_dict = unpack_authentication_response(http_response)
		napter_dict = create_napter_tunnel(auth_dict, imsiTarget, portTarget, duration_min, tlsBool)
		print(napter_dict)

def authenticate_to_soracom(authKeyId, authKey, api_endpoint):
		headerString = {'Content-Type': 'application/json', 'Accept': 'application/json'}
		bodyDict = {'authKeyId': authKeyId, 'authKey': authKey}

		http_response = requests.post(api_endpoints+'auth', headers = headerString, data = json.dumps(bodyDict))

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
	#TODO: have pysft 'roam' for connection with CG - prevent timeouts
	#def pull(napter_dict):
		#print("Establishing connection with Cloudgate...")
		#sftp = pysftp.Connection('192.168.1.1', username='admin', password='Metro123!', cnopts=cnopts)
		##Read JSON Config File for Unit No.
		#print("Finding unit number...")
		#sftp.get('mnt/data/lvm/config.json', preserve_mtime=True)
		#with open('config.json', 'r') as configfile:
		#	lines = configfile.readlines()
		##Find Unit No.
		#unitn = lines[1][20:24]
		#os.remove('config.json')
		#now = datetime.now()
		#timestamp = now.strftime("%m-%d-%Y-%H:%M:%S")

		#destination = "bin/" + unitn + "-LVM-LOG-" + timestamp + ".txt"
		#sftp.get('mnt/data/lvm/logs/lvm-service-log-01.txt', destination)

		#print("Complete")
		#sftp.close()
		#return destination

def getDest():
	return destination

#Calls pull() after some interval indefinitely
#Much of this should live in the main routine
def loop(self):
	while 1:
		#wait for log reporting interval
		init_t = time.process_time()
		print(init_t)
		while time.process_time() - init_t < 5.0:
			print("waiting")
			print(time.process_time())

		#grab logfile
		file = pull()

		#find log timestamp
		with open(file) as lvm_current:
			lines= lvm_current.readlines()
		current_stamp = lines[0][x:x]

		#validate LVM log currency
		if flag == 0:
			new = 1
			previous_stamp = current_stamp
		else:
			if previous_stamp == current_stamp:
				new = 1
				current_stamp = previous_stamp
		if new == 1:
			#disable eth0
			os.system('sudo ifconfig eth0 down')

			#upload logfile

			#remove logfile

			#enable eth0
			os.system('sudo ifconfig eth0 up')
		flag = 1
		time.sleep(10)
