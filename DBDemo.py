from DBCRmatcher import DBRowMatcher, DBColMatcher
import mysql.connector

config = {
  "host": "127.0.0.1",
  "user": "root",
  "passwd": "kevin777"
}

Matcher = DBRowMatcher(config)
result = Matcher.find(True, 'Governor', "Governor's_Name", 'texas_govs_1', 'texas_govs_1', 'Source', 'Target')
print(result)

