import socket
import jieba
import Pack
import search
import MySQL
import crawler
import threading

def createSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 6667
    s.connect((host, port))
    return s

def readData(db1, db2, conn):
    packlen = conn.recv(10).decode("gb2312")
    if len(packlen) == 0:
        conn.close()
    packlen = int(packlen.split("#")[0])
    li = list()
    while packlen != 0:
        data = conn.recv(packlen)
        if len(data) != 0:
            li.append(data)
            packlen -= len(data)
        else:
            conn.close()
    sot = bytes()
    for l in li:
        sot += l
    sot = sot.decode("gb2312").split("#")
    if len(sot) == 2 and sot[1][:4] == "http":
        db = MySQL.connectDatabase()
        q = threading.Thread(target = SpiderRequest, args = (db, conn, sot))
        q.start()
    elif len(sot) == 2:
        q = threading.Thread(target = WebRequest, args = (db2, conn, sot))
        q.start()


def WebRequest(db, conn, sot):
    words = jieba.cut(sot[1])
    urlS = search.orderURL(db, words)
    pres,resp = Pack.enURLandWeight(urlS)
    sendw = resp + "#" + sot[0] + "#"
    lenw = str(len(sendw) + len(pres))
    while len(lenw) < 10:
        lenw += "#"
    sendw = lenw + sendw
    print("send"+sendw)
    conn.send(sendw.encode("gb2312"))
    if len(pres) != 0: 
        conn.send(pres)

def SpiderRequest(db, conn, sot):
    urls = Pack.deURL(sot[0], sot[1].encode("gb2312"))
    if urls is None:
        return None
    try:
        urls = list(crawler.iterSpider(db, urls, 1))
    except:
        return
    if len(urls) == 0:
        return None
    pres, resp = Pack.enURL(urls)
    sendw = resp + "#" + "s" + "#"
    lenw = str(len(sendw) + len(pres))
    while len(lenw) < 10:
        lenw += "#"
    
    sendw = lenw + sendw
    conn.send(sendw.encode("gb2312"))
    conn.send(pres)
    MySQL.disconnect(db)


def searchData(db, words):
    return search.orderURL(db, words)
     

def main():
    db1 = MySQL.connectDatabase()
    db2 = MySQL.connectDatabase()
    s = createSocket()
    urls = ["http://www.sohu.com/"]
    pres, resp = Pack.enURL(urls)
    sot = list()
    sot.append(resp)
    sot.append(pres.decode("gb2312"))
    SpiderRequest(db1, s, sot)
    while True:
        readData(db1, db2, s)


if __name__ == "__main__":
    main()
