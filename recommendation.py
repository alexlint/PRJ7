
from os import listdir
import xml.etree.ElementTree as ET
import jieba
import jieba.analyse
import sqlite3
import configparser
from datetime import *
import math
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
 
class Recommendation:
    swords = set()
    knearest = []
    
    def __init__(self):
        self.swordpath = 'data/stop_words.txt'
        self.txtpath = 'data/idf.txt'
        self.dbpath = 'data/ir.db'
        self.path = path = 'news/'
        f = open(self.swordpath, encoding = 'utf-8')
        words = f.read()
        self.swords = set(words.split('\n'))

    def matrixDB(self):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS knearest''')
        c.execute('''CREATE TABLE knearest
                     (id INTEGER PRIMARY KEY, first INTEGER, second INTEGER,
                     third INTEGER, fourth INTEGER, fifth INTEGER)''')
        for docid, doclist in self.knearest:
            c.execute("INSERT INTO knearest VALUES (?, ?, ?, ?, ?, ?)", tuple([docid] + doclist))
        conn.commit()
        conn.close()
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
            
    
    def BuildMatrix(self, files, topK):
        M = len(files)
        N = 1
        terms = {}
        dt = []
        for i in files:
            root = ET.parse(self.path + i).getroot()
            title = root.find('title').text
            body = root.find('body').text
            docid = int(root.find('id').text)
            try:
                tags = jieba.analyse.extract_tags(title + '。' + body, topK=topK, withWeight=True)
            except:
                continue
            cleaned = {}
            for word, tfidf in tags:
                word = word.strip().lower()
                if word == '' or self.is_number(word):
                    continue
                cleaned[word] = tfidf
                if word not in terms:
                    terms[word] = N
                    N += 1
            dt.append([docid, cleaned])
        matrixmx = [[0 for i in range(N)] for j in range(M)]
        i =0
        for docid, t_tfidf in dt:
            matrixmx[i][0] = docid
            for term, tfidf in t_tfidf.items():
                matrixmx[i][terms[term]] = tfidf
            i += 1

        matrixmx = pd.DataFrame(matrixmx)
        matrixmx.index = matrixmx[0]
        print('matrix shape:(%d %d)'%(matrixmx.shape))
        return matrixmx
        
    def BuildKMatrix(self, matrixmx, k):
        print("BuildKMatrix")
        tmp = np.array(1 - pairwise_distances(matrixmx[matrixmx.columns[1:]], metric = "cosine"))
        sim_matrix = pd.DataFrame(tmp, index = matrixmx.index.tolist(), columns = matrixmx.index.tolist())
        for i in sim_matrix.index:
            if(i== 0):
                return
            tmp = [int(i),[]]
            j = 0
            while j < k:
                max_col = sim_matrix.loc[i].idxmax(axis = 1)
                sim_matrix.loc[i][max_col] =  -1
                try:
                    if max_col.astype(int) != i:
                        tmp[1].append(int(max_col))
                        j += 1
                except:
                    continue
            self.knearest.append(tmp)
    
    def genIDF(self):
        files = listdir(self.path)
        n = float(len(files))
        idf = {}
        for i in files:
            root = ET.parse(self.path + i).getroot()
            title = root.find('title').text
            body = root.find('body').text
            try:
                ss = jieba.analyse.extract_tags(title+'。'+body, topK = 5, allowPOS = ("ns", "n", "vn", "v"))
            except:
                continue
            finalRt = []
            for s in ss:
                if s[0] in self.swords:
                    continue
                else:
                    finalRt.append(s)
            for word in finalRt:
                word = word.strip().lower()
                if word == '' or self.is_number(word):
                    continue
                if word not in idf:
                    idf[word] = 1
                else:
                    idf[word] = idf[word] + 1
        idf_file = open(self.txtpath, 'w', encoding = 'utf-8')
        for word, df in idf.items():
            idf_file.write('%s %.9f\n'%(word, math.log(n / df)))
        idf_file.close()
        
    def kNearest(self, k, topK):
        self.genIDF()
        files = listdir(self.path)
        matrixmx = self.BuildMatrix(files, topK)
        self.BuildKMatrix(matrixmx, k)
        self.matrixDB()
        
if __name__ == "__main__":
    print('-----start time: %s-----'%(datetime.today()))
    rm = Recommendation()
    rm.kNearest(5,20)
    print('-----finish time: %s-----'%(datetime.today()))
    