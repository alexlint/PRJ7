import pymysql 
import sys

def connectDatabase():
    try:
        db = pymysql.connect(host="localhost",user="root",password="lintao1998",db="search",charset="utf8")
    except:
        print("database connect error")
        sys.exit()
    return db

def insertValues(db, table, keys, values):
    sqlcode = "insert into " + table
    cu = ','.join(keys)
    cu = "(" + cu + ")"
    sqlcode = sqlcode + cu
    sqlcode = sqlcode + " values "
    for value in values:
        strt =",".join(value)
        strt = "(" + strt + "),"
        sqlcode = sqlcode + strt
    print (sqlcode[0:-1])
    try:
        cursor = db.cursor()
        if len(sqlcode) > 500:
            return None
        cursor.execute(sqlcode[0:-1])
        db.commit()
    except:
        db.rollback()
        print("insert error")

def query(db, sqlcode):
    cursor = db.cursor()
    try:
        cursor.execute(sqlcode)
    except:
        print("query error %s" %(sqlcode))
        sys.exit()
    return cursor.fetchall()

def disconnect(db):
    db.close()


        
def main():
    db = connectDatabase()
    createTable(db)

if __name__ == "__main__":
    main()
