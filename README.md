# Proxy-Cache-DNS-Server
I wrote this program for CIS 432 Introduction to Computer Networking

This program functions as a four in one web proxy, web cache, web server,
and DNS Server.  I know, quite the hutspot.

The program has three main programs.

### proxy.py
This is the proxy server / web cache.
By default it will operate on localhost port 8888.  This can easily be 
modified at the head of the program.  This web proxy only operates HTTP 1.0.
It will cache objects smaller than 10Mb.
Records are written to the `./cache/` directory.
On a Mac you should configure your network settings to use localhost:8888 as
the HTTP proxy at: 
System Preferences > Network > Advanced > Proxies
This program is multithreaded.


### server.py
This is the web server.
By default it will operate on localhost port 80.  Web objects can be found
in the `./www/` directory.  On Mac's you might need to
run this program as a super user process as regular users are denied 
permission to bind port 80 by default.  This server is tested to handle 
`GET http://127.0.0.1/ HTTP/1.0`

### dns.py
This is the DNS server.
By default it will operate on localhost port 53.  This DNS is authoratize for
the domain
`altamirano.432`
It will respond with an error if queried for a record it doesn't have.
A good future modification would be to add records to other DNS servers.
This DNS server has been tested to handle.
`curl www.altamirano.432`
Records can be added at `./zones/www.altamirano.432.zone`

### driver.py
This is the driver program.
This script will spawn three processes, one for each server listed above.
Type `quit` to kill all processes.

Usage:
  * `sudo python3 driver.py`

Dependencies:
  * python3

### Note
Since we are running the proxy/cache as a SU process, regular users might not have
permission to erase the contents of the cache.  Use `sudo rm -rf cache/*` to clear
cache as non-SU
