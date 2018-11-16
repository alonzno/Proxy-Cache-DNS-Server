import os
import signal
import proxy

def start_proxy():
    proxy.start_proxy_server("127.0.0.1")

pids = []

if __name__ == "__main__":
    user_in = ""
    newpid = os.fork()
    if newpid == 0:
        start_proxy()
    else:
        pids.append(newpid)
        while user_in != "quit":
            user_in = input("Type quit to kill all processes")
        for pid in pids:
            os.kill(pid, signal.SIGTERM)

