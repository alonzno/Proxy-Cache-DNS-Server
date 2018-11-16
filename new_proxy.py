from socket import *
import urllib.request
import sys

if len(sys.argv) <= 1: 
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP  Address Of Proxy Server')
    sys.exit(2) 

tcpSerSock = socket(AF_INET, SOCK_STREAM)

tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(10)

while True:
    print("Ready to serve..")
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from:", addr)
    message = str(tcpCliSock.recv(4096))
    print(message)

    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = False
    fileToUse = "/" + filename
    print(fileToUse)
    try:
        f = open(fileToUse[1:], "r")
        outputData = f.read()
        fileExist = True

        tcpCliSock.send(outputData.encode())
        print("Read from cache")

    except IOError:
        if not fileExist:
            try:
                #GetIP
                hostn = filename.replace("/www.", "", 1).partition("/")[0]
                print("hostname", hostn)
                ip = gethostbyname(hostn)
                print(ip)
    
                #Connect to website
                c = socket(AF_INET, SOCK_STREAM)
                c.connect((ip, 80))
                s = "GET "+ "http://" + hostn + " HTTP/1.0\n\n"
                print("--------------------")
                print(s)
                print("--------------------")
                fileobj = c.makefile("rwb", 256)
                fileobj.write(s.encode())
                fileobj.flush()
                buf = fileobj.read()
                print(str(buf.decode('utf8')))
                tmpFile = open("./" + filename, "wb")
                tmpFile.write(buf)
                tcpCliSock.send(buf)
            except Exception as e:
                print(e)
                print(type(e))
                print(e.args)
                print("Illegal request")
        else:
            pass
    tcpCliSock.close()

