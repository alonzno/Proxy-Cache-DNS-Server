from re import match

from socket import *
import os
import _thread
import datetime

def start_proxy_server(ip_to_bind):
    tcpSerSock = socket(AF_INET, SOCK_STREAM)

    tcpSerSock.bind((ip_to_bind, 8888))
    tcpSerSock.listen(10)
    path = os.getcwd()
    os.chdir(path + "/cache/")



    def handle_client(tcpCliSock):
        message = str(tcpCliSock.recv(4096))

        filename = message.split()[1]
        if '/' in filename:
            filename = message.split()[1].partition("/")[2]


        fullname = message.split()[1]
        fullname = fullname.replace("http://","")

        fileExist = False
        fileToUse = "./cache/" + fullname + "_FILE"
        try:
            f = open("./" + fullname + "_FILE", "rb")

            if filename[0] == '/':
                hostn = str(filename[1:]).replace("/www.", "", 1).partition("/")[0]
            else:
                hostn = filename.replace("/www.", "", 1).partition("/")[0]

            #Handle the case of non port ip:port pattern
            if match("([0-9]+\.){3}[0-9]+:[0-9]+", hostn):
                items = hostn.partition(":")
                ip = items[0]
                port = int(items[2])
                addr = (ip, port)
            else:
                ip = gethostbyname(hostn)
                if ip == "0.0.0.0":
                    #DNS did not resolve the IP of hostname
                    return
                #Connect to website
                addr = (ip, 80)


            c = socket(AF_INET, SOCK_STREAM)
            c.connect(addr)
            s = "HEAD "+ "http://" + fullname + " HTTP/1.0\n"
            s += "Host: " + hostn + "\n\n"

            fileobj = c.makefile("rwb", 256)
            fileobj.write(s.encode())
            fileobj.flush()
            buf = fileobj.read()

            statbuf = os.stat("./" + fullname + "_FILE")

            outputData = f.read()
            fileExist = True

            tcpCliSock.send(outputData)

        except IOError:
            if not fileExist:
                try:
                    #GetIP
                    if filename[0] == '/':
                        hostn = str(filename[1:]).replace("/www.", "", 1).partition("/")[0]
                    else:
                        hostn = filename.replace("/www.", "", 1).partition("/")[0]

                    def sendGet(addr):
                        c = socket(AF_INET, SOCK_STREAM)
                        c.connect(addr)
                        s = "GET "+ "http://" + fullname + " HTTP/1.0\n"
                        s += "Host: " + hostn + "\n\n"

                        fileobj = c.makefile("rwb", 256)
                        fileobj.write(s.encode())
                        fileobj.flush()
                        buf = fileobj.read()

                        if not os.path.exists(os.path.dirname(fullname)):
                            try:
                                os.makedirs(os.path.dirname(fullname))
                            except OSError as err:
                                if err.errno != errno.EEXIST:
                                    raise
                        return buf

                    #Handle the case of non port ip:port pattern
                    if match("([0-9]+\.){3}[0-9]+:[0-9]+", hostn):
                        items = hostn.partition(":")
                        ip = items[0]
                        port = int(items[2])
                        buf = sendGet((ip, port))
                    else:
                        ip = gethostbyname(hostn)
                        if ip == "0.0.0.0":
                            #DNS did not resolve the IP of hostname
                            return
                        #Connect to website
                        buf = sendGet((ip, 80))

                    #Only Cache objects less that 10MB
                    if len(buf) < 10000000:
                        tmpFile = open("./" + fullname + "_FILE", "wb")
                        tmpFile.write(buf)

                    tcpCliSock.send(buf)
                except Exception as e:
                    pass
            else:
                pass
        tcpCliSock.close()

    while True:
        tcpCliSock, addr = tcpSerSock.accept()
        _thread.start_new_thread( handle_client, (tcpCliSock, ) )

if __name__ == "__main__":
    start_proxy_server("127.0.0.1")
