import os
import time
from uploader import Uploader
from puller_remote import PullerRemote
from puller_eth import PullerEth
edge_devices = [1047]
#puller = PullerEth()
puller = PullerRemote()
uploader = Uploader()
timestamp = ''
#for remote method, the class function will just pull all
#device_cycle(edge_devices)
#for each unit:
#for unit in edge_devices:
path = 'logs/' + str(1047)
#os.system('sudo ifconfig eth0 up')
#time.sleep(10)
timestamp = puller.pull_test(1047)
#os.system('sudo ifconfig eth0 down')
#time.sleep(10)
#uploader.upload_logs(path, 1047, timestamp)

