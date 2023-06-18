from CRmatcher import CSVMatcher

primary_file = 'data/autojoin-Benchmark/texas govs 1/source.csv'
foreign_file = 'data/autojoin-Benchmark/texas govs 1/target.csv'

CSV = CSVMatcher()

result = CSV.Match(True, primary_file, foreign_file, ['Governor', 'Party'])
print(result)