import socket

s = socket.socket()
s.bind(("0.0.0.0", 40008))
s.listen(10)

i = 1
while True:
    print(f"Printer ready for receiving on port {40008}")
    sc, address = s.accept()
    print(f"Connection from: {address}")
    filename = 'file_'+str(i)
    f = open(filename, "wb")
    i += 1
    try:
        l = sc.recv(1024)
        while l:
            f.write(l)
            l = sc.recv(1024)
        f.close()
        sc.close()
    except:
        pass

s.close()