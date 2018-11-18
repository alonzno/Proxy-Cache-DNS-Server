import os
import signal

import proxy
import server

def start_proxy():
    proxy.start_proxy_server("127.0.0.1")

def start_server():
    server.start_server("127.0.0.1")

pids = []

if __name__ == "__main__":
    '''
    if len(sys.argv) <= 1:
        print("Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP  Address Of Proxy Server")
        sys.exit(2)
    '''

    user_in = ""
    newpid = os.fork()
    if newpid == 0:
        start_server()
    else:
        pids.append(newpid)
        newpid = os.fork()
        if newpid == 0:
            start_proxy()
        else:
            pids.append(newpid)
            while user_in != "quit":
                user_in = input("Type quit to kill all processes")
            for pid in pids:
                os.kill(pid, signal.SIGTERM)

