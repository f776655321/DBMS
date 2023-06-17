from CRmatcher import ColMatcher, RowMatcher
from argparse import ArgumentParser
import os

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--input_data_dir', type=str,
                        default='./data')
    parser.add_argument('--benchmark', type=str,
                        default='autojoin-Benchmark')
    parser.add_argument('--case', type=str,
                        default='fruits 1')
    parser.add_argument('--output_file', type=str,
                        default=True)

    args = parser.parse_args()
    return args

#This function is just to get our data.
def get_data(input_data_dir,benchmark,case):
    with open(os.path.join(input_data_dir,benchmark,case,'rows.txt'), 'r') as file:
        i = 0
        
        for line in file:
            if( i == 0):
                line = line.strip('\n').split(':')
                src_col = line[0]
                target_col = line[1]

                i += 1

            else:
                
                direction = line

    if(direction == 'source'):
        foreign_file = os.path.join(input_data_dir,benchmark,case,'source.csv')
        foreign_key = src_col
        primary_key = target_col
        primary_file = os.path.join(input_data_dir,benchmark,case,'target.csv')
    else:
        foreign_file = os.path.join(input_data_dir,benchmark,case,'target.csv')
        foreign_key = target_col
        primary_key = src_col
        primary_file = os.path.join(input_data_dir,benchmark,case,'source.csv')

    return foreign_file, foreign_key, primary_key, primary_file

if __name__ == '__main__':
    
    args = parse_arguments()

    # We don't use foreign_column.
    foreign_file, foreign_column, primary_column, primary_file = get_data(args.input_data_dir,args.benchmark,args.case)

    col_matcher = ColMatcher()
    
    tables = col_matcher.files_to_tables(primary_file, foreign_file)

    foreign_column = col_matcher.get_column_matching(tables[0], tables[1], primary_column)

    row_matcher = RowMatcher()

    result = row_matcher.find(args.output_file, primary_column, foreign_column, primary_file, foreign_file)



