import socket, pickle, threading

ip = "0.0.0.0"
def noTouching():
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen(5)
    print(f"\nStarting file protection on port {port}")
    while True:
        clientsocket, address = s.accept()
        print(f"DANGER!!! FILE PROTECTION: {address[0]} is touching your files! ")
        msg = clientsocket.recv(1024).decode("utf-8")
        print(f"{msg}\n")

def antiBrute():
    port = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    print(f"\nBruteForce protection ready for receiving on port {port}")

    while True:
        dataAddr = s.recvfrom(1024)
        msg = dataAddr[0]
        address = dataAddr[1]
        # print(f"Received connection from: {address}")
        msg = pickle.loads(msg)
        for hacker in msg:
            print(f"\nI think there is a {hacker['prob']*100}% chance that you're being attacked by CONTI from: {hacker['ip']} on your honeypot: {address[0]}\n")

thread1 = threading.Thread(target=noTouching)
thread1.start()
thread2 = threading.Thread(target=antiBrute)
thread2.start()
