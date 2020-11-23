import os
import time
from uploader import Uploader
from puller_remote import PullerRemote

puller = PullerRemote()
#uploader = Uploader()

destination = ""

#in loop...
#check for new logfile using timestamp method (&check for authorized timestamp)


#pull file
puller.device_cycle()

#disable LAN interface
#print("establishing internet connection on wlam0\n")
#os.system('sudo ifconfig eth0 down')
#time.sleep(10)

#upload file directory
#uploader.upload_logs('bin')


#delete last logfile


# delete logs
