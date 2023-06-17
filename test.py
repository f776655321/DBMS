from Match import CSVMatcher, DBMatcher

primary_file = 'data/autojoin-Benchmark/texas govs 1/source.csv'
foreign_file = 'data/autojoin-Benchmark/texas govs 1/target.csv'
config ={
  "host": "127.0.0.1",
  "user": "root",
  "passwd": "kevin777"
}
CSV = CSVMatcher()
DB = DBMatcher(config)
result = CSV.Match(True, primary_file, foreign_file, 'Governor', "Governor's Name")
print(result)
result = DB.Match(True, 'Source', 'Target', 'texas_govs_1', 'texas_govs_1', 'Governor', "Governor's_Name")
print(result)