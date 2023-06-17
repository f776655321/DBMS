from DBCRmatcher import DBRowMatcher, DBColMatcher
import mysql.connector

config = {
  "host": "127.0.0.1",
  "user": "root",
  "passwd": "kevin777"
}

Matcher = DBRowMatcher(config)
Matcher.find(False, 'United_States_Cities', 'City', 'us_cities', 'us_cities', 'Source', 'Target')

