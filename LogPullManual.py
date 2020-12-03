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



def pull():
	print("Establishing connection with Cloudgate...")
	sftp = pysftp.Connection('192.168.1.1', username='admin', password='Metro123!', cnopts=cnopts)
	#Read JSON Config File for Unit No.
	print("Finding unit number...")
	sftp.get('mnt/data/lvm/config.json', 'config.txt')
	with open('config.txt', 'r') as configfile:
		lines = configfile.readlines()
	#Find Unit No.
	unitn = lines[0][18:22]
	os.remove('config.txt')
	now = datetime.now()
	timestamp = now.strftime("_%m-%d-%Y")
	#if a root directory has not been defined:
	root_dir = "V3cLogs_" + timestamp
	direc = root_dir + "/" + unitn + timestamp

	direc2 = logs + "/" + unitn
	osmakedirs(direc2)
	timee = now.strftime('%Y-%m-%d-%H')
	sftp.get('mnt/data/lvm/logs/lvm-service-log-01.txt', direc2 + '/timee.txt')

	print("Creating Local Directories...")
	#Check if directory exists
	if not os.path.exists(direc):
		os.makedirs(direc)
		exists = 0
	else:
		exists = 1
		print("A Log Directory for this Unit " + unitn + " Already Exists! Please Check and Try Again")

	if exists == 0:
		system_logs_local = direc + "/System_Logs/"
		lvm_logs_local = direc + "/LVM_Logs/"
		#Create Subfolders
		os.makedirs(system_logs_local)
		os.makedirs(lvm_logs_local)
		print("Collecting System Logs...")
		#Collect System Logs
		sftp.get_d('log/', system_logs_local, preserve_mtime=True)
		#Collect LVM Logs
		print("Collecting LVM Logs...")
		sftp.get_d('mnt/data/lvm/logs/', lvm_logs_local, preserve_mtime=True)
		#Collect Config File
		print("Collecting Config File...")
		sftp.get('mnt/data/lvm/config.json', direc+'/config.json')

		print("COMPLETE")

	print("Connection Terminated")
	sftp.close()

#Begins a new directory for logs and removes old
def reset():
	now = datetime.now()
	timestamp = now.strftime("%m-%d-%Y")
	#set current root directory for logs set
	root_dir = "V3cLogs_" + timestamp
	#create directory
	os.makedirs("logs/" + root_dir)

while 1:
	flag = 0
	flag1 = 0
	pull_count = 0
	reset_count = 0
	for i in range(20):
		#check for new log set request
		time.sleep(0.01)
		pull_count = pull_count + GPIO.input(11)
	if pull_count == 20 and flag == 0:
		flag = 1
		pull()
	if GPIO.input(11) == 0 and flag == 1:
		flag = 0

