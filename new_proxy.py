from socket import *
import urllib.request
import sys
import os
import _thread

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP  Address Of Proxy Server')
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)

tcpSerSock.bind((sys.argv[1], 8887))
tcpSerSock.listen(10)
path = os.getcwd()
os.chdir(path + "/cache/")

def handle_client(tcpCliSock):
    message = str(tcpCliSock.recv(4096))
    print(message)

    filename = message.split()[1].partition("/")[2]

    fullname = message.split()[1]
    fullname = fullname.replace("http://","")
    #fullname = str(fullname[:-1])

    print(filename)
    print("fullname", fullname)
    fileExist = False
    fileToUse = "./cache/" + fullname + "_FILE"
    print(fileToUse)
    try:
        f = open("./" + fullname + "_FILE", "rb")
        outputData = f.read()
        fileExist = True

        tcpCliSock.send(outputData)
        print("Read from cache")

    except IOError:
        if not fileExist:
            try:
                #GetIP
                if filename[0] == '/':
                    hostn = str(filename[1:]).replace("/www.", "", 1).partition("/")[0]
                else:
                    hostn = filename.replace("/www.", "", 1).partition("/")[0]
                print("hostname", hostn)
                print(filename)
                ip = gethostbyname(hostn)
                print(ip)
                if ip == "0.0.0.0":
                    #Yo fix this, bad move
                    return

                #Connect to website
                c = socket(AF_INET, SOCK_STREAM)
                c.connect((ip, 80))
                s = "GET "+ "http://" + fullname + " HTTP/1.0\n"
                s += "Host: " + hostn + "\n\n"
                #Add the parts of the message for sending
                #Host: header.  for cloudflare
                print("--------------------")
                print(s)
                print("--------------------")
                fileobj = c.makefile("rwb", 256)
                fileobj.write(s.encode())
                fileobj.flush()
                buf = fileobj.read()
                #print(str(buf.decode()))

                #os.chdir(path + "/cache/")
                #REVISE BELOW THIS
                if not os.path.exists(os.path.dirname(fullname)):
                    try:
                        os.makedirs(os.path.dirname(fullname))
                    except OSError as exc: # Guard against race condition
                        os.chdir(path)
                        if exc.errno != errno.EEXIST:
                            raise
                #REVISE ABOVE THIS
                #os.chdir(path)

                #tmpFile = open("./cache/" + fullname + "_FILE", "wb")
                tmpFile = open("./" + fullname + "_FILE", "wb")

                tmpFile.write(buf)
                tcpCliSock.send(buf)
            except Exception as e:
                os.chdir(path)
                print(e)
                print(type(e))
                print(e.args)
                print("Illegal request")
        else:
            pass
    tcpCliSock.close()

while True:
    print("Ready to serve..")
    tcpCliSock, addr = tcpSerSock.accept()
    print("Received a connection from:", addr)
    _thread.start_new_thread( handle_client, (tcpCliSock, ) )
