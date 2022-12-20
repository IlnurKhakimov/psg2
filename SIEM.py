import re, time, socket

# read() returns string, readlines() returns list
def getDif(old, new):
    with open(old, encoding="utf-8") as f:
        oldtxt = f.read()
    with open(new, encoding="utf-8") as f:
        newtxt = f.read()
    try:
        dif = newtxt.replace(oldtxt, '')
    except:
        dif = False
    return dif

file1=r"C:\authnew.log"
file2=r"C:\ssh.log"
dif = getDif(file1, file2)

# separate full string into a list of lines
def getLines(string):
    lines = string.split("\n")
    return lines
lines = getLines(dif)

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
attempts = dictSSH(lines)

# gets amount of try's in given dictionary of ip's and try's. returns list of hackers
def bruteDetect(attempts):
    hackers = []
    for user in attempts:
        if user['count'] > 9:
            print(f"BRUTEFORCE DETECTED!!! HACKER COMES FROM IP {user['ip']}")
            hackers.append(user['ip'])
    return hackers

def exportLogs(expTarget, expPort, file):
    ip = expTarget
    port = expPort
    soc = socket.socket()
    soc.connect((ip, port))
    fopen = open(file, "rb")
    line = fopen.read(1024)
    while line:
        soc.send(line)
        line = fopen.read(1024)
    fopen.close()
    soc.close()