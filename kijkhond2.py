import pyinotify
import socket
from datetime import datetime


# This function will be called whenever the file is opened
def my_event_handler(event):
    # Send the notification using notify-send
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5555))
    time = datetime.now()
    dateformat = time.strftime("%d/%m/%Y %H:%M:%S")
    message = "{} | Bait file has been opened!".format(dateformat)
    s.send(bytes(message, "utf-8"))
    #test message
    print("Test") 


# Set up a watch on the file
wm = pyinotify.WatchManager()
watch_mask = pyinotify.IN_OPEN
notifier = pyinotify.Notifier(wm, default_proc_fun=my_event_handler)
# select the files you want to monitor:
wm.add_watch("/home/reep/Documents/Project securit/belangrijk.txt", watch_mask)
wm.add_watch("/home/reep/Documents/Project securit/testfile.txt", watch_mask)

# Start the notifier
notifier.loop()


