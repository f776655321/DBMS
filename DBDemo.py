from DBCRmatcher import DBRowMatcher, DBColMatcher
import mysql.connector

config = {
  "host": 
  "user": 
  "passwd": 
}
host = config['host']
user = config['user']
passwd = config['passwd']
connector = mysql.connector.connect(host = host, user = user, passwd = passwd)

Matcher = DBColMatcher(connector)

connector.close()