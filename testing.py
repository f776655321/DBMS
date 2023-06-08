from column_matcher import column_matcher
import sys
    
args = sys.argv[:]
primary_file = args[1]
foreign_file = args[2]
primary_key_column = args[3]

my_col_matcher = column_matcher()
tables = my_col_matcher.files_to_tables(primary_file, foreign_file)
target_column = my_col_matcher.get_column_matching(tables[0], tables[1], primary_key_column)
print(target_column)