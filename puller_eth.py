import pysftp
from datetime import datetime
import os
import scp as SCPClient
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

flag = 0
previous_stamp = ''

class PullerEth:

	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(11, GPIO.IN)

		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None

		destination = ""

		flag = 0
		previous_stamp = ''

	#Establishes connection with CloudGate and retrieves lvm service log 01
	#TODO: have pysft 'roam' for connection with CG - prevent timeouts
	def pull(self, unit):
		print("Establishing connection with Cloudgate...")
		sftp = pysftp.Connection('192.168.1.1', username='admin', password='Metro123!', cnopts=cnopts)
		#Read JSON Config File for Unit No.
		print("Finding unit number...")
		#sftp.get('mnt/data/lvm/config.json', preserve_mtime=True)
		#with open('config.json', 'r') as configfile:
		#	lines = configfile.readlines()
		#Find Unit No.
		now = datetime.now()
		timestamp = now.strftime('%Y-%m-%d-%H')

		destination = 'logs/' + str(unit) + '/' + timestamp + ".txt"
		sftp.get('mnt/data/lvm/logs/lvm-service-log-01.txt', destination)

		print("Complete")
		sftp.close()
		return timestamp

	def getDest(self):
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
