import re, time, socket, pyinotify, threading, pickle
from datetime import datetime

exportTargetIP = str(input("Enter C2 IP here: "))
protectedFiles = ["/home/kali/Desktop/important/secret.txt"]
while True:
    ui = str(input("Enter full path of files you wish to protect here or press 2 for exit: "))
    if ui == "2":
        print("\nProceeding protecting your files\n")
        break
    else:
        protectedFiles.append({ui})

# read() returns string, readlines() returns list
def getDifInTime(file, seconds):
    with open(file, encoding="utf-8") as f:
        oldtxt = f.read()
    time.sleep(seconds)
    with open(file, encoding="utf-8") as f:
        newtxt = f.read()
    try:
        dif = newtxt.replace(oldtxt, '')
    except:
        dif = False
    return dif

# separate full string into a list of lines
def getLines(string):
    lines = string.split("\n")
    return lines


def getIpFrom(string):
    ipPatern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    ip = ipPatern.search(string)[0]
    return ip

def repSsh(lines):
    sshList = []
    for line in lines:
        if "sshd" in line:
            sshList.append(line)
    return sshList

# return a list of dicts with ip and amount of attempts to ssh
def dictSSH(lines):
    sshList = repSsh(lines)
    brute = []
    for attempt in sshList:
        if "Failed password" in attempt:
            brute.append(attempt)

    # get all ip's from given list
    allConnectors = []
    for attempt in brute:
        agent = getIpFrom(attempt)
        allConnectors.append(agent)

    # retreive unique ip's
    uniqueConnectors = []
    for connector in allConnectors:
        if connector not in uniqueConnectors:
            uniqueConnectors.append(connector)
    
    # count occurence of unique ip in total ip's list
    ipAttemtps = []
    for connector in uniqueConnectors:
        count = allConnectors.count(connector)
        ipAttemtps.append({"ip":connector, "count": count})
    
    return ipAttemtps


# gets amount of try's in given dictionary of ip's and try's. returns list of probable hackers
def bruteDetect(attempts):
    hackers = []
    for user in attempts:
        if user['count'] > 20:
            prob = 1.0
            hackers.append({"ip":user['ip'], "prob":prob})
        elif user['count'] > 5:
            prob =  0.5
            hackers.append({"ip":user['ip'], "prob":prob})
        elif user['count'] > 2:
            prob = 0.2
            hackers.append({"ip":user['ip'], "prob":prob})
        
    return hackers

def exportWarning(expTarget, msg):
    ip = expTarget
    port = 10001
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.sendto(msg, (ip, port))
    soc.close()

# This function will be called whenever the file is opened
def my_event_handler(event):
    # Send the notification using notify-send
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exportTargetIP, port))
    time = datetime.now()
    dateformat = time.strftime("%d/%m/%Y %H:%M:%S")
    message = "{} | Bait file has been opened!".format(dateformat)
    s.send(bytes(message, "utf-8"))
   

def watchFile():
    # Set up a watch on the file
    wm = pyinotify.WatchManager()
    watch_mask = pyinotify.IN_OPEN
    notifier = pyinotify.Notifier(wm, default_proc_fun=my_event_handler)
    # select the files you want to monitor:
    for filepath in protectedFiles:
        wm.add_watch(filepath, watch_mask)
    print(f"Protecting files {protectedFiles}")
    notifier.loop()


def bruteforceReport():
    print("Bruteforce protection activated")
    while True:
        sshlog = r"/var/log/auth.log"
        dif = getDifInTime(sshlog, seconds = 20)
        if dif:
            lines = getLines(dif)
            listOfAttempts = dictSSH(lines)
            maybeHackers = bruteDetect(listOfAttempts)
            # print(maybeHackers)
            hackersInSTR = pickle.dumps(maybeHackers)
            # print(f"Pickle: {hackersInSTR}")
            exportWarning(exportTargetIP, hackersInSTR)




thread1 = threading.Thread(target = watchFile)
thread1.start()
thread2 = threading.Thread(target=bruteforceReport)
thread2.start()