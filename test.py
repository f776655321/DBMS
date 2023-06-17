from Match import CSVMatcher

primary_file = 'data/autojoin-Benchmark/texas govs 1/source.csv'
foreign_file = 'data/autojoin-Benchmark/texas govs 1/target.csv'
CSV = CSVMatcher()
result = CSV.Row_Matcher(True, 'Governor', "Governor's Name", primary_file, foreign_file)
print(result)