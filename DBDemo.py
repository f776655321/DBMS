from CRmatcher import DBMatcher

config ={
  "host": "127.0.0.1",
  "user": "root",
  "passwd": "kevin777"
}
DB = DBMatcher(config)

result = DB.Match(True, 'Source', 'Target', 'texas_govs_1', 'texas_govs_1', 'Governor', "Governor's_Name")
print(result)