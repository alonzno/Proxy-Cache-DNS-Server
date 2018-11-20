from socket import *
import json

def read_zone():
    f = open("zones/www.altamirano.432.zone")
    data = json.load(f)
    return data

zone = read_zone()

def maskToString(b1, b2):
    return str(bin(ord(b1)&ord(b2)))[2:]

def getRR(data):
    host_name, q_type = getRRDomain(data)
    t = ''
    if (q_type == b'\x00\x01'):
        t = 'a'
    try:
        rr = zone['Records']['.'.join(host_name)]
        return (rr, host_name);
    except:
        return (None, host_name)
    pass

def getRRDomain(data):
    scanning = False
    counter = 0
    q_len = 0
    host_name = []
    domain = ''
    byte_counter = 0
    for b in data:
        if scanning:
            domain += chr(b)
            counter += 1;
            if counter == q_len:
                host_name.append(domain)
                domain = ''
                scanning = False
                counter = 0
            if b == 0:
                break;
        else:
            q_len = b
            scanning = True
        byte_counter += 1

    q_type = data[byte_counter:byte_counter+2]
    return (host_name, q_type)
def questionToBytes(name):
    retB = b''
    for p in name:
        retB += bytes([len(p)])
        for c in p:
            retB += ord(c).to_bytes(1, byteorder='big')
    retB += int(0).to_bytes(1, byteorder='big')
    retB += int(1).to_bytes(2, byteorder='big')
    retB += int(1).to_bytes(2, byteorder='big')

    return retB

    #retB += bytes([0])

def recordToBytes(name, type_, value, ttl):
    retB = b'\xc0\x0c'
    
    if type_ == "A":
        retB += bytes([0]) + bytes([1])
    retB += bytes([0]) + bytes([1])
    retB += int(ttl).to_bytes(4, byteorder='big')
    if type_ == "A":
        retB += bytes([0]) + bytes([4])
    for p in value.split('.'):
        retB += int(p).to_bytes(1, byteorder='big')
    return retB

    

def extractFlags(data, error = False):
    byteA = bytes(data[0])
    byteB = bytes(data[1])
    
    qr = '1'
    opcode = ''
    for b in range(1,5):
        opcode += str(ord(byteA) & (1<<b))
    aa = '1'
    tc = '0'
    ra = '0'
    rd = '0'
    z = '000'
    if error:
        rcode = '0010'
    else:
        rcode = '0000'


    flags = [qr, opcode, aa, tc, rd, ra, z, rcode]
    return int("".join(list(flags[0:5])), 2).to_bytes(1, byteorder = 'big') + int("".join(list(flags[5:])), 2).to_bytes(1, byteorder = 'big')

def makeResponse(data):
    transId = data[0:2]
    
    
    flagBytes = data[2:4]
    flags = extractFlags(flagBytes)
    
    qcount = b'\x00\x01'
    nscount = b'\x00\x00'
    arcount = b'\x00\x00'

    rr, host_name = getRR(data[12:])
    if rr == None:
        acount = b'\x00\x00'
        flags = extractFlags(flagBytes, True)
        dnsheader = transId + flags + qcount + acount + nscount + arcount
        dnsbody = questionToBytes(host_name)
        return dnsheader + dnsbody
        #More response forming here
    else:
        acount = b'\x00\x01'
        dnsheader = transId + flags + qcount + acount + nscount + arcount
        dnsbody = questionToBytes(host_name) + recordToBytes(host_name, rr['Type'], rr['Value'], rr['TTL'])
        return dnsheader + dnsbody

    

def start_dns(ip_to_use):
    port = 53
    ip = ip_to_use

    serSock = socket(AF_INET, SOCK_DGRAM)
    serSock.bind((ip, port))
    

    while True:
        data, addr = serSock.recvfrom(512)
        response = makeResponse(data)
        serSock.sendto(response, addr)
        #serSock.sendto(response, addr)

if __name__ == "__main__":
    start_dns("127.0.0.1")
