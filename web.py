from flask import Flask,render_template, request, redirect, url_for
from werkzeug.routing import BaseConverter
from flask_script import Manager
import pymysql
import webServer
import requests
import urllib
import sqlite3
import MySQL
import xml.etree.ElementTree as ET
import os 

from gne import GeneralNewsExtractor
connecter = webServer.connect( )

class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]
        self.db = MySQL.connectDatabase()
        self.idf_path = 'data/idf.txt'
        self.path = 'news/'
        self.config_encoding = 'utf-8'
app = Flask(__name__)
app.secret_key = 'itheima'
pymysql.install_as_MySQLdb( )
search = ""


app.url_map.converters['regex']=RegexConverter
manager = Manager(app)

@app.route('/',methods=['POST','GET'])
def judge():
    from forms import Search
    sform = Search( )
    if request.method == 'POST':
        if sform.validate_on_submit( ):
            search = sform.search.data
            print(search)
            return redirect(url_for('.go', search=search))
    return render_template('search.html', title='Search', form=sform)

@app.route('/find/<id>', methods=['GET','POST'])
def find(id,extra=True):
    docs = []
    idf_path = 'data/idf.txt'
    db_path = 'data/ir.db'
    root = ET.parse('news/' + '%s.xml' % id).getroot()
    url = root.find('url').text.replace("'","")
    title = root.find('title').text
    body = root.find('body').text
    time = root.find('datetime').text.split(' ')[0]
    datetime = root.find('datetime').text
    doc = {'url': url, 'title': title, 'datetime': datetime, 'time': time, 'body': body,
           'id': id, 'extra': []}    
    if extra:
        temp_doc = get_k_nearest(id)
        for i in temp_doc:
            print(i)
            root = ET.parse('news/' + '%s.xml' % i).getroot()
            title = root.find('title').text
            doc['extra'].append({'id': i, 'title': title})
    # docs.append(doc)
    # headers = {
    #     "User-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    # }       
    # try:
    #     response = requests.get(url=url, headers=headers).content.decode('utf-8',"ignore")
    #     extractor = GeneralNewsExtractor()
    #     article_content = extractor.extract(response)
    #     article_content["url"] = url
    return render_template('find.html', doc=doc)
        
def get_k_nearest(docid, k=5):
    conn = sqlite3.connect('data/ir.db')
    c = conn.cursor()
    c.execute("SELECT * FROM knearest WHERE id=?", (docid,))
    docs = c.fetchone()
    conn.close()
    return docs[1: 1 + (k if k < 5 else 5)] 

def getTitle(url):
    bs = getSoup(url)
    if bs is None:
        return "no article"
    if bs.title is None:
        return "no title"
    title=bs.title.string
    return title

def getSoup(url):
    try:
        c = urllib.request.urlopen(url)
    except:
        return None
    html = c.read()
    bs = BeautifulSoup(html, "lxml")
    return bs

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

@app.route('/go',methods=['POST', 'GET'])
def go( ):
    from forms import Search
    sform = Search()
    db = MySQL.connectDatabase()
    if sform.validate_on_submit():
        search = sform.search.data
        webServer.writeData(connecter, search)
        print(search)
        if request.method == "POST":
            sqt = webServer.readData(connecter)
            val = []
            title = []
            for url in sqt:
                sql = "select id from urllist where url = '" + url + "' ;"
                urlid = MySQL.query(db, sql)
                try:
                    root = ET.parse('news/' + '%s.xml' % urlid[0][0]).getroot()
                    url = root.find('url').text
                    title = root.find('title').text
                    doc = {'url':url,'title':title,'id':urlid[0][0]}
                except:
                    article_content = fetch(url)
                    doc = ET.Element("doc")
                    ET.SubElement(doc, "id").text = "%d"%(urlid[0][0])
                    ET.SubElement(doc, "url").text = url
                    ET.SubElement(doc, "title").text = article_content["title"]
                    ET.SubElement(doc, "datetime").text = article_content["publish_time"]
                    ET.SubElement(doc, "body").text = article_content["content"]
                    tree = ET.ElementTree(doc)
                    tree.write("news/" + "%d.xml"%(urlid[0][0]), encoding = "utf-8", xml_declaration = True)  
                    doc = {'url':url,'title':article_content["title"],'id':urlid[0][0]}
                val.append(doc)
            if len(val) > 1:
                return render_template("result.html", result=val, form1=sform)
        else:
            pass
        val = []
        val.append("%s" % search)
        print(val)
        return render_template('result.html', result=val,form1 = sform)

@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)


if __name__ == '__main__':
    manager.run( )
