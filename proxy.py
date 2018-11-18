from re import match

from socket import *
import os
import _thread
#import sys         #DEBUG
#import linecache   #DEBUG

def start_proxy_server(ip_to_bind):
    tcpSerSock = socket(AF_INET, SOCK_STREAM)

    tcpSerSock.bind((ip_to_bind, 8888))
    tcpSerSock.listen(10)
    path = os.getcwd()
    os.chdir(path + "/cache/")

    def handle_client(tcpCliSock):
        message = str(tcpCliSock.recv(4096))
        print(message)

        filename = message.split()[1]
        if '/' in filename:
            filename = message.split()[1].partition("/")[2]


        fullname = message.split()[1]
        fullname = fullname.replace("http://","")

        print("fullname", fullname)
        print("filename", filename)
        fileExist = False
        fileToUse = "./cache/" + fullname + "_FILE"
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
                    #Handle the case of non port ip:port pattern
                    if match("([0-9]+\.){3}[0-9]+:[0-9]+", hostn):
                        items = hostn.partition(":")
                        ip = items[0]
                        port = int(items[2])
                        c = socket(AF_INET, SOCK_STREAM)
                        c.connect((ip, port))
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
                        return
                    else:
                        ip = gethostbyname(hostn)
                    print("IP Address", ip)
                    if ip == "0.0.0.0":
                        #DNS did not resolve the IP of hostname
                        return

                    #Connect to website
                    c = socket(AF_INET, SOCK_STREAM)
                    c.connect((ip, 80))
                    s = "GET "+ "http://" + fullname + " HTTP/1.0\n"
                    s += "Host: " + hostn + "\n\n"

                    fileobj = c.makefile("rwb", 256)
                    fileobj.write(s.encode())
                    fileobj.flush()
                    buf = fileobj.read()

                    if not os.path.exists(os.path.dirname(fullname)):
                        try:
                            os.makedirs(os.path.dirname(fullname))
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise

                    #Only Cache objects less that 10MB
                    if len(buf) < 10000000:
                        tmpFile = open("./" + fullname + "_FILE", "wb")
                        tmpFile.write(buf)
                    tcpCliSock.send(buf)
                except Exception as e:
                    #Begin DEBUG
                    '''
                    exc_type, exc_obj, tb = sys.exc_info()
                    f = tb.tb_frame
                    lineno = tb.tb_lineno
                    filename = f.f_code.co_filename
                    linecache.checkcache(filename)
                    line = linecache.getline(filename, lineno, f.f_globals)
                    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
                    print("============================")
                    '''
                    #End DEBUG
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
