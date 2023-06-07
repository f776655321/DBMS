import os
from argparse import ArgumentParser
from LM_matcher import FileRowMatcher

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--input_data_dir', type=str,
                        default='./data')
    parser.add_argument('--benchmark', type=str,
                        default='autojoin-Benchmark')
    parser.add_argument('--case', type=str,
                        default='fruits 1')
    parser.add_argument('--output_file', type=str,
                        default='./output.csv')

    args = parser.parse_args()
    return args

#This function is just to get our data
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
        foreign_file = 'source.csv'
        foreign_key = src_col
        primary_key = target_col
        primary_file = 'target.csv'
    else:
        foreign_file = 'target.csv'
        foreign_key = target_col
        primary_key = src_col
        primary_file = 'source.csv'

    return foreign_file, foreign_key, primary_key, primary_file

if __name__ == '__main__':
    args = parse_arguments()

    RowMatcher = FileRowMatcher()

    foreign_file, foreign_key, primary_key, primary_file = get_data(args.input_data_dir,args.benchmark,args.case)

    data_dir = os.path.join(args.input_data_dir,args.benchmark,args.case)

    RowMatcher.find(data_dir, args.output_file, foreign_key, primary_key, foreign_file, primary_file)

