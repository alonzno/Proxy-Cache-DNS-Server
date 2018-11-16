from socket import *
import os
import _thread

def start_proxy_server(ip_to_bind):
    '''
    if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP  Address Of Proxy Server')
        sys.exit(2)
    '''

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
        #fullname = str(fullname[:-1])

        #print(filename)
        print("fullname", fullname)
        print("filename", filename)
        fileExist = False
        fileToUse = "./cache/" + fullname + "_FILE"
        #print(fileToUse)
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
                    #print("hostname", hostn)
                    #print(filename)
                    ip = gethostbyname(hostn)
                    print("IP Address", ip)
                    if ip == "0.0.0.0":
                        #Yo fix this, bad move
                        return

                    #Connect to website
                    c = socket(AF_INET, SOCK_STREAM)
                    c.connect((ip, 80))
                    s = "GET "+ "http://" + fullname + " HTTP/1.0\n"
                    s += "Host: " + hostn + "\n\n"

                    #print("--------------------")
                    #print(s)
                    #print("--------------------")
                    fileobj = c.makefile("rwb", 256)
                    fileobj.write(s.encode())
                    fileobj.flush()
                    buf = fileobj.read()

                    #REVISE BELOW THIS
                    if not os.path.exists(os.path.dirname(fullname)):
                        try:
                            os.makedirs(os.path.dirname(fullname))
                        except OSError as err:
                            if err.errno != errno.EEXIST:
                                raise
                    #REVISE ABOVE THIS
                    #os.chdir(path)

                    #Only Cache objects less that 10MB
                    if len(buf) < 10000000:
                        tmpFile = open("./" + fullname + "_FILE", "wb")
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

    while True:
        print("Ready to serve..")
        tcpCliSock, addr = tcpSerSock.accept()
        print("Received a connection from:", addr)
        _thread.start_new_thread( handle_client, (tcpCliSock, ) )
