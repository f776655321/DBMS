from CRmatcher import CSVMatcher

primary_file = 'data/autojoin-Benchmark/texas govs 1/source.csv'
foreign_file = 'data/autojoin-Benchmark/texas govs 1/target.csv'

CSV = CSVMatcher()

# 1 to 1
# result = CSV.Match(True, primary_file, foreign_file, 'Governor')
# print(result)

primary_file = 'data/multi_primary/source.csv'
foreign_file = 'data/multi_primary/target.csv'

# result = CSV.Match(True, primary_file, foreign_file, ['FirstName','LastName'])
# print(result)

primary_file = 'data/multi_foreign/source.csv'
foreign_file = 'data/multi_foreign/target.csv'

result = CSV.Match(True, primary_file, foreign_file, "Governor's Name", find_col=2)
print(result)