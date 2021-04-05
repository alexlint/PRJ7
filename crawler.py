import urllib
from bs4 import BeautifulSoup
import sys
import re
import jieba
import jieba.analyse
import os
import MySQL
import requests
import configparser
import xml.etree.ElementTree as ET
from os import listdir
from gne import GeneralNewsExtractor

skip = ["知道","失去","咳","迅速","那儿","一次","不问","如同","共同","有力","重新","似乎",
"各级","抑或","起","不是","曾经","它们","不变","唯有","不仅","为止","类如","固然","了解",
"不至于","密切","这样","前者","虽然","除非","两者","怎么办","多数","就是","截至","尔尔",
"以后","可是","另外","一直","使用","眨眼","然后","遵循","只是","以外","例如","咚","特点",
"经过","因此","5","所以","只怕","而言","俺们","总而言之","比方","她的","一时","还是","加强",
"反之","换句话说","多次","哦","咱们","哎","论","哼唷","至若","才","使","今後","起来","有着",
"仍","孰知","此间","反应","一天","方便","其","这么点儿","做到","一旦","任凭","这里","逐步",
"最","还有","吓","反过来","不够","毫不","突然","他人","云云","处理","以故","借傥然","后面",
"去","具体地说","孰料","遇到","首先","越是","相对而言","要不然","而已","确定","开始","尚且",
"哪样","正值","到","出于","纵然","下列","哼","造成","就","坚持","不惟","再者说","之前","与此同时",
"犹且","为此","自打","乘","自后","普遍","全体","一","维持","这个","任何","尤其","况且","假如",
"代替","让","故","自己","哗","来着","哈","尽管","等","先不先","一些","突出","嘻","她","即若",
"2","转动","不断","得了","一起","扩大","经","那些","其中","中","取得","必要","运用","再","通常",
"兼之","比及","一边","7","冲","注意","立即","内","再者","随","限制","准备","叫做","彻底","便于",
"哩","乃至","喏","赶","不若","又及","替代","中小","先后","来自","其次","上下","遵照","而且","甚或",
"难道说","管","以致","自家","莫不然","趁","这般","有的","俺","允许","任","严重","归齐","成为","哪年",
"哈哈","却不","们","上来","何况","8","嗡嗡","乃","别的","比","可","啦","看来","照着","庶几","如","像",
"个别","只限","往往","伟大","既","人家","至今","适用","实现","于是","除此之外","者","这麽","简言之","A",
"惟其","除开","着","那边","一则","那般","余外","罢了","大大","能够","些","纵","按照","每年","这点","exp",
"矣哉","从此","譬如","啷当","上去","不外乎","Lex","要","说说","考虑","总是","并且","鉴于","构成","各","别管",
"而外","且说","凡","巴巴","呜呼","避免","吱","那么些","顺","或者","主要","怎样","各地","前后","不管","大多数",
"呗","各位","目前","倘然","达到","变成","嗳","设若","有时","不会","所在","昉","所谓","有些","本人","3","几乎",
"自身","最近","之类","逐渐","得","基本","认识","宣布","属于","那么","至于","始而","您","大家","怎奈","然而",
"前进","这么","他们们","谁人","矣乎","不同","总的来说","叮咚","此","兮","具体说来","形成","整个","不只","每个",
"当着","或","甚至于","这么样","与否","好","吧哒","需要","又","ub","觉得","有著","的","距","任务","尽管如此",
"使得","纵令","9","后者","真正","出来","无","换言之","什么样","于是乎","由","按","附近","不能","一片","同时",
"既然","之後","以免","意思","有所","上升","如何","根本","凡是","等到","哉","你的","正在","看出","依照","加之",
"此处","那样","上","啥","互相","正巧","上面","而后","毋宁","倘若","哎哟","何时","纵使","庶乎","望","一定","一方面",
"假使","得出","的话","的确","前此","由于","已","因为","哟","进行","是的","据","这时","乌乎","把","没有","若","拿",
"喽","打从","那么样","这边","由此可见","后来","果真","保持","她们","强烈","还要","但凡","特别是","嘎登","要么",
"并不是","了","已矣","不要","遭到","对待","下面","各人","倘使","复杂","当地","相应","再则","里面","有关","必须",
"不妨","为着","对应","处在","反而","规定","重大","乃至于","儿","即使","仍旧","显然","呼哧","或曰","除了","据此",
"及其","看看","各自","哪些","向着","为何","一下","咋","不一","绝对","同一","在下","高兴","最好","呕","关于具体地说",
"完成","第","嘘","都","就算","进而","时候","焉","跟","而","帮助","起见","给","或则","有效","莫若","不","别处","嘿",
"咦","大批","广大","如果","引起","不久","受到","不特","呜","此地","只当","万一","以","呢","即","上述","小","正常",
"即令","说来","我们","什么","up","欢迎","自","甚么","为什么","直接","显著","开外","积极","左右","左","右","依靠",
"尽","咧","无法","问题","曾","待","不然","继之","一致","然後","开展","甚至","但是","如上所述","被","诚然","呵呵",
"依","诸如","这些","哪","其实","来说","促进","进步","人们","比较","靠","不成","彼此","他的","作为","另一方面","倘或",
"相似","产生","哪个","极了","即或","大力","後面","何以","争取","合理","嘛","某些","和","则","一样","战斗","将","中间",
"彼","另","啪达","认为","诸位","非徒","继后","具有","那","行动","总结","可以","譬喻","贼死","之一","亦","它","不得","怎",
"怎么","周围","几","设或","也是","现代","之所以","认真","以至于","光是","不但","省得","已经","没奈何","是不是","你们","多少",
"何处","谁知","宁","不足","他","不尽","多么","哇","看见","巴","0","几时","看到","自从","非特","用","某某","不单","既往","临",
"及","然则","由此","转变","宁肯","决定","倘","随时","之","虽","下来","宁可","先生","向使","可能","一何","连","采取","呃","练习",
"如是","较","综上所述","那麽","喂","吧","出去","随著","特殊","不光","丰富","竟而","结合","部分","趁着","只","企图","相反","这种",
"着呢","大","咱","此次","当","适应","漫说","再其次","很","才能","你","当然","于","嗯","是以","再说","么","宁愿","致","顺着","何",
"吗","若非","且","旁人","每当","欤","冒","好的","这会儿","替","4","过去","今后","不如","本","非独","归","朝着","嗡","故而","甚而",
"其一","如若","今天","由是","也好","常常","掌握","普通","喔唷","总之","要求","及时","许多","就是说","对","今","与","全面","比如",
"召开","它的","好象","较之","也罢","沿","其二","组成","实际","应当","所","对方","某","因了","从而","莫如","即便","且不说","呸",
"而况","别说","所幸","能","明显","专门","真是","最大","方面","除","什麽","存在","一般","己","满足","等等","多","因","沿着","能否",
"只有","凭借","若夫","移动","接着","并非","假若","阿","反映","原来","来","是","介于","不怕","犹自","呵","向","地","其他","根据",
"正如","直到","设使","从","嘎","举行","相信","并不","谁","哎呀","别","以便","依据","这儿","不尽然","此外","啐","不敢","该","哪儿",
"紧接着","叫","岂但","也","通过","嘿嘿","加以","对于","也","同","这","乎","前面","非常","般的","却","具体","适当","随后","呀",
"容易","啊","完全","本身","一面","全部","一切","1","尔","诚如","6","有及","行为","继而","说明","结果","防止","其余","要不是",
"这就是说","无宁","正是","总的来看","再有","看","并没有","用来","后","基于","怎么样","与其","别人","尔后","虽说","如其","大约",
"从事","并","至","本着","有","双方","得到","以前","另悉","以至","广泛","唉","那会儿","当时","进入","重要","哪边","云尔","在",
"获得","先後","可见","朝","无论","以为","最後","非但","各种","那里","因而","分别","其它","加入","为主","同样","以及","最高",
"就是了","除外","现在","不料","如下","总的说来","严格","出现","则甚","少数","以下","别是","如此","所有","安全","范围","後来",
"我","甚且","谁料","为","在于","自各儿","为了","自个儿","过","愿意","若果","为什麽","每天","哪天","充分","离","个人","反过来说",
"恰恰相反","以後","边","照","明确","只要","似的","不比","而是","下去","彼时","他们","这么些","有利","主张","怎麽","人","与其说",
"巨大","深入","嗬","这次","不拘","就要","二来","或是","慢说","那时","仍然","腾","还","以来","一转眼","不过","清楚","要是","巩固",
"对比","矣","应用","它们的","随着","年","月","日","今年","诸","针对","这一来","此时","是否","只消","不可","转贴","表示","十分",
"否则","但","大量","及至","某个","接著","更加","打","联系","故此","果然","连同","以上","坚决","心里","鄙人","下","强调","继续",
"个","因着","我的","关于","以期","过来","赖以","相同","要不","之后","必然","那个","哪怕","哪里","最后","有点","各个","经常","即如",
"不独","集中","当前","相等","应该","相对","既是","表明","良好","若是","本地","一来","凭","不论","如上","往","相当","每","虽则"]
   
# 爬取网页
def getSoup(url):
    try:
        c = urllib.request.urlopen(url)
    except:
        return None
    html = c.read()
    bs = BeautifulSoup(html, "lxml")
    return bs

def getURL(db, bs, page):
    links = bs('a')
    urls = set()
    for link in links:
        if 'href' in dict(link.attrs):
            url = urllib.parse.urljoin(page, link['href'])
            url = url.split('<')[0]
            url = url.split('#')[0]
            if url[:4] != 'http':
                continue
            urls.add(url)
            link = str(link)
            index1 = 0
            index2 = 0
            for i in range(len(link)):
                if link[i] == '>':
                    index1 = i+1
                if index1 != 0 and link[i] == '<':
                    index2 = i
                    break
            finalRt = splitWord(link[index1:index2])
            createLinkwordix(db, finalRt, url)
    return urls

def getTitle(url):
    bs = getSoup(url)
    if bs is None:
        return "no article"
    if bs.title is None:
        return "no title"
    title=bs.title.string
    return title

def splitWord(content):
    ls = jieba.analyse.textrank(content, topK = 20, withWeight = True, allowPOS = ("ns", "n", "vn", "v"))
    finalRt = []
    for l in ls:
        if l[0] in skip:
            continue
        else:
            finalRt.append(l)
    return finalRt

def fetch(url):
    headers = {
        "User-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }       
    try:
        response = requests.get(url=url, headers=headers).content.decode('utf-8',"ignore")
        extractor = GeneralNewsExtractor()
        article_content = extractor.extract(response)
        article_content["url"] = url
    except:
        return None
    return article_content

def iterSpider(db, url_list, n):
    a = set()
    for url in url_list:
        a.add(url)
    for i in range(n):
        urls = a.copy()
        a.clear()
        for url in urls:
            bs = getSoup(url)
            if bs is None:
                continue
            article_content = fetch(url)
            if article_content == None:
                return None
            if len(article_content["content"]) < 20 :
                continue 
            text = article_content["content"]
            finalRt = splitWord(text)
            createIndex(db, finalRt, url,article_content)
            urlset = getURL(db, bs, url)
            a = a.union(urlset)
            createLinkix(db, url, a)
            urlset.clear()
    return a


def createIndex(db, words, url,article_content):
    if "tv." in str(url):
        return None
    symbols = "~!@#$%^&*()_+-*/<>,.[]\/"
    for symbol in symbols:
        if symbol in article_content["content"]:
            return None
    urlid = getUID(db, url,article_content)
    if urlid is None:
        return None
    for word in words:
        wid = getWid(db, word)
        if wid is None:
            continue
        sql = "select urlid from wordlocation where wordid = " + str(wid) + " and urlid = " + str(urlid) + ";"
        finalRt = MySQL.query(db, sql)
        if finalRt is None:
            return None
        if len(finalRt) == 0:
            MySQL.insertValues(db, "wordlocation",["wordid", "urlid", "weight"],[[str(wid), str(urlid), str(word[1])]])

def getUID(db, url,article_content):
    if "tv." in str(url):
        return None
    sql = "select id from urllist where url = " + "'" + url + "';"
    finalRt = MySQL.query(db, sql)
    if finalRt is None:
        return None
    if len(finalRt) == 0:
        url = "'" + url + "'"
        files = listdir("news/")
        n = float(len(files))
        if n!=0:
            for i in files:
                root = ET.parse("news/" + i).getroot()
                title = root.find('title').text
                if article_content["title"] == title:
                    return None
        MySQL.insertValues(db, "urllist", ["url"], [[url]])
        finalRt = MySQL.query(db, sql)
        if finalRt is None:
            return None
        doc = ET.Element("doc")
        ET.SubElement(doc, "id").text = "%d"%(finalRt[0][0])
        ET.SubElement(doc, "url").text = url
        ET.SubElement(doc, "title").text = article_content["title"]
        ET.SubElement(doc, "datetime").text = article_content["publish_time"]
        ET.SubElement(doc, "body").text = article_content["content"]
        tree = ET.ElementTree(doc)
        tree.write("news/" + "%d.xml"%(finalRt[0][0]), encoding = "utf-8", xml_declaration = True)
    return finalRt[0][0]
    
def getUrlIdForLink(db, url):
    if "tv." in str(url):
        return None
    sql = "select id from urllist where url = " + "'" + url + "';"
    finalRt = MySQL.query(db, sql)
    if finalRt is None:
        return None
    if len(finalRt) == 0:
        url = "'" + url + "'"
        article_content = fetch(url.replace("'",""))   
        if article_content == None:
            return None
        files = listdir("news/")
        n = float(len(files))
        if n!=0:
            for i in files:
                root = ET.parse("news/" + i).getroot()
                title = root.find('title').text
                if article_content["title"] == title:
                    return None
        MySQL.insertValues(db, "urllist", ["url"], [[url]])
        finalRt = MySQL.query(db, sql)
        if finalRt is None:
            return None
        doc = ET.Element("doc")
        ET.SubElement(doc, "id").text = "%d"%(finalRt[0][0])
        ET.SubElement(doc, "url").text = url
        ET.SubElement(doc, "title").text = article_content["title"]
        ET.SubElement(doc, "datetime").text = article_content["publish_time"]
        ET.SubElement(doc, "body").text = article_content["content"]
        tree = ET.ElementTree(doc)
        tree.write("news/" + "%d.xml"%(finalRt[0][0]), encoding = "utf-8", xml_declaration = True)
    return finalRt[0][0]

def getWid(db, word):
    sql = "select id from wordlist where word = " + "'" + word[0] + "';"
    finalRt = MySQL.query(db, sql)
    if finalRt is None:
        return None
    if len(finalRt) == 0:
        wordStr = "'" + word[0] + "'"
        MySQL.insertValues(db, "wordlist", ["word"],[[wordStr]])
        finalRt = MySQL.query(db,sql)
        if finalRt is None:
            return None
    return finalRt[0][0]


def createLinkwordix(db, words, url):
    if "tv." in str(url):
        return None
    if len(words) == 0:
        return 
    urlid = getUrlIdForLink(db, url)
    if urlid is None:
        return None
    for word in words:
        wordStr = "'" + word[0] + "'"
        sql = "select linkid from linkword where word = " + wordStr + ";"
        urlRes = MySQL.query(db, sql)
        if urlRes is None:
            continue
        if len(urlRes) == 0:
            MySQL.insertValues(db, "linkword", ["word", "linkid"], [[wordStr, str(urlid)]])
        else:
            for urlid_query in urlRes:
                if urlid_query[0] ==  urlid:
                    break
            else:
                MySQL.insertValues(db, "linkword", ["word", "linkid"], [[wordStr, str(urlid)]])
                

def createLinkix(db, url, urls):
    if "tv." in str(url):
        return None
    fromid = getUrlIdForLink(db, url)
    if fromid is None:
        return None
    for link in urls:
        toid = getUrlIdForLink(db, link)
        if toid is None:
            return None
        MySQL.insertValues(db, "link", ["fromid", "toid"], [[str(fromid), str(toid)]])

def main():
    db = MySQL.connectDatabase()
    MySQL.createTable(db)

if __name__ == "__main__":
    main()
