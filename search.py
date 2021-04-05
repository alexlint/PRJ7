import MySQL
import socket
import jieba.analyse
import crawler

def orderURL(db, words):
    urlmark = dict()
    linkids = set()
    for word in words:
        wid = getWid(db, word)
        if wid is None:
            continue
        urlw = getUID(db, wid)
        if urlw is None:
            continue
        for urlin in urlw:
            url =  getURL(db, urlin[0])
            if url is None:
                continue
            linkids.add((urlin[0],url))
            calURLscore(urlmark, url, urlin[1])
        rlinkid = getLid(db, word)
        if rlinkid is None:
            continue
        else:
            for linkid in rlinkid:
                url = getURL(db, linkid[0])
                if url is None:
                    continue
                else:
                    linkids.add((linkid[0],url))
                    calURLscore(urlmark, url, 0.5)
    urlmark = LinkScore(db, urlmark, linkids)
    urlmark = sorted(urlmark.items(), key = lambda item:item[1],reverse = True)
    return urlmark



def LinkScore(db, urlmark, linkids):
    pageR = dict()
    urlTF = dict()
    for linkid in linkids:
        pageR[linkid[0]] = 1.0
        urlTF[linkid[0]] = list()
        
    for linkid in linkids:
        linkfid = getFromid(db, linkid[0])
        if linkfid is None:
            continue
        else:
            for tmpid in linkfid:
                urlTF[linkid[0]].append(tmpid[0])
    loop = 20
    for i in range(loop):
        for linkid in linkids:
            linkidss = urlTF[linkid[0]]
            pageR[linkid[0]] = len(linkidss) * 0.80
    
    for linkid in linkids:
        calURLscore(urlmark, linkid[1], pageR[linkid[0]])

    return urlmark

def getFromid(db, tid):
    sql = "select fromid from link where toid = " + str(tid) + ";"
    finalRt = MySQL.query(db, sql)
    if len(finalRt) == 0:
        return None
    else:
        return finalRt

def getLid(db, linkkey):
    sql = "select linkid from linkword where word = " + "'" + linkkey + "';"
    finalRt = MySQL.query(db, sql)
    if len(finalRt) == 0:
        return  None
    else:
        return finalRt

def getWid(db, keyword):
    sql = "select id from wordlist where word = " + "'" + keyword + "';"
    finalRt = MySQL.query(db, sql)
    if len(finalRt) == 0:
        return None
    return finalRt[0][0]

def getURL(db,idu):
    sql = "select url from urllist where id = " + str(idu) + ";"
    finalRt = MySQL.query(db, sql)
    if len(finalRt) == 0:
        return None;
    return finalRt[0][0]

def getUID(db, wid):
    sql2 = "select urlid, weight from wordlocation where wordid = " + str(wid) + ";"
    finalRt = MySQL.query(db, sql2)
    if len(finalRt) == 0:
        return None
    return finalRt

def calURLscore(urlmark, url, score):
    if url in urlmark:
        urlmark[url] += score
    else:
        urlmark[url] = score

def main():
    inputSt = input("Searching:")
    db = MySQL.connectDatabase()
    print("Keywords:%s" %(inputSt))
    words = jieba.cut(inputSt)
    orderURL(db, words)

if __name__ == "__main__":
    main()

