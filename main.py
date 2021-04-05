import socket
import sys
import Pack
import gevent
import time
import Redis
from gevent import monkey
monkey.patch_all()


r = Redis.Connect()
linkWeb = set()
linkSv = set()
flagR = dict()

def createSocket():
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port1 = 6666
    server1.bind((host,port1))
    server1.listen(5)
    port2 = 6667
    server2.bind((host,port2))
    server2.listen(5)
    return server1, server2

class combine:
    def __init__(self, link):
        self.link = link
        self.URList = dict()
        self.ser_links = list()

    def com(self, ser_link, sites, weight):
        for i in range(len(sites)):
            if sites[i] in self.URList:
                self.URList[sites[i]] += weight[i]
            else:
                self.URList[sites[i]] = weight[i]
        self.ser_links.append(ser_link)
        for link in linkSv:
            if link not in self.ser_links:
                return False
        return True
    
    def sortUrl(self):
        tmp = sorted(self.URList.items(), key = lambda item:item[1], reverse = True)
        tmp = dict(tmp)
        return list(tmp.keys())

    def getConn(self):
        return self.link


def acceptConn(con):
    while True:
        link, addr = con.accept()
        print("new connect %s" %(link))
        if con == server1:
            linkWeb.add(link)
            gevent.spawn(WebRequest, link)
        else:
            linkSv.add(link)
            gevent.spawn(SubRequest, link)

def readData(link):
    packL = link.recv(10).decode("gb2312")
    if len(packL) == 0:
        return None
    packL = int(packL.split("#")[0])
    li = list()
    while packL != 0:
        data = link.recv(packL)
        if len(data) != 0:
            li.append(data)
            packL -= len(data)
        else:
            return None
    slt = bytes()
    for l in li:
        slt += l
    return slt.decode("gb2312")

def WebRequest(link):
    while True:
        slt = readData(link)
        if slt is None:
            linkWeb.remove(link)
            link.close()
            return None
        slt = str(hash(link)) + "#" + slt
        print(slt)
        strL = str(len(slt.encode("gb2312")))
        while len(strL) < 10:
            strL += "#"
        senS = strL + slt
        print(senS)
        for c in linkSv:
            c.send(senS.encode("gb2312"))    
        linkInf = combine(link)
        flagR[hash(link)] = linkInf
    

def SubRequest(link):
    while True:
        slt = readData(link)
        if slt is None:
            linkSv.remove(link)
            link.close()
            return None
        slt = slt.split("#")
        print(slt)
        if slt[1] == 's':
            sites = Pack.deURL(slt[0], slt[2].encode("gb2312"))
            checkURLrepeat(sites)
        else:
            if(slt[1] == ''):
                continue
            sites, weight = Pack.deURLandWeight(slt[0], slt[2].encode("gb2312"))
            print(sites)
            print(weight)
            linkInf = flagR[int(slt[1])]
            if linkInf.com(link, sites, weight):
                writeWeb(linkInf)

def checkURLrepeat(sites):
    noUrl = []
    for url in sites:
        if not Redis.Sismember(r, url, 1):
            noUrl.append(url)
            Redis.Add(r, url, 1)

    times = len(linkSv)
    vacant = (len(noUrl) // times) + 1
    i = 0
    for link in linkSv:
        repack, reP = Pack.enURL(noUrl[i:i+vacant])
        i += vacant
        senS = reP + "#"
        lenS = str(len(senS) + len(repack))
        while len(lenS) < 10:
            lenS += "#"
        senS = lenS + senS
        link.send(senS.encode("gb2312"))
        link.send(repack)
    

def writeWeb(linkInf):    
    link = linkInf.getConn()
    sites = linkInf.sortUrl()
    repack,reP = Pack.enURL(sites)
    senS = reP + "#"
    lenS = str(len(senS) + len(repack))
    while len(lenS) < 10:
        lenS += "#"
    senS = lenS + senS
    link.send(senS.encode("gb2312"))
    link.send(repack)
server1, server2 = createSocket()

def main():
    while True:
        g1 = gevent.spawn(acceptConn, server1)
        g2 = gevent.spawn(acceptConn, server2)
        g1.join()
        g2.join()

if __name__ == "__main__":
    main()
